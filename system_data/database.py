# Standard Library Imports
import json
import fileinput
from datetime import datetime as dt
from datetime import timedelta

import linecache

import os

# ============================= GLOBAL VARIABLES =============================
dir_path = os.path.dirname(os.path.realpath(__file__))
database_file = os.path.join(dir_path, "database.txt")
log_file = os.path.join(dir_path, "logfile.txt")

# =================================== BOOKS ==================================
## Getting & Updating Books from file ========================================
def get_all_books():
    """
    PARAMATERS
        * None
    RETURN VALUES
        * a list of dictionaries with each dictionary holding information about an indivdual book
    WHAT DOES THIS FUNCTION DO?
        * This function retrieves all book information in the database.txt file and returns it as a list
    """
    try:
        database = open(database_file, "r")
        return [json.loads(book) for book in database]
    except:
        print('Something went wrong...')
    database.close()

def get_book_by_id(book_id):
    """
    PARAMATERS
        * book_id -> an integer representing the unique identifier of a book
    RETURN VALUES
        * a single dictionary that holds information about a particular book
    WHAT DOES THIS FUNCTION DO?
        * This function locates the information of an indivdual book in the database and returns it
    """
    try:
        book_str = linecache.getline(database_file, book_id)
        return json.loads(book_str)
    except:
        print('something went wrong...')

def update_book(book_id, book_obj):
    """
    PARAMATERS
        * book_id -> an integer representing the unique identifier of a book
        * book_obj -> a dictionary with the newly updated information of a book
    RETURN VALUES
        * None
    WHAT DOES THIS FUNCTION DO?
        * This function locates a book in the database and updates its information
    """
    try:
        for book in fileinput.input(database_file, inplace=True):
            book_dict = json.loads(book)
            if book_dict['id'] == book_id:
                print(json.dumps(book_obj))
            else:
                print(json.dumps(book_dict))
    except:
        print('Error -- Could not update book record')

## Searching for books =======================================================
def search_books(search_phrase, categories=None):
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
    search_results = [
        result_match(book, search_phrase, categories) for book in book_index
    ]
    return sorted(
        [result for result in search_results if result != None], 
        key=lambda x: x[0]
    )

def category_match(book_index, selected_categories=None):
    """
    PARAMATERS
        * book_index -> a list of dictionaries representing all the books in the database
        * selected_categories -> a list of selected book categories
    RETURN VALUES
        * a list of dictionaries with each dictionary reprenting a book in the selected categories
    WHAT DOES THIS FUNCTION DO?
        * This function returns only the books in database to belong to a set of selected categories
    """
    if selected_categories == None:
        return book_index
    return [
        book for book in book_index if set(selected_categories).issubset(set(book['category']))
    ]

def result_match(book_obj, search_phrase, categories):
    """
    PARAMATERS
        * book_obj -> a dictionary that stores the information of a book
        * search_phrase -> a string that represents the search term used to find books
        * categories -> a list of selected book categories
    RETURN VALUES
        * a binary tuple with the first element being an integer and the second a dictionary
    WHAT DOES THIS FUNCTION DO?
        * This function assesses how closely the title of a book matches a given search term
    """
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

# =========================== LOGS & BOOKS ON LOAN ===========================
## Log Processing ============================================================
def get_all_logs(sort_by_date=False):
    """
    PARAMATERS
        * sort_by_date -> a boolean that indicates whether or not a list should be sorted
    RETURN VALUES
        * a list of dictionaries with each dictionary holding information about an indivdual log
    WHAT DOES THIS FUNCTION DO?
        * This function retrieves all log information in the logfile.txt file and returns it as a list
    """
    try:
        log_data = open(log_file, "r")
        log_index = [json.loads(log) for log in log_data]
        if sort_by_date:
            log_index.sort(
                key=lambda x: dt.strptime(x['return_date'], '%d/%m/%Y'), 
                reverse=True
            )
        return log_index
    except Exception as err:
        print('Error could retrieve log data\n', err)
    log_data.close()

def get_active_logs():
    """
    PARAMATERS
        * None
    RETURN VALUES
        * a list of dictionaries with each dictionary holding information about an indivdual log
    WHAT DOES THIS FUNCTION DO?
        * This function retrieves the log information of all books that are currently on loan
    """
    log_index = get_all_logs(True)
    return [log for log in log_index if log['book_returned'] == False]

def get_log_by_id(log_id):
    """
    PARAMATERS
        * log_id -> an integer representing the unique identifier of a book
    RETURN VALUES
        * a single dictionary that holds information about a particular log
    WHAT DOES THIS FUNCTION DO?
        * This function locates the information of an indivdual log in the logfile and returns it
    """
    try:
        log_str = linecache.getline(log_file, log_id)
        return json.loads(log_str)
    except:
        print('Error -- Could not get log of transaction')

