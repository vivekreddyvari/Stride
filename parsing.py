import collections.abc
import gzip
import json
import random
import tempfile
import os
import re
from bs4 import BeautifulSoup
import pymongo

# connect to db
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
        )
    db = mongo.crawl
    mongo.server_info()  # trigger exception if db connection failed
except:
    print("ERROR - cannot connect to db")


class GZ_JSON_Array(collections.abc.Sequence):
    """ Allows objects in gzipped file of JSON objects, one-per-line, to be
        treated as an immutable sequence of JSON objects.
    """
    def __init__(self, gzip_filename):
        self.tmpfile = tempfile.TemporaryFile('w+b')
        # Decompress a gzip file into a temp file and save offsets of the
        # start of each line in it.
        self.offsets = []
        with gzip.open(gzip_filename, mode='rb') as gzip_file:
            for line in gzip_file:
                line = line.rstrip().decode('utf-8')
                if line:
                    self.offsets.append(self.tmpfile.tell())
                    self.tmpfile.write(bytes(line + '\n', encoding='utf-8'))

    def __len__(self):
        return len(self.offsets)

    def __iter__(self):
        for index in range(len(self)):
            yield self[index]

    def __getitem__(self, index):
        """ Return a JSON object at offsets[index] in the given open file. """
        if index not in range(len(self.offsets)):
            raise IndexError
        self.tmpfile.seek(self.offsets[index])
        try:
            size = self.offsets[index+1] - self.offsets[index]  # Difference with next.
        except IndexError:
            size = -1  # Last one - read all remaining data.
        return json.loads(self.tmpfile.read(size).decode())

    def __del__(self):
        try:
            self.tmpfile.close()  # Allow it to auto-delete.
        except Exception:
            pass


def ListDirectory(dir, gz_name):
    """
    :param dir:
    :param gz_name:
    :return: List the folders and files
    """

    file_names = os.listdir(dir)
    file_names = [i for i in file_names if os.path.isfile(i)]

    for name in file_names:
        gz_type = '.gz'
        if any(gz_type in x for x in file_names):
            gz_name = name
        else:
            print("Not found")
    return gz_name


def checkJson(array):
    """ create Crawl DB with following collections
    1) Product Overview:
    2) Product Details:

    """
    # Initialize empty lists
    body = []
    crawled_at = []
    page_type = []
    page_url = []

    for index in random.sample(range(len(json_array)), 1000):
        obj = json_array[index]

        # determine competitor?
        competitor = determine_competitor(obj['page_url'])

        if obj['page_type'] == 'product_detail':
            schema_of_detail = {}

            # HTML Parsing
            html_parsing = obj['body']
            url = obj['page_url']

            # Parse the page to fetch relevant information and HTML Scrapping
            zalando_info = {}
            omoda_info = {}
            scrapped_data = html_scrapper(html_parsing,
                          url,
                          zalando_info,
                          omoda_info)

            if 'zalando' in competitor and scrapped_data != {} :
                schema_of_detail['page_type'] = obj['page_type']
                schema_of_detail['page_url'] = obj['page_url']
                schema_of_detail['crawled_at'] = obj['crawled_at']
                schema_of_detail['body'] = obj['body']
                schema_of_detail['competitor'] = competitor
                schema_of_detail['zalando_info'] = scrapped_data
                # db.productdetail.insert_one(schema_of_detail)

            if 'omoda' in competitor and scrapped_data != {}:
                schema_of_detail['page_type'] = obj['page_type']
                schema_of_detail['page_url'] = obj['page_url']
                schema_of_detail['crawled_at'] = obj['crawled_at']
                schema_of_detail['body'] = obj['body']
                schema_of_detail['competitor'] = competitor
                schema_of_detail['omoda_info'] = scrapped_data
                # db.productdetail.insert_one(schema_of_detail)

        if obj['page_type'] == 'product_listing':
            schema_of_overview = {}
            if 'ziengs' not in competitor:
                schema_of_overview['page_type'] = obj['page_type']
                schema_of_overview['page_url'] = obj['page_url']
                schema_of_overview['page_number'] = obj['page_number']
                schema_of_overview['crawled_at'] = obj['crawled_at']
                schema_of_overview['product_category'] = obj['product_category']
                schema_of_overview['ordering'] = obj['ordering']
                schema_of_overview['competitor'] = competitor
                schema_of_overview['body'] = obj['body']
                # db.productoverview.insert_one(schema_of_overview)


