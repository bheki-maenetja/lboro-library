# Standard Library Imports
import tkinter as tk

# Local Imports
from database import search_books

book_categories = ("non-fiction", "fiction", "textbook", "novel", "short story", "languages", "technology", "art", "social", "business", "programing", "philosophy")

# ============================================================ Functionality Components for Searching Books ============================================================
def search_function(widget):
    print(widget.get())
    string_var = tk.StringVar()
    widget['textvariable'] = string_var
    string_var.trace_add("write", lambda: print("I'm typing something..."))