def update_log(log_id, log_obj):
    """
    PARAMATERS
        * log_id -> an integer representing the unique identifier of a log
        * log_obj -> a dictionary with the newly updated information of a log
    RETURN VALUES
        * None
    WHAT DOES THIS FUNCTION DO?
        * This function locates a log in the logfile and updates its information
    """
    try:
        for log in fileinput.input(log_file, inplace=True):
            log_dict = json.loads(log)
            if log_dict['id'] == log_id:
                print(json.dumps(log_obj))
            else:
                print(json.dumps(log_dict))
    except:
        print('Error -- Could not update transaction log')

## Book Processing ===========================================================
def get_books_on_loan():
    """
    PARAMATERS
        * None
    RETURN VALUES
        * a list of dictionaries with each dictionary holding the relevant information of a book on loan
    WHAT DOES THIS FUNCTION DO?
        * This function finds all books that are on loan and categorises them as either on-time or overdue
    """
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
    """
    PARAMATERS
        * book_id -> an integer representing the unique identifier of a book
        * only_overdue -> a boolean value that determines whether or not only overdue books should be searched
        * only_on_time -> a boolean value that determines whether or not only on time books should be searched
    RETURN VALUES
        * a list of tuples with each tuple reprenting a search result and its rank
    WHAT DOES THIS FUNCTION DO?
        * finds all the books on loan whose ID matches (or resembles) the book_id 
    """
    all_books_on_loan = get_books_on_loan()
    if only_overdue:
        search_results = [match_result(book_id, book) for book in all_books_on_loan if is_book_overdue(book)]
    elif only_on_time:
        search_results = [match_result(book_id, book) for book in all_books_on_loan if not is_book_overdue(book)]
    else:
        search_results = [match_result(book_id, book) for book in all_books_on_loan]
    
    return sorted([result for result in search_results if result != None], key=lambda x: x[0])

def match_result(book_id, book_obj):
    """
    PARAMATERS
        * book_id -> an integer representing the unique identifier of a book
        * book_obj -> a dictionary that stores the information of a book
    RETURN VALUES
        * a binary tuple with the first element being an integer and the second a dictionary
    WHAT DOES THIS FUNCTION DO?
        * This function assesses how closely the id of a book matches a given book id search term
    """
    id_string = f"{str(book_obj['book_id']).strip()}".zfill(4)

    if book_id == '':
        return (1, book_obj)
    elif int(book_id) == book_obj['book_id']:
        return (1, book_obj)
    elif len(book_id) <= len(id_string) and book_id[:len(book_id)] == id_string[:len(book_id)]:
        return (2, book_obj)

def is_book_overdue(log):
    """
    PARAMATERS
        * log -> a dictionary that holds information about a log
    RETURN VALUES
        * a boolean value indicating whether a book is overdue
    WHAT DOES THIS FUNCTION DO?
        * This function uses log information to determine whether a not a book is overdue
    """
    present_day = dt.combine(dt.now(), dt.max.time())
    return_date = dt.combine(dt.strptime(log['return_date'], '%d/%m/%Y'), dt.max.time())
    return return_date < present_day

# ============================ CHECKOUTS & RETURN ============================
## Checkout ==================================================================
def checkout_book(book_id, member_id, loan_duration):
    """
    PARAMATERS
        * book_id -> an integer representing the unique identifier of a book
        * member_id -> a four digit integer representing the unique identifier of a member
        * loan_duration -> an integer representing the number of days a book will be loaned out for
    RETURN VALUES
        * None
    WHAT DOES THIS FUNCTION DO?
        * This function handles all the file operations associated with checking out a book
    """
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
    """
    PARAMATERS
        * loan_duration -> an integer representing the number of days a book will be loaned out for
    RETURN VALUES
        * a string that represents a date in the future
    WHAT DOES THIS FUNCTION DO?
        * This function determines the return date for a book that has been loaned out
    """
    present_day = dt.combine(dt.now(), dt.max.time())
    return_date = present_day + timedelta(days=loan_duration)
    return dt.strftime(return_date, '%d/%m/%Y')

def write_log(log):
    """
    PARAMATERS
        * log -> a dictionary that holds information about a log
    RETURN VALUES
        * None
    WHAT DOES THIS FUNCTION DO?
        * This function writes a new log to the logfile when a book has been checked out
    """
    with open(log_file, 'a') as log_file_handler:
        log_file_handler.write(json.dumps(log) + "\n")

## Return ====================================================================
def return_book(log_id, book_id):
    """
    PARAMATERS
        * log_id -> an integer representing the unique identifier of a log
        * book_id -> an integer representing the unique identifier of a book
    RETURN VALUES
        * None
    WHAT DOES THIS FUNCTION DO?
        * This function handles all the file operations associated with returning a book
    """
    log_obj, book_obj = get_log_by_id(log_id), get_book_by_id(book_id)
    log_obj['book_returned'] = True
    book_obj['member_id'] = None
    update_book(book_obj['id'], book_obj)
    update_log(log_obj['id'], log_obj)

