##This script takes a JSON file of a paper (wish I knew the name of the format)
#and makes it into a txt file, puting a newline each paragraph.

import sys
import json
from os import listdir
from os.path import isfile, join

mypath = '../comm_use_subset_100/'
filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
with open('generated_text.txt', 'w') as out_file:
    for paper in filenames:
        if paper.endswith('.json'):
            with open(mypath + paper, 'r') as json_file:
                data = json.load(json_file) #Dictionary containing the json file
                if data["metadata"]:
                    title = data['metadata']['title']
                    out_file.write(title + '\n\n')
                if data['abstract']:
                    if isinstance(data['abstract'],list):
                        data['abstract'] = data['abstract'][0]
                    abstract = data['abstract']['text']
                    out_file.write(abstract + '\n\n')
                for sentence in data['body_text']:
                    out_file.write(sentence['text'] + '\n\n')
