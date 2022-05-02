import gzip
import io
import os
import json_lines
import jsonlines
import json

strpath = r"/Users/vivekreddyvari/opt/anaconda/Flask/Assignment"

def ListDirectory(dir, gz_name=''):
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


competitor_data = (ListDirectory(strpath))

def Create_JL_file(file):
    """ Create a .jl file """
    with gzip.open(file, 'rb') as input_file:
        for input_file_information in input_file:
            # print(input_file_information)
            tempfile = io.BytesIO(input_file_information)

            # reader = jsonlines.Reader(tempfile)




print(Create_JL_file(competitor_data))
#with gzip.open(competitor_data, 'rb') as information:
#    for line in information:

