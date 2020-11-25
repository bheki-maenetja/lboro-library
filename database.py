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

def get_book(book_id):
    try:
        database = open("database.txt", "r")
        for book in database:
            if json.loads(book)['id'] == book_id:
                return json.loads(book)
        return None
    except:
        print('something went wrong...')


print(get_book(int(input("Enter a number: "))))



