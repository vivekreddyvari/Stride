import collections.abc
import gzip
import json
import random
import tempfile
import os
import pandas as pd
import numpy as np
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
    ''' List the folders and files '''
    fileNames = os.listdir(dir)
    for fileName in fileNames:
        gz_type = '.gz'
        if any(gz_type in x for x in fileNames):
            # print("The gz file type found: ", fileName)
            gz_name = fileName
        else:
            print("Not found")
    return gz_name


def checkJson(array):
    ''' create dictionary obj'''
    """ Product Details:
      - body
      - crawled_at
      - page_type
      - page_url """
    # Initialize empty lists
    body = []
    crawled_at = []
    page_type = []
    page_url = []

    for index in random.sample(range(len(json_array)), 2):
        obj = json_array[index]
        html_parsing = obj['body']
        htmlScrapper(html_parsing)
        # print(obj['body'])
        # print(obj['page_type'])
        # print(obj['crawled_at'])
        # print(obj['page_url'])
        # print('object[{}]: {!r}'.format(index, obj))





def htmlScrapper(html):
    ''' This function scraps the html '''
    soup = BeautifulSoup(html, features="html.parser")
    product_type = []
    product_name = []
    price = []
    brand_name = []
    for elements in soup.findAll('div', attrs={'id':'wrapper'}):
        product_type = elements.find('li', attrs={'class': 'level0 parent active'})
        product_name = elements.find('span', attrs={'itemprop': 'name'})
        brand_name = elements.find('span', attrs={'itemprop': 'brand'})
        price = elements.find('span', attrs={'class': 'price nowrap'})
    print(product_type.text)
    print(product_name.text)
    print(brand_name.text)
    print(price.text)


    pass

if __name__ == '__main__':
    path_name = ''
    strpath = r"/Users/vivekreddyvari/opt/anaconda/Flask/Assignment"
    gzip_filename = ListDirectory(strpath, path_name)

    json_array = GZ_JSON_Array(gzip_filename)

    checkJson(json_array)


    # Randomly access some objects in the JSON array.
    ''' 
    for index in random.sample(range(len(json_array)), 2):
        obj = json_array[index]
        print(obj)
        # print('object[{}]: {!r}'.format(index, obj))
    '''