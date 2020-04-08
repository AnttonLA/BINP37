##This script transforms the output file given by BioBERT and outputs a JSON files
#in the PubAnnotation format

import re
import json

def extract_text_entities(raw_parag): #Extract text and the entities form the paragraph
    full_parag = ''
    entities = []
    ent_positions = []

    single_entity = ''
    for line in raw_parag:

        #Rebuild text from the tsv file
        word = re.findall(r'^([\S]+)',line)
        word = word[0] #For each line, add the word to the full paragraph
        full_parag = full_parag + word + ' '
        #Isolate Named Entites using info from the tsv file
        if re.findall(r'B-MISC',line): #THIS CODE IS REALLY FRAGILE. FIX!
            single_entity = word
            start_pos = len(full_parag) - len(word) - 1 #-1 because 1st pos is 0
        elif re.findall(r'I-MISC',line) and single_entity != '':
            single_entity = single_entity + ' ' + word
        else:
            if single_entity != '':
                entities.append(single_entity)
                end_pos = len(full_parag) - len(word) - 1
                ent_positions.append((start_pos, end_pos))
            single_entity = ''

    if single_entity != '': #In case last word is not 'O'
            entities.append(single_entity)
            end_pos = len(full_parag)-1
            ent_positions.append((start_pos, end_pos))

    return full_parag.rstrip(), entities, ent_positions
'''
testarray = ['Function O-MISC O-MISC\n', 'of O-MISC O-MISC\n', 'the O-MISC O-MISC\n',\
'Deubiquitinating O-MISC B-MISC\n', 'green O-MISC I-MISC\n',\
'moose O-MISC I-MISC\n', 'radar O-MISC O-MISC\n', 'on O-MISC O-MISC\n',\
'the O-MISC O-MISC\n', 'Paracetamol O-MISC B-MISC\n', 'bears O-MISC I-MISC\n',\
'in O-MISC O-MISC\n', 'Mexico O-MISC O-MISC\n']
'''

with open('generated_json.json', 'w') as out_file:
    with open('./NER_result_conll.txt', 'r') as in_file:
        paragraph = []
        count = 0 #Counter for testing purposes. DELETE LATER
        for line in in_file:
            if line == '\n': #End of paragraph
                full_text, ents, ent_span = extract_text_entities(paragraph)
                denot_array = []
                if ents: #If there are entities for this paragraph
                    for i in range(len(ents)):
                        denot_array.append({"id": i+1, "span": {"begin": ent_span[i][0], "end": ent_span[i][1]}, "obj": 'ne'})
                tmp_dict = {
                    "text": full_text, #Add full text
                    "denotations": denot_array
                }
                out_file.write(json.dumps(tmp_dict))
                paragraph = [] #Empty paragraph
                count += 1 #Counter for testing purposes. DELETE LATER
                if count > 1: #Counter for testing purposes. DELETE LATER
                    break #Counter for testing purposes. DELETE LATER
            else:
                paragraph.append(line)
