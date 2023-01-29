import os
from pyairtable import Table

# Get secret variables
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE = os.getenv('AIRTABLE_BASE')

def get_strings(reco):
    try:
        table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE, 'strings')
        fields = table.all(sort=["id"])[reco - 1]["fields"]
    except:
        print("could not access database, please check api key and base name")
        print(AIRTABLE_API_KEY)
        return None

    strings = {}
    try:
        for i in range(3):  # number of recommendations
            prefix = "string_" + str(i + 1)
            strings[prefix] = {
                "name": fields[prefix + "_name"][0],
                "price": fields[prefix + "_price"][0],
                "image": fields[prefix + "_image"][0]["url"],
                "description": fields[prefix + "_description"][0],
            }
    except KeyError:
        print(
            "key error when accessing data base, sending a slack message...\n",
            fields)
        return None

    return strings