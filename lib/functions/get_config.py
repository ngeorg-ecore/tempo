import json


def get_config():
    with open("config/user.json", "r") as jsonfile:
        file = json.load(jsonfile)
        return file

