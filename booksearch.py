# Standard Library Imports
import tkinter as tk

# Local Imports
from database import search_books

# Global Variables
book_categories = ("non-fiction", "fiction", "textbook", "novel", "short story", "languages", "technology", "art", "social", "business", "programing", "philosophy")

# ============================================================ Functionality for Searching Books ============================================================
def get_search_results(search_phrase, categories=None):
    search_results = search_books(search_phrase, categories)
    return [result[1] for result in search_results]