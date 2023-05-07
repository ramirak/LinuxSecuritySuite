import json

def retrieve_from_file(file_name):
    # Opening profiles JSON file
    with open(file_name) as my_json:
        data = json.load(my_json)
        return data



