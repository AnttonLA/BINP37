#Script that will extract a list of disease names from the mondo.json files

import json

with open('/Users/Tony/Downloads/mondo.json', 'r') as in_json:
    with open('disease_name_list.txt', 'w') as out_file:
        data = json.load(in_json)
        old_basicProp = []
        last_disease = []

        for index, key in enumerate(data["graphs"][0]["nodes"]):
            """
            if "meta" in data["graphs"][0]["nodes"][index]:  # Get the synonims
                if "basicPropertyValues" in data["graphs"][0]["nodes"][index]["meta"]: # Skip cells
                    basicProp = data["graphs"][0]["nodes"][index]["meta"]["basicPropertyValues"][0]["val"]
                    if basicProp == "cell":
                        pass
            """
            id = ''
            if "id" in data["graphs"][0]["nodes"][index]:
                id = data["graphs"][0]["nodes"][index]["id"]
            
            if "lbl" in data["graphs"][0]["nodes"][index]:  # Get "label", the main name.
                current_name = data["graphs"][0]["nodes"][index]["lbl"]
                if current_name.startswith('obsolete'):  # Remove 'obsolete' tag from disease name
                    current_name = current_name[9:]
                if last_disease != current_name:  # Avoid writing duplicate names
                    out_file.write(current_name + "\t" + id + "\n")  # Get the name
                last_disease = current_name

            if "meta" in data["graphs"][0]["nodes"][index]:  # Get the synonims
                if "synonyms" in data["graphs"][0]["nodes"][index]["meta"]:
                    for index_2, synonym in enumerate(data["graphs"][0]["nodes"][index]["meta"]["synonyms"]):
                        current_name = data["graphs"][0]["nodes"][index]["meta"]["synonyms"][index_2]["val"]
                        if current_name.startswith('obsolete'):  # Remove 'obsolete' tag
                            current_name = current_name[9:]
                        if last_disease != current_name: # Avoid writing duplicate names
                            out_file.write(current_name + "\t" + id + "\n")
                        last_disease = current_name


            #if index > 5:
            #    break
