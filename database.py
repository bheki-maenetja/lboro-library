# Standard Library Imports
import json
import re

from random import choice

# Loading files

# Get Index
def get_all_books():
    try:
        database = open("database.txt", "r")
        return [json.loads(book) for book in database]
    except:
        print('Something went wrong...')
    database.close()

print(get_all_books())



