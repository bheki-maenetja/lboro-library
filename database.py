# Standard Library Imports
import json
import fileinput

from random import choice

# Index View
## GET
def get_all_books():
    try:
        database = open("database.txt", "r")
        return [json.loads(book) for book in database]
    except:
        print('Something went wrong...')
    database.close()

def search_books(search_phrase, categories=None):
    book_index = category_match(get_all_books(), categories)
    search_results = [result_match(book, search_phrase, categories) for book in book_index]
    return sorted([result for result in search_results if result != None], key=lambda x: x[0])

def category_match(book_index, selected_categories=None):
    if selected_categories == None:
        return book_index
    return [book for book in book_index if set(selected_categories).issubset(set(book['category']))]

def result_match(book_obj, search_phrase, categories):
    book_title = book_obj['title'].lower()
    search_phrase = search_phrase.lower()
    
    if search_phrase == '':
        return (1, book_obj)
    elif book_title == search_phrase:
        return (1, book_obj)
    elif book_title in search_phrase or search_phrase in book_title:
        return (2, book_obj)
    elif len(search_phrase) >= 3 and search_phrase[:3] == book_title[:3]:
        return (3, book_obj)

# Single View
## GET
def get_book_by_id(book_id):
    try:
        database = open("database.txt", "r")
        for book in database:
            if json.loads(book)['id'] == book_id:
                return json.loads(book)
        return None
    except:
        print('something went wrong...')

## PUT
def update_book(book_id, book_obj):
    try:
        for book in fileinput.input("database.txt", inplace=True):
            book_dict = json.loads(book)
            if book_dict['id'] == book_id:
                print(json.dumps(book_obj))
            else:
                print(json.dumps(book_dict))
    except:
        print('something went wrong...')

print(search_books('programming', categories=['textbook', 'technology']))



