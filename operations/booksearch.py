# Local Imports
from system_data import database as db

# ===================== Functionality for Searching Books ====================
## Searching Books on Shelf ==================================================
def search_handler(search_phrase, categories=None):
    """
    PARAMETERS
        * search_phrase -> a string that is used to search for books
        * categories -> a list of selected book categories with each category being a string
    RETURN VALUES
        * a dictionary of lists with each list storing dictionaries that store information about books
    WHAT DOES THIS FUNCTION DO?
        * finds all books, in the given categories, whose title matches (or resembles) the search_phrase
    """
    search_results = get_search_results(search_phrase, categories)
    formatted_results = format_results(search_results)
    return formatted_results

def get_search_results(search_phrase, categories=None):
    """
    PARAMETERS
        * search_phrase -> a string that is used to find books
        * categories -> a list of selected book categories with each category being a string
    RETURN VALUES
        * a sorted of list of dictionaries that represent information about books
    WHAT DOES THIS FUNCTION DO?
        * this function get the raw results of a search query and returns them for formatting
    """
    search_results = db.search_books(search_phrase, categories)
    return [result[1] for result in search_results]

def format_results(search_results, page_size=5):
    """
    PARAMETERS
        * search_results -> a sorted list of dictionaries
        * page_size -> an integer that represent the number of results on a page
    RETURN VALUES
        * a dictionary of lists with each list representing a 'page' of search results
    WHAT DOES THIS FUNCTION DO?
        * This function formats a given set of search results into pages of a specified size
    """
    result_pages = dict()
    result_subsets = (search_results[i:i+page_size] for i in range(0, len(search_results), page_size))
    for i, subset in enumerate(result_subsets):
        result_pages[i] = subset
    return result_pages

## Searching Books on Loan ===================================================
def loan_search_handler(search_phrase, only_overdue=False, only_on_time=False):
    """
    PARAMETERS
        * search_phrase -> a string representing a search term
    RETURN VALUES
        * only_overdue -> a boolean value that determines whether or not only overdue books should be searched
        * only_on_time -> a boolean value that determines whether or not only books that are on time should be searched
    WHAT DOES THIS FUNCTION DO?
        * finds all the books on loan whose ID matches (or resembles) the search_phrase
    """
    search_results = db.search_books_on_loan(search_phrase, only_overdue, only_on_time)
    search_results = [result[1] for result in search_results]
    formatted_results = format_results(search_results, page_size=10)
    return formatted_results