def html_scrapper(
        html,
        url,
        zalando_info,
        omoda_info):

    """ This function scraps the html and extracts product details
    from the competitors
    :param html, url
    :return zalando information, omoda information
    """

    # Scrap the data
    soup = BeautifulSoup(html, features="html.parser")

    # Find the competitors
    is_zalando = 'zalando'
    is_omoda = 'omoda'
    is_ziengs = 'ziengs'
    zalando_match = re.findall(is_zalando, url)
    omoda_match = re.findall(is_omoda, url)
    ziengs_match = re.findall(is_ziengs, url)

    # Competitor Zalando
    zalando_info = {}
    if is_zalando in zalando_match:
        for elements in soup.findAll('div', attrs={'id':'wrapper'}):
            try:
                product_type = (elements.find('ul', attrs={'class': 'breadcrumbs'})).text
                zalando_info['product_name'] = (elements.find('span', attrs={'itemprop': 'name'})).text
                zalando_info['brand_name'] = (elements.find('span', attrs={'itemprop': 'brand'})).text
                price = (elements.find('span', attrs={'class': 'price nowrap'})).text
            except AttributeError:
                product_type = 'None'
                zalando_info['product_type'] = product_type
                zalando_info['product_name'] = 'None'
                zalando_info['brand_name'] = 'None'
                price = 'None'
                zalando_info['price'] = price

            # format product type to extract specific name
            if product_type != 'None':
                conv_string = product_type.split('\n')
                values = [val.strip("\xa0/") for val in conv_string if val != '' and val != ' ']
                len_of_values = len(values)
                if len_of_values != 0 and len_of_values <= 3:
                    zalando_info['product_type'] = values[2] + ' ' + values[3] + ' ' + values[4]
                else:
                    zalando_info['product_type'] = values[2] + ' ' + values[3]

            # format price with many blank lines
            if price != 'None':
                zalando_info['price'] = re.sub(r'\n', '', price)

        return zalando_info

    # Competitor Omoda
    omoda_info = {}
    if is_omoda in omoda_match:
        for elements in soup.findAll('div', attrs={'id': 'site'}):

            # Extract Product details
            try:
                product_type = (elements.find('table', attrs={'class': 'detail-kenmerken'})).text
                product_name = (elements.find('h1', attrs={'itemprop': 'name'})).text
                price = (elements.find('div', attrs={'class': 'prijs clearfix'})).text
                competitor_check = is_omoda
            except AttributeError:
                product_type = 'None'
                product_name = 'None'
                price = 'None'

            ptype_cat = ' '
            if product_type != 'None':
                ptype_cat = extract_omoda_ptype(product_type, ptype_cat)
                omoda_info['ptype_cat'] = ptype_cat

            # Product Name and Brand
            if product_name != 'None':
                brand = ''
                pname = ''
                pname_brand = extract_omoda_pname(product_name, pname, brand)
                omoda_info['pname'] = pname_brand[0]  # product Name
                omoda_info['brand_name'] = pname_brand[1]  # products Brand

            # Product Price - actual price and discount price
            if price != 'None':
                cost_dis = ''
                cost_ext = ''
                cost_extracted = extract_omoda_price(price, cost_dis, cost_ext)
                # if cost has discount price, then object becomes tuple,
                is_tuple = type(cost_extracted)

                if is_tuple == type(cost_extracted):
                    omoda_info['cost_ext'] = cost_extracted[0].replace('\xa0', ' ')
                    if len(cost_extracted) == 2:
                        omoda_info['cost_dis'] = cost_extracted[1]
                    else:
                        omoda_info['cost_dis'] = '0'
                else:
                    omoda_info['cost_ext'] = cost_extracted
        return omoda_info

    # Competitor Ziengs (kept aside)
    """ 
    if is_ziengs in ziengs_match:
        for elements in soup.findAll('div', attrs={'id':'wrapper'}):
            product_type = elements.find('li', attrs={'class': 'level0 parent active'})
            product_name = elements.find('span', attrs={'itemprop': 'name'})
            brand_name = elements.find('span', attrs={'itemprop': 'brand'})
            price = elements.find('span', attrs={'class': 'price nowrap'})

    else:
            product_type = 'None'
            product_name = 'None'
            brand_name = 'None'
            price = 'None'
    """



def extract_omoda_ptype(type, category_product):
    """
    :param type
    :return: Product Category
    """
    split_the_text = type.split('\n')
    category_product = [val for val in split_the_text if val != '' and val != ' ']
    return category_product[7]


def extract_omoda_pname(name, product_name, brand):
    """
    :param name, product_name, brand
    :return: product_name, brand
    """
    split_the_text = name.split(' ')
    pname_not_blank = [val for val in split_the_text if val != '' and val != ' ']
    product_name = ' '.join([pname_not_blank[i] for i in [0,1,2]])
    brand = ' '.join([pname_not_blank[i] for i in [1]])
    return product_name, brand


def extract_omoda_price(cost_text, cost, disc):
    """
    :param cost_text, cost, disc
    :return: Actual Cost, Disc
    """
    split_the_text = cost_text.split('\n')
    extracted_value = [val for val in split_the_text if val != '' and val != ' ']

    # Check the product has discounted price with Sale indication.
    check_values = extracted_value[0]
    if check_values == 'Sale':
        actual_price = extracted_value[1].replace('\xa0', ' ')
        discount_price = extracted_value[2].replace('\xa0', ' ')
        return actual_price, discount_price
    elif check_values == 'Vanaf':
         check_values = extracted_value[0].replace('\xa0', ' ')
         return check_values
    else:
        check_values = extracted_value
        return check_values


def determine_competitor(url):
    """ This functions returns competitor name
    :param url
    :return competitor_name
    """
    is_zalando = 'zalando'
    is_omoda = 'omoda'
    is_ziengs = 'ziengs'
    zalando_match = re.findall(is_zalando, url)
    omoda_match = re.findall(is_omoda, url)
    ziengs_match = re.findall(is_ziengs, url)

    if is_zalando in zalando_match:
        competitor_name = is_zalando
    elif is_omoda in omoda_match:
        competitor_name = is_omoda
    elif is_ziengs in ziengs_match:
        competitor_name = is_ziengs
    else:
        competitor_name = "competitor NOT FOUND"

    return competitor_name


if __name__ == '__main__':
    path_name = ''
    # data extract path
    strpath = r"/Users/vivekreddyvari/opt/anaconda/Flask/Assignment"

    # Extract data from (.gz)
    gzip_filename = ListDirectory(strpath, path_name)

    # convert to JSON format
    json_array = GZ_JSON_Array(gzip_filename)

    # Check the JSON file and extract data
    checkJson(json_array)

    # Randomly access some objects in the JSON array.

    ''' 
    # this is only for testing purpose
    for index in random.sample(range(len(json_array)), 2):
        obj = json_array[index]
        print(obj)
        # print('object[{}]: {!r}'.format(index, obj))
    '''
