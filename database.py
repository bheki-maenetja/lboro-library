# Standard Library Imports
import json
import fileinput
from datetime import datetime as dt
from datetime import timedelta

import linecache
# ============================================================ BOOKS ============================================================
## Getting & Updating Books from file ========================
def get_all_books(): # return all books in the database
    try:
        database = open("database.txt", "r")
        return [json.loads(book) for book in database]
    except:
        print('Something went wrong...')
    database.close()

def get_book_by_id(book_id): # returns a book based on its id
    try:
        book_str = linecache.getline("database.txt", book_id)
        return json.loads(book_str)
    except:
        print('something went wrong...')
    # database.close()

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

## Searching for books =======================================
def search_books(search_phrase, categories=None): # returns books based on search parameters
    """
    PARAMETERS:
        * search_phrase -> a string that is used to find books
        * categories -> a list of selected book categories with each category being a string
    RETURN VALUES
        * search_results -> a sorted list of binary tuples with the first element being an integer and second element being a dictinary
    WHAT DOES THIS FUNCTION DO?
        * finds all the books in the database, in the given categories, whose title matches (or resembles) the search_phrase   
    """
    book_index = category_match(get_all_books(), categories)
    search_results = [result_match(book, search_phrase, categories) for book in book_index]
    return sorted([result for result in search_results if result != None], key=lambda x: x[0])

def category_match(book_index, selected_categories=None): # filters books based on selected categories
    if selected_categories == None:
        return book_index
    return [book for book in book_index if set(selected_categories).issubset(set(book['category']))]

def result_match(book_obj, search_phrase, categories): # filters books based on search string
    book_title = book_obj['title'].lower().strip()
    search_phrase = search_phrase.lower().strip()
    
    if search_phrase == '':
        return (1, book_obj)
    elif book_title == search_phrase:
        return (1, book_obj)
    elif len(search_phrase) <= len(book_title) and search_phrase[:len(search_phrase)] == book_title[:len(search_phrase)]:
        return (2, book_obj)
    elif book_title in search_phrase or search_phrase in book_title:
        return (3, book_obj)

# ============================================================ LOGS & BOOKS ON LOAN ============================================================
## Log Processing ============================================
def get_all_logs(sort_by_date=False):
    try:
        log_data = open("logfile.txt", "r")
        log_index = [json.loads(log) for log in log_data]
        if sort_by_date:
            log_index.sort(key=lambda x: dt.strptime(x['return_date'], '%d/%m/%Y'), reverse=True)
        return log_index
    except Exception as err:
        print('Something went wrong...\n', err)
    log_data.close()

def get_active_logs():
    log_index = get_all_logs(True)
    return [log for log in log_index if log['book_returned'] == False]

def get_log_by_id(log_id):
    try:
        log_str = linecache.getline("logfile.txt", log_id)
        return json.loads(log_str)
    except:
        print('something went wrong...')

def update_log(log_id, log_obj):
    try:
        for log in fileinput.input("logfile.txt", inplace=True):
            log_dict = json.loads(log)
            if log_dict['id'] == log_id:
                print(json.dumps(log_obj))
            else:
                print(json.dumps(log_dict))
    except:
        print('something went wrong...')

## Book Processing ==========================================
def get_books_on_loan():
    books_on_loan = []
    active_logs = get_active_logs()
    for log in active_logs:
        new_obj = {
            'log_id': log['id'],
            'book_id': get_book_by_id(log['book_id'])['id'],
            'member_id': log['member_id'],
            'title': get_book_by_id(log['book_id'])['title'],
            'start_date': log['start_date'],
            'return_date': log['return_date'],
            'is_overdue': is_book_overdue(log)
        }

        books_on_loan.append(new_obj)

    return books_on_loan

def search_books_on_loan(book_id, only_overdue=False, only_on_time=False):
    all_books_on_loan = get_books_on_loan()
    if only_overdue:
        search_results = [match_result(book_id, book) for book in all_books_on_loan if is_book_overdue(book)]
    elif only_on_time:
        search_results = [match_result(book_id, book) for book in all_books_on_loan if not is_book_overdue(book)]
    else:
        search_results = [match_result(book_id, book) for book in all_books_on_loan]
    
    return sorted([result for result in search_results if result != None], key=lambda x: x[0])

def match_result(book_id, book_obj):
    id_string = f"{str(book_obj['book_id']).strip()}".zfill(4)

    if book_id == '':
        return (1, book_obj)
    elif int(book_id) == book_obj['book_id']:
        return (1, book_obj)
    elif len(book_id) <= len(id_string) and book_id[:len(book_id)] == id_string[:len(book_id)]:
        return (2, book_obj)

def is_book_overdue(log):
    present_day = dt.combine(dt.now(), dt.max.time())
    return_date = dt.combine(dt.strptime(log['return_date'], '%d/%m/%Y'), dt.max.time())
    return return_date < present_day

# ============================================================ CHECKOUT & RETURN ============================================================
## Checkout ==================================================
def checkout_book(book_id, member_id, loan_duration):
    book_obj = get_book_by_id(book_id)
    log_obj = dict()

    book_obj['member_id'] = member_id

    log_obj['id'] = len(get_all_logs()) + 1
    log_obj['book_id'] = book_id
    log_obj['member_id'] = member_id
    log_obj['start_date'] = dt.strftime(dt.now(), '%d/%m/%Y')
    log_obj['return_date'] = get_return_date(loan_duration)
    log_obj['book_returned'] = False

    update_book(book_id, book_obj)
    write_log(log_obj)

def get_return_date(loan_duration):
    present_day = dt.combine(dt.now(), dt.max.time())
    return_date = present_day + timedelta(days=loan_duration)
    return dt.strftime(return_date, '%d/%m/%Y')

def write_log(log):
    with open('logfile.txt', 'a') as log_file:
        log_file.write(json.dumps(log) + "\n")

## Return ====================================================
def return_book(log_id, book_id):
    log_obj, book_obj = get_log_by_id(log_id), get_book_by_id(book_id)
    log_obj['book_returned'] = True
    book_obj['member_id'] = None
    update_book(book_obj['id'], book_obj)
    update_log(log_obj['id'], log_obj)

# ============================================================ ANALYTICS ============================================================
def get_title_usage():
    books_titles = [get_book_by_id(log['book_id'])['title'] for log in get_all_logs()]
    book_title_set = set(books_titles)
    title_usage = ((book, books_titles.count(book)) for book in book_title_set)
    for data in title_usage:
        print(data)

# ============================================================ UTILITY FUNCTIONS ============================================================
def book_status():
    books = get_books_on_loan()
    overdue_books = [book for book in books if book['is_overdue']]
    on_time_books = [book for book in books if not book['is_overdue']]
    input("Books on loan >>> ")
    for i in on_time_books:
        print(i)
    input("Overdue Books >>> ")
    for i in overdue_books:
        print(i)

get_title_usage()
# book_status()
# input("returning book >>> ")
# loan_obj = get_loan_object()
# return_book(loan_obj['on-loan'][0])
# book_status()