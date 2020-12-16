# Local Imports
from system_data import database as db

# ============================================================================= Functionality for Searching Books =============================================================================
## Searching Books on Shelf ===================================================
def search_handler(search_phrase, categories=None):
    search_results = get_search_results(search_phrase, categories)
    formatted_results = format_results(search_results)
    return formatted_results

def get_search_results(search_phrase, categories=None):
    search_results = db.search_books(search_phrase, categories)
    return [result[1] for result in search_results]

def format_results(search_results, page_size=5):
    result_pages = dict()
    result_subsets = (search_results[i:i+page_size] for i in range(0, len(search_results), page_size))
    for i, subset in enumerate(result_subsets):
        result_pages[i] = subset
    return result_pages

## Searching Books on Loan ====================================================
def loan_search_handler(search_phrase, only_overdue=False, only_on_time=False):
    search_results = db.search_books_on_loan(search_phrase, only_overdue, only_on_time)
    search_results = [result[1] for result in search_results]
    formatted_results = format_results(search_results, page_size=10)
    return formatted_results