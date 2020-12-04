# Standard Library Imports
import tkinter as tk

# Local Imports
import database as db

# Global Variables
book_categories = (
    ("non-fiction", lambda: "non-fiction"), 
    ("fiction", lambda: "fiction"), 
    ("textbook", lambda: "textbook"), 
    ("novel", lambda: "novel"), 
    ("short story", lambda: "short story"), 
    ("languages", lambda: "languages"), 
    ("technology", lambda: "technology"), 
    ("art", lambda: "art"), 
    ("social", lambda: "social"), 
    ("business", lambda: "business"), 
    ("programing", lambda: "programming"), 
    ("philosophy", lambda: "philosophy")
)

# ============================================================ Functionality for Searching Books ============================================================
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
