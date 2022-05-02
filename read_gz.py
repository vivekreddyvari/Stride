import gzip
import os.path
from io import BytesIO

import patoolib
import os
import glob
import json
from bs4 import BeautifulSoup



strpath = r"/Users/vivekreddyvari/opt/anaconda/Flask/Assignment"
dstpath = r"/Users/vivekreddyvari/opt/anaconda/Flask/Assignment/ext"

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


def ReadGzFile(input_file_path, count=0):
    ''' Read the gz zip and extract the files to the path'''
    competitors = []
    with gzip.open(input_file_path, 'rb') as f:

        for line in f:
            if len(line.strip()) != 0:
                compe_data = BytesIO(line)
                competitors.append(compe_data)

    return competitors

def getCompetitors(competitors):

    for key, value in competitors:
        print(key)

    return key
        # for i, name in enumerate(f):
        #    pass
        # count = "File {1} contain {0} lines".format(i+1, input_file_path)

        # data = json.loads(f.read())
        # print(data)

        #return count







path_name = ''
gz_file_name = ListDirectory(strpath, path_name)
print(gz_file_name)
dst = 'd'
json_name = ReadGzFile(gz_file_name)
print(json_name)
# idx = 'idx'
getCompetitors((json_name))

""" 
for key, value in obj.items():
    body.append(obj['body'])
    # crawled_at.append(obj['crawled_at'])
    # page_type.append(obj['page_type'])
    # page_url.append(obj['page_url'])

    pass
print(body)
# save columns into a dataframe

# output_df = pd.DataFrame({'page_type': page_type, 'page_url': page_url, 'crawled_at': crawled_at, 'body': body })
"""