# ================================= ANALYTICS ================================
## Book Title Data ===========================================================
def get_all_titles():
    """
    PARAMATERS
        * None
    RETURN VALUES
        * a list of strings representing book titles
    WHAT DOES THIS FUNCTION DO?
        * This function retrieves all the unique book titles from the database
    """
    unique_titles = list({ book['title'] for book in get_all_books() })
    return unique_titles

def get_used_titles():
    """
    PARAMATERS
        * None
    RETURN VALUES
        * a list of strings representing book titles
    WHAT DOES THIS FUNCTION DO?
        * This function retrieves the unique titles of books that have been checked out
    """
    used_titles = list({ get_book_by_id(log['book_id'])['title'] for log in get_all_logs() })
    return used_titles

def get_unused_titles():
    """
    PARAMATERS
        * None
    RETURN VALUES
        * a list of strings representing book titles
    WHAT DOES THIS FUNCTION DO?
        * This function retrieves the unique titles of books that have never been checked out
    """
    unused_set = set.difference(set(get_all_titles()), set(get_used_titles()))
    return list(unused_set)

def get_title_usage():
    """
    PARAMATERS
        * None
    RETURN VALUES
        * a list of tuples with the first element being a string and the second an integer
    WHAT DOES THIS FUNCTION DO?
        * This function gets all the titles of books that have been checked out and the number checkouts associated with that title
    """
    books_titles = [get_book_by_id(log['book_id'])['title'] for log in get_all_logs()]
    title_usage = [(book, books_titles.count(book)) for book in get_used_titles()]
    return sorted(title_usage, key=lambda x: x[1], reverse=True)

## Book Category Data ========================================
def get_category_usage_data(main_category, sub_categories):
    """
    PARAMATERS
        * main_category -> a string representing the main search parameter for finding book titles
        * sub_categories -> a list of strings that represent sub-categories of the main_category
    RETURN VALUES
        * a list of tuples with the first element being a string and the second an integer
    WHAT DOES THIS FUNCTION DO?
        * This function finds the number of checkouts associated with selected book categories
    """
    data_list = []
    for category in sub_categories:
        usage_count = 0
        log_gen = (log for log in get_all_logs())
        for log in log_gen:
            book_categories = get_book_by_id(log['book_id'])['category']
            if main_category in book_categories and category in book_categories:
                usage_count += 1
        data_list.append((category, usage_count))
    return data_list

## Book Usage Data ===========================================
def get_book_usage_data():
    """
    PARAMATERS
        * None
    RETURN VALUES
        * a list of tuples with the first element being a string and the second an integer
    WHAT DOES THIS FUNCTION DO?
        * This function finds the number of checkouts associated with all used book titles
    """
    book_years = [log['start_date'].split('/')[-1] for log in get_all_logs()]
    book_usage = [(year, book_years.count(year)) for year in set(book_years)]
    return sorted(book_usage, key=lambda x: x[0])

# ================================== TESTING ==================================
def book_status():
    """
    PARAMATERS
        * None
    RETURN VALUES
        * None
    WHAT DOES THIS FUNCTION DO?
        * Tests that all books, books on loan and overdue books can be loaded properly
    """
    try:
        all_books = get_all_books()
        on_loan_books = get_books_on_loan()
        overdue_books = [book for book in on_loan_books if book['is_overdue']]
        on_time_books = [book for book in on_loan_books if not book['is_overdue']]
        print(f"\nBooks successfully loaded. Test passed.")
        print("--- STATUS OF BOOKS ---")
        print(f"Total Books: {len(all_books)}")
        print(f"Books on loan: {len(on_loan_books)}")
        print(f"Books on time: {len(on_time_books)}")
        print(f"Books on overdue: {len(overdue_books)}")
    except:
        print("Error -- Could not load books")

def title_status():
    """
    PARAMATERS
        * None
    RETURN VALUES
        * None
    WHAT DOES THIS FUNCTION DO?
        * Tests that book titles, used titles and unused titles can be loaded properly
    """
    try:
        all_titles = get_all_titles()
        used_titles = get_used_titles()
        unused_titles = get_unused_titles()
        print(f"\nBook titles successfully loaded. Test passed.")
        print("--- STATUS OF UNIQUE BOOK TITLES ---")
        print(f"Used titles: {len(used_titles)}")
        print(f"Unused titles {len(unused_titles)}")
        print(f"Total titles: {len(all_titles)}")
    except:
        print("Error -- Could not retrieve book titles")

def run_tests():
    """
    PARAMATERS
        * None
    RETURN VALUES
        * None
    WHAT DOES THIS FUNCTION DO?
        * Tests the main functionality aspects of this module
    """
    print("--- Running Tests for database.py ---")
    book_status()
    title_status()

if __name__ == "__main__":
    run_tests()