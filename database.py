# Standard Library Imports
import json
import fileinput
import datetime as dt

# ==================== BOOKS ====================
# Index View
## GET
def get_all_books(): # return all books in the database
    try:
        database = open("database.txt", "r")
        return [json.loads(book) for book in database]
    except:
        print('Something went wrong...')
    database.close()

def search_books(search_phrase, categories=None): # returns books based on search parameters
    book_index = category_match(get_all_books(), categories)
    search_results = [result_match(book, search_phrase, categories) for book in book_index]
    return sorted([result for result in search_results if result != None], key=lambda x: x[0])

def category_match(book_index, selected_categories=None): # filters books based on selected categories
    if selected_categories == None:
        return book_index
    return [book for book in book_index if set(selected_categories).issubset(set(book['category']))]

def result_match(book_obj, search_phrase, categories): # filters books based on search string
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
def get_book_by_id(book_id): # returns a book based on its id
    try:
        database = open("database.txt", "r")
        for book in database:
            if json.loads(book)['id'] == book_id:
                return json.loads(book)
        return None
    except:
        print('something went wrong...')

## PUT
def update_book(book_id, book_obj): # updates a book
    try:
        for book in fileinput.input("database.txt", inplace=True):
            book_dict = json.loads(book)
            if book_dict['id'] == book_id:
                print(json.dumps(book_obj))
            else:
                print(json.dumps(book_dict))
    except:
        print('something went wrong...')

# ==================== LOGS ====================
# Index View
## GET
def get_all_logs(sort_by_date=False):
    try:
        log_data = open("logfile.txt", "r")
        log_index = [json.loads(log) for log in log_data]
        if sort_by_date:
            log_index.sort(key=lambda x: dt.datetime.strptime(x['return_date'], '%d/%m/%Y'), reverse=True)
        return log_index
    except:
        print('Something went wrong...')
    log_data.close()

for i in get_all_logs(True):
    print(i)
