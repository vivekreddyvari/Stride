import collections.abc
import gzip
import json
import random
import tempfile
import os
import re
from bs4 import BeautifulSoup


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
    """ create dictionary obj
    Product Details:
      - body
      - crawled_at
      - page_type
      - page_url

    Product Overview:
    """
    # Initialize empty lists
    body = []
    crawled_at = []
    page_type = []
    page_url = []

    for index in random.sample(range(len(json_array)), 100):
        obj = json_array[index]

        # HTML Parsing
        html_parsing = obj['body']
        url = obj['page_url']

        # Parse the page to fetch relavant information
        htmlScrapper(html_parsing, url)  # HTML Scrapping
        print("The page type is ", obj['page_type'])
        print("\n\n\n")

        if obj['page_type'] == 'product_listing':
            print(obj['page_url'])
            print(obj['page_number'])
            print(obj['crawled_at'])
            print(obj['product_category'])
            print(obj['ordering'])
            web_site_text = obj['body']

            soup = BeautifulSoup(web_site_text, features="html.parser")
            print(soup.prettify())
            print("\n\n\n")
        # print(obj['crawled_at'])
        # print(obj['page_url'])
        # print('object[{}]: {!r}'.format(index, obj))


def htmlScrapper(html, url):
    """ This function scraps the html and extracts product details
    from the competitors """
    # Scrap the data
    soup = BeautifulSoup(html, features="html.parser")

    # Initialize the variable
    product_type = []
    ptype_cat = []
    product_name = []
    pname = []
    price = []
    cost_ext = []
    cost_dis = []
    brand_name = []
    brand = []
    html_omoda = ''

    # Find the competitors
    is_zalando = 'zalando'
    is_omoda = 'omoda'
    is_ziengs = 'ziengs'
    zalando_match = re.findall(is_zalando, url)
    omoda_match = re.findall(is_omoda, url)
    ziengs_match = re.findall(is_ziengs, url)

    # Competitor Zalando
    if is_zalando in zalando_match:
        for elements in soup.findAll('div', attrs={'id':'wrapper'}):
            try:
                product_type = (elements.find('ul', attrs={'class': 'breadcrumbs'})).text
                product_name = (elements.find('span', attrs={'itemprop': 'name'})).text
                brand_name = (elements.find('span', attrs={'itemprop': 'brand'})).text
                price = (elements.find('span', attrs={'class': 'price nowrap'})).text
            except AttributeError:
                product_type = 'None'
                product_name = 'None'
                brand_name = 'None'
                price = 'None'

            # format product type to extract specific name
            if product_type != 'None':
                conv_string = product_type.split('\n')
                values = [val.strip("\xa0/") for val in conv_string if val != '' and val != ' ']
                len_of_values = len(values)
                if len_of_values != 0 and len_of_values <= 3:
                    product_type = values[2] + ' ' + values[3] + ' ' + values[4]
                else:
                    product_type = values[2] + ' ' + values[3]

            # format price with many blank lines
            if price != 'None':
                price = re.sub(r'\n', '', price)

        print("The Product Category is:", product_type)
        print("The Product Name is:", product_name)
        print("The Product Brand is:", brand_name)
        print("The product price is:", price)
        # print("The cost of the product is:", cost_ext)
        # print("The disc of the product is:", cost_dis)

    # Competitor Omoda
    if is_omoda in omoda_match:
        for elements in soup.findAll('div', attrs={'id': 'site'}):

            # Extract Product details
            try:
                product_type = (elements.find('table', attrs={'class': 'detail-kenmerken'})).text
                product_name = (elements.find('h1', attrs={'itemprop': 'name'})).text
                price = (elements.find('div', attrs={'class': 'prijs clearfix'})).text
            except AttributeError:
                product_type = 'None'
                product_name = 'None'
                price = 'None'

            if product_type != 'None':
                ptype_cat = ExtractOmodaPtype(product_type, ptype_cat)

            # Product Name and Brand
            if product_name != 'None':
                pname_brand = ExtractOmodaPname(product_name, pname, brand)
                pname = pname_brand[0]  # product Name
                brand_name = pname_brand[1]  # products Brand

            # Product Price - actual price and discount price
            if price != 'None':
                cost_extracted = ExtractOmodaPrice(price, cost_dis, cost_ext)
                # if cost has discount price, then object becomes tuple,
                is_tuple = type(cost_extracted)

                if is_tuple == type(cost_extracted):
                    cost_ext = cost_extracted[0]
                    if len(cost_extracted) == 2:
                        cost_dis = cost_extracted[1]
                    else:
                        cost_dis = '0'
                else:
                    cost_ext = cost_extracted

        # print(soup.prettify())
        # print(url)

        print("The Product Category is:", ptype_cat)
        print("The Product Name is:", pname)
        print("The Product Brand is:", brand_name)
        # print(price)
        print("The cost of the product is:", cost_ext)
        print("The disc of the product is:", cost_dis)

    # Competitor Ziengs
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
    # print(product_type)
    # print(product_name)
    # print(brand_name)
    # print(price)

    pass

def ExtractOmodaPtype(type, category_product):
    """
    :param type
    :return: Product Category
    """
    split_the_text = type.split('\n')
    category_product = [val for val in split_the_text if val != '' and val != ' ']
    return category_product[7]


def ExtractOmodaPname(name, product_name, brand):
    """
    :param name, product_name, brand
    :return: product_name, brand
    """
    split_the_text = name.split(' ')
    pname_not_blank = [val for val in split_the_text if val != '' and val != ' ']
    product_name = ' '.join([pname_not_blank[i] for i in [0,1,2]])
    brand = ' '.join([pname_not_blank[i] for i in [1]])
    return product_name, brand


def ExtractOmodaPrice(cost_text, cost, disc):
    """
    :param cost_text, cost, disc
    :return: Actual Cost, Disc
    """
    split_the_text = cost_text.split('\n')
    extracted_value = [val for val in split_the_text if val != '' and val != ' ']

    # Check the product has discounted price with Sale indication.
    check_values = extracted_value[0]
    if check_values == 'Sale':
        actual_price = extracted_value[1]
        discount_price = extracted_value[2]
        return actual_price, discount_price
    elif check_values == 'Vanaf':
         check_values = extracted_value[0]
         return check_values
    else:
        check_values = extracted_value
        return check_values


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
