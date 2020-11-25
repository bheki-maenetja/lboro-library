# Standard Library Imports
import json
import fileinput

from random import choice

# Loading files

# GET
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

def update_book(book_id, book_obj):
    try:
        database = open("database.txt", "w")
        for book in fileinput.input(database):
            book_dict = json.loads(book)
            if book_dict['id'] == book_id:
                print(json.dumps(book_obj))
            else:
                print(json.dumps(book_dict))
    except:
        print('something went wrong...')

update_book(1, {'name': 'Scooby-doo', 'id' : 1})



