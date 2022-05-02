import json_lines
import os.path
import pandas as pd
import json
from bs4 import BeautifulSoup
# Try to find the folder

folder = os.path.expanduser("~/Desktop/book/Motivation Letters/99 Resume /18 Nelson/09 Assignment /Vivek Reddyvari Cover Letter//crawl_ziengs.nl_2016-05-30T23-15-20.jl")
# folder = os.path.expanduser("~/Desktop/book/Motivation Letters/99 Resume /18 Nelson/09 Assignment /Vivek Reddyvari Cover Letter.gz")

df = pd.DataFrame()
count = 0
items = {}
with open(folder, 'rb') as f:
    for item in json_lines.reader(f):
        # print(item)
        count += 1
        items.update(item)
        # conv = json.loads(item)
        # df = df.append(conv, ignore_index = True)
        # df.head()
    print(count)
    print((items))
    if item == items:
        print("True")
    else:
        print("False")

    print("size of single item " + str(item.__sizeof__()) + " bytes")
    print("size of single items " + str(items.__sizeof__()) + " bytes")

    # print(item) # comment the item
    for key, value in items.items():
        print(key)


    """for key, value in item.items():
        print(key)
        # print(value)
    #print(item['body'])
    #print(item['crawled_at'])
    #print(item['page_type'])
    #print(item['page_url'])
    """


    s = BeautifulSoup(items['body'])

    # s = s.prettify()
    # html_file = open("ziengs_sample", "w")
    # html_file.write(s)
    # html_file.close()

    print(s.prettify())

    # print(s.head)
    # print(s.h1)
    # print(s.h2)
    # print(s.h3)
    # print(s.h4)
    # print(s.li)
    """ Recursive child generator """
    ''' for tags in s.recursiveChildGenerator():
        # traverse the names of the tags
            if tags.name:
                print(tags.name) '''

    """ finding all elements 
    for tag in s.findAll('p'):
        print(f'{tag.name}: {tag.text}')
    """

# with json_lines.open(folder) as f:
#    for item in f:
#        print(item['x'])

# try:
#    with zipfile.ZipFile(zip_file) as z:
#        z.extractall("temp")
#        print("Extract all")
# except:
#    print("Invalid file")
# path = "//Users//vivekreddyvari//Desktop//book//Motivation Letters//99 Resume //18 Nelson//09 Assignment //Vivek Reddyvari Cover Letter//crawl_ziengs.nl_2016-05-30T23-15-20.jl"

# ziengs_df = pd.read_json(folder, lines=True)
# ziengs_df.head(5)