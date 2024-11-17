import json


def openJsonFile(file):
    with open(file,'r') as json_file:
        data_file = json.load(json_file)

    return data_file
