import json

def read_config():
    print("Reading config file ")
    with open('config.json', 'r') as json_file:
        data = json.load(json_file)
    return data