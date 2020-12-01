# Standard Library Imports
import tkinter as tk

book_categories = ("non-fiction", "fiction", "textbook", "novel", "short story", "languages", "technology", "art", "social", "business", "programing", "philosophy")
# UI Components for Searching Books
def build_books_page(master_frame):
    books_page = tk.Frame(master=master_frame)
    books_page.columnconfigure(0, weight=1, minsize=10)
    books_page.rowconfigure(0, weight=1, minsize=10)
    books_page.rowconfigure(1, weight=1, minsize=10)
    books_page.rowconfigure(2, weight=1, minsize=10)

    category_section = build_category_section(books_page)
    search_section = build_search_section(books_page)
    search_section.grid(row=0, column=0, sticky="nsew")
    category_section.grid(row=1, column=0, sticky="new")
    return books_page

def build_category_section(master_frame):
    category_section = tk.Frame(master_frame, bg="grey")

    for i in range(4):
        category_section.columnconfigure(i, weight=1, minsize=70)
        for j in range(3):
            category_section.rowconfigure(j, weight=1, minsize=30)
            index = i + 4*j
            new_checkbox = tk.Checkbutton(master=category_section, text=book_categories[index], onvalue="on", offvalue="off", bg="green")
            new_checkbox.deselect()
            new_checkbox.grid(row=j, column=i, padx=0, pady=0, sticky="w")
    
    return category_section

def build_search_section(master_frame):
    search_section = tk.Frame(master=master_frame, bg="darkgrey")
    search_bar = tk.Entry(master=search_section)
    search_button = tk.Button(master=search_section, text="Search")
    search_bar.pack(fill=tk.X, expand=3, side=tk.LEFT)
    search_button.pack(fill=tk.X, expand=1, side=tk.LEFT)

    return search_section

# Functionality Components for Searching Books