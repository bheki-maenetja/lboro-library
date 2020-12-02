# Standard Library Imports
import tkinter as tk

# Local Imports
from database import search_books

book_categories = ("non-fiction", "fiction", "textbook", "novel", "short story", "languages", "technology", "art", "social", "business", "programing", "philosophy")

sample_books = search_books('', categories=['fiction'])
# ============================================================ UI Components for Searching Books ============================================================
## Books Page
def build_books_page(master_frame):
    books_page = tk.Frame(master=master_frame)
    books_page.columnconfigure(0, weight=1, minsize=10)
    books_page.rowconfigure(0, weight=1, minsize=10)
    books_page.rowconfigure(1, weight=1, minsize=10)
    books_page.rowconfigure(2, weight=1, minsize=10)
    books_page.rowconfigure(3, weight=4, minsize=10)

    search_section = build_search_section(books_page)
    category_section = build_category_section(books_page)

    headings = list(sample_books[0][1].keys())
    headings.remove('category')
    header = build_row(books_page, headings, is_header=True)
    results_section = build_results_section(books_page, headings)

    search_section.grid(row=0, column=0, sticky="nesw")
    category_section.grid(row=1, column=0, sticky="nesw")
    header.grid(row=2, column=0, sticky="ew")
    results_section.grid(row=3, column=0, sticky="nesw")
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

    search_bar.bind('<FocusIn>', lambda e: search_function(e.widget))
    return search_section

def build_results_section(master_frame, headings):
    results_section = tk.Frame(master=master_frame, bg="pink")
    results_section.rowconfigure(0, weight=1, minsize=10)
    results_section.columnconfigure(0, weight=1, minsize=10)

    canvas = tk.Canvas(results_section, bg="green")
    scrollable_frame = tk.Frame(canvas, bg="yellow")
    scrollbar = tk.Scrollbar(results_section, orient="vertical", command=canvas.yview)

    scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.itemconfigure(scrollable_frame_id, width=e.width))

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollable_frame.columnconfigure(0, weight=1, minsize=1)
    for i in range(100):
        scrollable_frame.rowconfigure(i, weight=1, minsize=1)
        new_row = build_row(scrollable_frame, headings)
        new_row.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
    
    canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=1)
    scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=0)
    
    return results_section
    
def build_row(master_frame, headings, is_header=False, row_data=sample_books[0][1]):
    if is_header:
        header_frame = tk.Frame(master=master_frame, bg="red", relief=tk.RAISED)
        header_frame.rowconfigure(0, weight=1, minsize=1)
        for index, heading in enumerate(headings):
            header_frame.columnconfigure(index, weight=1, minsize=10)
            heading_label = tk.Label(master=header_frame, text=heading.upper())
            heading_label.grid(row=0, column=index, pady=5)
        return header_frame
    elif row_data:
        row_frame = tk.Frame(master=master_frame, bg="blue")
        row_frame.rowconfigure(0, weight=1, minsize=10)
        for index, heading in enumerate(headings):
            row_frame.columnconfigure(index, weight=1, minsize=10)
            row_label = tk.Label(master=row_frame, text=row_data[heading])
            row_label.grid(row=0, column=index, pady=5, padx=5, sticky="w")
        return row_frame

# ============================================================ Functionality Components for Searching Books ============================================================
def search_function(widget):
    print(widget.get())
    string_var = tk.StringVar()
    widget['textvariable'] = string_var
    string_var.trace_add("write", lambda: print("I'm typing something..."))