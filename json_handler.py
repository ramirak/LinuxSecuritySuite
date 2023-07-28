import json

def retrieve_from_file(file_name):
    with open(file_name) as my_json:
        data = json.load(my_json)
        return data

def save_to_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write(json.dumps(data))


def list_to_json(keys, values):
    my_dict = dict(zip(keys, values))
    return my_dict#json.dumps(my_dict)


def replace_val_from_key(key, value, file_name):
    data = None
    if key !=  None:
        data = retrieve_from_file(file_name)    
        data[key] = value
    else:
        data = value
    save_to_file(file_name, data)


