# Standard Library Imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
import re

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from datetime import datetime as dt
from time import sleep

# Local Imports
import booksearch as bs
import bookcheckout as bc
import bookreturn as br
import bookweed as bw

# =============================================================================== MAIN WINDOW & GLOBAL VARIABLES ===============================================================================  
## Window Setup =================================================================
root = tk.Tk()
root.title('Loughborough Library Management System')
root.geometry('900x630')
root.resizable(False, False)
# root.minsize(900, 630)
# root.maxsize(1350, 945)
# root.aspect(10,7,10,7)

## Global Variables =============================================================
page_manager = dict()

# ===================================================================================== UTILITY FUNCTIONS =====================================================================================
def alert(message, is_error=True):
    if is_error:
        messagebox.showwarning(message=message)
    else:
        messagebox.showinfo(message=message)

def format_text(input_str, standard_length):
    str_len = len(input_str)
    if str_len == standard_length:
        return input_str
    elif str_len > standard_length:
        return input_str[:standard_length - 3] + "..."
    elif str_len < standard_length:
        return input_str + " "*(standard_length - str_len)

# ======================================================================================== PAGE CONTAINER ========================================================================================
## The Main Page Container ===============================================================
def build_page_container():
    page_notebook = ttk.Notebook(master=root)
    page_notebook.add(tk.Frame(), text="Home")

    books_page = build_books_page(page_notebook)
    loan_manager_page = build_loan_manager_page(page_notebook)
    analytics_page = build_analytics_page(page_notebook)
    system_info_page = build_system_info_page(page_notebook)

    page_notebook.add(books_page, text="Books")
    page_notebook.add(loan_manager_page, text="Loan Manager")
    page_notebook.add(analytics_page, text="Analytics")
    page_notebook.add(system_info_page, text="System Info")

    page_notebook.bind('<<NotebookTabChanged>>', lambda e: page_change())

    return page_notebook

# ========================================================================================= HOME PAGE =========================================================================================
## Home Page UI Components ================================================================
def build_home_page():
    home_frame = tk.Frame(master=root, height=100, width=100)
    home_frame.columnconfigure(0, weight=1, minsize=root.winfo_height())
    home_frame.rowconfigure(0, weight=1, minsize=root.winfo_width())
    home_frame.rowconfigure(1, weight=1, minsize=root.winfo_width())

    hero_section = build_hero_section(home_frame)
    button_section = build_button_section(home_frame)
    hero_section.grid(row=0, column=0, sticky="nesw")
    button_section.grid(row=1, column=0, sticky="nesw")

    return home_frame

def build_hero_section(master_frame):
    hero_section = tk.Frame(master=master_frame, bg="purple")
    hero_section.rowconfigure(0, weight=1, minsize=root.winfo_width())
    hero_section.rowconfigure(1, weight=1, minsize=root.winfo_width())
    hero_section.columnconfigure(0, weight=1, minsize=root.winfo_height())

    heading_font = tkFont.Font(family="Verdana", size=40, weight="bold")
    sub_heading_font = tkFont.Font(family="Verdana", size=20, slant="italic")

    heading = tk.Label(master=hero_section, text="Loughborough Library", font=heading_font, bg="purple", fg="white")
    sub_heading = tk.Label(master=hero_section, text=f"{dt.strftime(dt.now(), '%d %B, %Y')}", font=sub_heading_font, bg="purple", fg="white")

    heading.grid(row=0, column=0, sticky="ws", padx=20)
    sub_heading.grid(row=1, column=0, sticky="wn", padx=20)

    return hero_section

def build_button_section(master_frame):
    button_section = tk.Frame(master=master_frame, bg="purple")
    button_info = [
        ('Books', 'blue', lambda e: transition(pages_index=1)), 
        ('Loan Manager', 'green', lambda e: transition(pages_index=2)), 
        ('Analytics', 'orange', lambda e: transition(pages_index=3)), 
        ('System Info', 'grey', lambda e: transition(pages_index=4))
    ]
    button_font = tkFont.Font(family="helvetica", size=20, weight="bold", slant="italic")

    for i in range(2):
        button_section.columnconfigure(i, weight=1, minsize=25)
        button_section.rowconfigure(i, weight=1, minsize=25)
        for j in range(2):
            new_button_info = button_info[j + i * 2]
            new_button = tk.Label(button_section, text=new_button_info[0], font=button_font, bg=new_button_info[1], highlightthickness=5, fg="white", relief=tk.RAISED)
            new_button.bind('<Button-1>', new_button_info[2])
            new_button.grid(row=i, column=j, sticky="nesw")
    
    return button_section

## Home Page Functionality ================================================================
page_manager['home_page'] = build_home_page()

# ======================================================================================== BOOKS PAGE ========================================================================================
## Books Page State Variables ============================================================
books_page_state = {
    'search_var': tk.StringVar(),
    'duration_var': tk.StringVar(),
    'member_var': tk.StringVar(),
    'search_bar': None,
    'result_headings': ["id", "isbn", "title", "author", "purchase_date", "member_id"],
    'search_results': {},
    'results_section': None,
    'checkout_form': None,
    'current_page': [],
    'page_label': tk.Label(),
    'selected_categories': [],
    'checkout_books': [],
    'book_categories': (
        ("non-fiction", lambda: select_book_category("non-fiction")), 
        ("textbook", lambda: select_book_category("textbook")), 
        ("languages", lambda: select_book_category("languages")), 
        ("philosophy", lambda: select_book_category("philosophy")),
        ("technology", lambda: select_book_category("technology")),  
        ("art", lambda: select_book_category("art")), 
        ("social", lambda: select_book_category("social")), 
        ("sports", lambda: select_book_category("sports")), 
        ("biography", lambda: select_book_category("biography")), 
        ("fiction", lambda: select_book_category("fiction")), 
        ("novel", lambda: select_book_category("novel")), 
        ("short story", lambda: select_book_category("short story")), 
        ("horror", lambda: select_book_category("horror")), 
        ("fantasy", lambda: select_book_category("fantasy")), 
        ("sci-fi", lambda: select_book_category("sci-fi")), 
        ("adventure", lambda: select_book_category("adventure")), 
    )
}

books_page_state['search_var'].trace_add("write", lambda *args: book_search_handler(search_bar.get()))

## Books Page UI Components ==============================================================
def build_books_page(master_frame):
    books_page = tk.Frame(master=master_frame)
    books_page.columnconfigure(0, weight=1, minsize=10)
    books_page.rowconfigure(0, weight=1, minsize=10)
    books_page.rowconfigure(1, weight=2, minsize=10)
    books_page.rowconfigure(2, weight=0, minsize=0)
    books_page.rowconfigure(3, weight=0, minsize=10)
    books_page.rowconfigure(4, weight=8, minsize=10)

    search_section = build_search_section(books_page)
    category_section = build_category_section(books_page)

    headings = books_page_state['result_headings']
    header = build_header_row(books_page, headings)
    checkout_section = build_checkout_section(books_page)
    results_section = build_results_section(books_page)

    search_section.grid(row=0, column=0, sticky="nesw")
    category_section.grid(row=1, column=0, sticky="nesw")
    checkout_section.grid(row=2, column=0, sticky="nesw")
    checkout_section.grid_remove()
    header.grid(row=3, column=0, sticky="news", pady=0)
    results_section.grid(row=4, column=0, sticky="nesw")
    return books_page

def build_search_section(master_frame):
    global search_bar
    search_font = tkFont.Font(size=15, weight="bold")
    search_section = tk.Frame(master=master_frame, bg="#B0C4DE")
    search_bar = tk.Entry(master=search_section, textvariable=books_page_state['search_var'], bg="#1E90FF", fg="white", font=search_font)
    search_button = tk.Button(master=search_section, text="Search")
    search_bar.pack(fill=tk.BOTH, expand=3, side=tk.LEFT)
    search_button.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)

    return search_section

def build_category_section(master_frame):
    category_section = tk.Frame(master_frame, bg="#B0C4DE")

    for i in range(4):
        category_section.columnconfigure(i, weight=1, minsize=70)
        for j in range(4):
            category_section.rowconfigure(j, weight=1, minsize=30)
            index = i + 4*j
            print(index)
            new_checkbox = tk.Checkbutton(
                master=category_section, 
                text=books_page_state['book_categories'][index][0], 
                onvalue="on", 
                offvalue="off", 
                bg="#B0C4DE",
                fg="navy", 
                command=books_page_state['book_categories'][index][1]
            )
            new_checkbox.deselect()
            new_checkbox.grid(row=j, column=i, padx=0, pady=0, sticky="w")
    
    return category_section

def build_checkout_section(master_frame):
    checkout_section = tk.Frame(master=master_frame, bg="#4169E1")
    checkout_section.rowconfigure(0, weight=1, minsize=10)
    for i in range(6):
        checkout_section.columnconfigure(i, weight=1, minsize=10)

    member_label = tk.Label(master=checkout_section, text="Member ID (# from 1000-9999)", bg="#4169E1", fg="white")
    member_entry = tk.Entry(master=checkout_section,  textvariable=books_page_state['member_var'], validate="key", validatecommand=(checkout_section.register(validate_numeric_entry), '%P'))

    duration_label = tk.Label(master=checkout_section, text="Loan duration (# of days)", bg="#4169E1", fg="white")
    duration_options = tk.OptionMenu(checkout_section, books_page_state['duration_var'], *[i for i in range(1,11)])
    books_page_state['duration_var'].set(1)

    checkout_btn = tk.Button(master=checkout_section, text="Checkout Selected Books", command=book_checkout_handler)
    cancel_btn = tk.Button(master=checkout_section, text="Cancel", command=clear_selected_books)

    member_label.grid(row=0, column=0, pady=5, padx=2, sticky="e")
    member_entry.grid(row=0, column=1, pady=5, padx=2, sticky="w")
    duration_label.grid(row=0, column=2, pady=5, padx=2, sticky="e")
    duration_options.grid(row=0, column=3, pady=5, padx=2, sticky="w")
    checkout_btn.grid(row=0, column=4, pady=5, padx=2, sticky="e")
    cancel_btn.grid(row=0, column=5, pady=5, padx=2, sticky="e")

    books_page_state['checkout_form'] = checkout_section
    return checkout_section

def build_header_row(master_frame, headings):
    heading_font = tkFont.Font(weight="bold")

    header_frame = tk.Frame(master=master_frame, bg="navy", relief=tk.RAISED)
    header_frame.rowconfigure(0, weight=1, minsize=1)
    for index, heading in enumerate(headings):
        heading_label = tk.Label(master=header_frame, bg="navy", fg="white", font=heading_font)
        if heading in ("id","isbn"):
            header_frame.columnconfigure(index, weight=1, minsize=20)
            heading_label['text'] = heading.upper()
            heading_label.grid(row=0, column=index, pady=5, padx=5, sticky="ew")
        elif heading == "title":
            header_frame.columnconfigure(index, weight=10, minsize=20)
            heading_label['text'] = heading.upper()
            heading_label.grid(row=0, column=index, pady=5, padx=5, sticky="ew")
        elif heading == "purchase_date":
            header_frame.columnconfigure(index, weight=0, minsize=20)
            heading_label['anchor'] = "e"
            heading_label['text'] = "PURCHASE DATE"
            heading_label.grid(row=0, column=index, pady=5, padx=5, sticky="ew")
        elif heading == "member_id":
            header_frame.columnconfigure(index, weight=5, minsize=20)
            heading_label['text'] = "STATUS"
            heading_label.grid(row=0, column=index, pady=5, padx=5, sticky="ew")
        else:
            header_frame.columnconfigure(index, weight=2, minsize=10)
            heading_label['text'] = heading.upper()
            heading_label.grid(row=0, column=index, pady=5, padx=5, sticky="ew")
    return header_frame

def build_results_section(master_frame):
    results_section = tk.Frame(master=master_frame, bg="pink")
    results_section.rowconfigure(0, weight=1, minsize=10)
    results_section.columnconfigure(0, weight=1, minsize=10)
    
    footer_frame = tk.Frame(master=results_section, bg="navy")
    previous_button = tk.Button(footer_frame, text="Previous", command=lambda: change_book_results_page(False))
    next_button = tk.Button(footer_frame, text="Next", command=lambda: change_book_results_page(True))
    page_label = tk.Label(footer_frame, text="Page", bg="navy", fg="white")

    books_page_state['page_label'] = page_label

    previous_button.pack(fill=tk.Y, side=tk.LEFT)
    next_button.pack(fill=tk.Y, side=tk.LEFT)
    page_label.pack(fill=tk.Y, side=tk.RIGHT)

    footer_frame.pack(fill=tk.X, side=tk.BOTTOM, expand=0)
    books_page_state['results_section'] = results_section
    return results_section

def build_results_page():
    page_data = books_page_state['current_page'][1]

    page_frame = tk.Frame(master=books_page_state['results_section'], bg="#4682B4")
    page_frame.columnconfigure(0, weight=1, minsize=1)

    for i in range(5):
        page_frame.rowconfigure(i, weight=1, minsize=1)

    for i, row in enumerate(page_data):
        new_row = build_results_row(page_frame, row)
        new_row.grid(row=i, column=0, padx=5, pady=3, sticky="nesw")
    page_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=1)
    books_page_state['current_page'][2] = page_frame

def build_results_row(master_frame, row_data):
    headings = books_page_state['result_headings']

    label_font = tkFont.Font(family="monaco", size=12, weight="bold")
    status_font = tkFont.Font(family="helvetica", size=13)

    row_frame = tk.Frame(master=master_frame, bg="#87CEEB")
    row_frame.rowconfigure(0, weight=1, minsize=20)
    
    for index, heading in enumerate(headings):
        row_label = tk.Label(master=row_frame, font=label_font, bg="#B0E0E6", fg="navy")
        if heading == "id":
            row_frame.columnconfigure(index, weight=0, minsize=20)
            row_label['text'] = f"{row_data[heading]}".zfill(4)
            row_label.grid(row=0, column=index, pady=5, padx=5, sticky="w")
        elif heading == "title":
            row_frame.columnconfigure(index, weight=1, minsize=20)
            row_label['text'] = format_text(row_data[heading], 35)
            row_label.grid(row=0, column=index, pady=5, padx=5, sticky="ew")
        elif heading == "author":
            row_frame.columnconfigure(index, weight=1, minsize=20)
            row_label['text'] = format_text(row_data[heading], 20)
            row_label.grid(row=0, column=index, pady=5, padx=5, sticky="ew")
        elif heading in ("purchase_date", "isbn"):
            row_frame.columnconfigure(index, weight=0, minsize=20)
            row_label['text'] = row_data[heading]
            row_label.grid(row=0, column=index, pady=5, padx=5, sticky="w")
        elif heading == "member_id":
            row_frame.columnconfigure(index, weight=0, minsize=20)
            if row_data[heading]:
                row_label['text'] = f"Unavailable: On loan to {row_data[heading]}"
                row_label['font'] = status_font
                row_label.grid(row=0, column=index, pady=5, padx=5, sticky="e")
            else:
                row_label.destroy()
                checkout_checkbox = ttk.Checkbutton(
                    master=row_frame, 
                    text="Select book for checkout", 
                    onvalue="on", 
                    offvalue="off"
                )
                if row_data['id'] in books_page_state['checkout_books']:
                    checkout_checkbox.invoke()
                else:
                    checkout_checkbox.invoke()
                    checkout_checkbox.invoke()
                checkout_checkbox['command'] = lambda: select_for_checkout(row_data['id'])
                checkout_checkbox.grid(row=0, column=index, pady=5, padx=5, sticky="e")
        else:
            row_frame.columnconfigure(index, weight=1, minsize=20)
            row_label['text'] = row_data[heading]
            row_label.grid(row=0, column=index, pady=5, padx=5, sticky="ew")
    return row_frame

## Books Page Functionality ==============================================================
def book_search_handler(search_phrase):
    current_page = books_page_state['current_page']

    if len(current_page) == 3:
        books_page_state['current_page'][2].destroy()

    search_results = bs.search_handler(search_phrase, books_page_state['selected_categories'])
    # for key in search_results:
    #     print(f"Page {key}:", search_results[key], sep="\n")

    if search_results:
        current_page = [0, search_results[0], None]
        page_label = f"Page 1 of {len(search_results)}"
    else:
        current_page = [0, [], None]
        page_label = "Page 1 of 1"

    books_page_state['search_results'] = search_results
    books_page_state['current_page'] = current_page
    books_page_state['page_label']['text'] = page_label

    build_results_page()

def book_checkout_handler():
    loan_duration = books_page_state['duration_var'].get()
    member_id = books_page_state['member_var'].get()
    selected_books = books_page_state['checkout_books']

    if len(member_id) < 4 or int(member_id) < 1000:
        alert("Please enter a valid member ID!!!")
    else:
        try:
            member_id, loan_duration = int(member_id), int(loan_duration)
            bc.checkout_handler(member_id, selected_books, loan_duration)
            clear_selected_books()
            book_search_handler(books_page_state['search_var'].get())
            alert("Success - Book(s) have been checked out", False)
        except:
            alert("Error - Books could not be checked out")
    
def change_book_results_page(increment):
    page_num, page_data, page_frame = books_page_state['current_page']
    num_results = len(books_page_state['search_results'])

    if increment and page_num + 1 < num_results:
        new_page_num, new_search_results = page_num + 1, books_page_state['search_results'][page_num + 1]
    elif not increment and page_num - 1 >= 0:
        new_page_num, new_search_results = page_num - 1, books_page_state['search_results'][page_num - 1]
    else:
        return
    
    books_page_state['current_page'][0], books_page_state['current_page'][1] = new_page_num, new_search_results
    books_page_state['page_label']['text'] = f"Page {new_page_num + 1} of {num_results}"
    page_frame.destroy()
    build_results_page()

def select_book_category(category):
    selected_categories = books_page_state['selected_categories']

    if category in selected_categories:
        selected_categories.remove(category)
    else:
        selected_categories.append(category)

    books_page_state['selected_categories'] = selected_categories
    book_search_handler(books_page_state['search_var'].get())

def select_for_checkout(book_id):
    checkout_books = books_page_state['checkout_books']
    pre_existing_books = bool(checkout_books)

    if book_id in checkout_books:
        checkout_books.remove(book_id)
    else:
        checkout_books.append(book_id)

    if not checkout_books:
        books_page_state['checkout_form'].grid_remove()
    elif checkout_books and not pre_existing_books:
        books_page_state['checkout_form'].grid()
    
    print(checkout_books)
    books_page_state['checkout_books'] = checkout_books

def clear_selected_books():
    current_page_frame = books_page_state['current_page'][2]
    current_page_frame.destroy()
    books_page_state['checkout_books'] = []
    books_page_state['checkout_form'].grid_remove()
    books_page_state['member_var'].set('')
    books_page_state['duration_var'].set(1)
    build_results_page()

def validate_numeric_entry(val):
    return re.match('^[0-9]*$', val) is not None and len(val) < 5

# ===================================================================================== LOAN MANAGER PAGE =====================================================================================
## Loan Manager State Variables =======================================================
loan_manager_state = {
    'search_var': tk.StringVar(),
    'selector_var': tk.IntVar(),
    'show_on_time_books': False,
    'show_overdue_books': False,
    'book_headings': ['book_id', 'member_id', 'title', 'start_date', 'return_date', 'is_overdue'],
    'search_results': {},
    'results_container': None,
    'current_page': [],
    'page_label': tk.Label(),
    'return_books': [],
    'return_form': tk.Frame()
}

loan_manager_state['search_var'].trace_add('write', lambda *args: loan_book_search_handler(loan_manager_state['search_var'].get()))
loan_manager_state['selector_var'].trace_add('write', lambda *args: change_book_view())

## Loan Manager UI Components =========================================================
def build_loan_manager_page(master_frame):
    loan_manager_page = tk.Frame(master=master_frame)
    loan_manager_page.columnconfigure(0, weight=1, minsize=10)
    loan_manager_page.rowconfigure(0, weight=0, minsize=10)
    loan_manager_page.rowconfigure(1, weight=0, minsize=10)
    loan_manager_page.rowconfigure(2, weight=0, minsize=10)
    loan_manager_page.rowconfigure(3, weight=2, minsize=10)

    selector_section = build_selector_section(loan_manager_page)
    search_form = build_search_form(loan_manager_page)
    header = build_loan_header_row(loan_manager_page, loan_manager_state['book_headings'])
    results_container = build_results_container(loan_manager_page)

    selector_section.grid(row=0, column=0, sticky="nesw")
    search_form.grid(row=1, column=0, sticky="nesw")
    header.grid(row=2, column=0, sticky="nesw")
    results_container.grid(row=3, column=0, sticky="nesw")

    return loan_manager_page

def build_selector_section(master_frame):
    selector_section = tk.Frame(master=master_frame, bg="#2E8B57")
    selector_section.rowconfigure(0, weight=1, minsize=10)
    for i in range(3):
        selector_section.columnconfigure(i, weight=1, minsize=10)
    
    all_books_btn = tk.Radiobutton(master=selector_section, variable=loan_manager_state['selector_var'], text="Show All Books", value=1, bg="#2E8B57", fg="white")
    on_loan_btn = tk.Radiobutton(master=selector_section, variable=loan_manager_state['selector_var'], text="Show On-time Books", value=2, bg="#2E8B57", fg="white")
    overdue_btn = tk.Radiobutton(master=selector_section, variable=loan_manager_state['selector_var'], text="Show Overdue Books", value=3, bg="#2E8B57", fg="white")

    loan_manager_state['selector_var'].set(1)

    all_books_btn.grid(row=0, column=0, pady=10)
    on_loan_btn.grid(row=0, column=1, pady=10)
    overdue_btn.grid(row=0, column=2, pady=10)

    return selector_section

def build_search_form(master_frame):
    search_form = tk.Frame(master=master_frame, bg="#3CB371")
    search_form.rowconfigure(0, weight=1, minsize=10)
    for i in range(3):
        search_form.columnconfigure(i, weight=1, minsize=10)

    search_id_label = tk.Label(master=search_form, text="Search by Book ID", bg="#3CB371", fg="white")
    id_entry = tk.Entry(master=search_form, textvariable=loan_manager_state['search_var'], validate="key", validatecommand=(search_form.register(validate_numeric_entry), '%P'))

    return_form = build_return_form(search_form)
    loan_manager_state['return_form'] = return_form

    search_id_label.grid(row=0, column=0, sticky="e", padx=2, pady=10)
    id_entry.grid(row=0, column=1, padx=2, pady=10, sticky="w")
    return_form.grid(row=0, column=3, sticky="e", padx=2, pady=10)

    return_form.grid_remove()
    return search_form

def build_return_form(master_frame):
    return_form = tk.Frame(master=master_frame)
    return_form.rowconfigure(0, weight=1, minsize=10)
    return_form.columnconfigure(0,weight=1, minsize=10)
    return_form.columnconfigure(1,weight=1, minsize=10)

    return_btn = tk.Button(master=return_form, text="Return Selected Books", command=book_return_handler)
    cancel_btn = tk.Button(master=return_form, text="Cancel", command=clear_selected_loan_books)

    return_btn.grid(row=0, column=0, padx=2, sticky="ew")
    cancel_btn.grid(row=0, column=1, padx=2, sticky="ew")

    return return_form

def build_results_container(master_frame):
    results_container = tk.Frame(master=master_frame, bg="yellow")

    footer_frame = tk.Frame(master=results_container, bg="#004517")
    previous_button = tk.Button(footer_frame, text="Previous", command=lambda: change_loan_results_page(False))
    next_button = tk.Button(footer_frame, text="Next", command=lambda: change_loan_results_page(True))
    page_label = tk.Label(footer_frame, text="Page", bg="#004517", fg="white")

    previous_button.pack(fill=tk.Y, side=tk.LEFT)
    next_button.pack(fill=tk.Y, side=tk.LEFT)
    page_label.pack(fill=tk.Y, side=tk.RIGHT)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM, expand=0)
    
    loan_manager_state['page_label'] = page_label
    loan_manager_state['results_container'] = results_container

    return results_container

def build_loan_header_row(master_frame, headings):
    header_frame = tk.Frame(master=master_frame, bg="#004517", relief=tk.RAISED)
    header_frame.rowconfigure(0, weight=1, minsize=1)

    heading_font = tkFont.Font(weight="bold")

    for index, heading in enumerate(headings):
        heading_label = tk.Label(master=header_frame, bg="#004517", fg="white", font=heading_font)
        if heading in ("book_id","member_id"):
            header_frame.columnconfigure(index, weight=0, minsize=10)
            heading_label['text'] = " ".join(heading.split("_")).upper()
            heading_label['anchor'] = "w"
        elif heading == "title":
            header_frame.columnconfigure(index, weight=1, minsize=20)
            heading_label['text'] = heading.upper()
        elif heading in ("start_date", "return_date"):
            header_frame.columnconfigure(index, weight=0, minsize=20)
            heading_label['text'] = " ".join(heading.split("_")).upper()
            heading_label['anchor'] = "e"
        elif heading == "is_overdue":
            header_frame.columnconfigure(index, weight=0, minsize=20)
            heading_label['text'] = "STATUS"
            heading_label['anchor'] = "w"
        else:
            header_frame.columnconfigure(index, weight=2, minsize=10)
            heading_label['text'] = heading.upper()

        heading_label.grid(row=0, column=index, pady=5, padx=7, sticky="ew")
    
    header_frame.columnconfigure(len(headings), weight=1, minsize=10)
    return header_frame

def build_loan_results_page():
    page_data = loan_manager_state['current_page'][1]

    page_frame = tk.Frame(master=loan_manager_state['results_container'], bg="#228B22")
    page_frame.columnconfigure(0, weight=1, minsize=1)

    for i in range(10):
        page_frame.rowconfigure(i, weight=1, minsize=1)

    for i, row in enumerate(page_data):
        new_row = build_loan_results_row(page_frame, row)
        new_row.grid(row=i, column=0, padx=5, pady=3, sticky="nesw")
    page_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=1)
    loan_manager_state['current_page'][2] = page_frame

def build_loan_results_row(master_frame, row_data):
    headings = loan_manager_state['book_headings']

    label_font = tkFont.Font(family="monaco", size=12, weight="bold")

    row_frame = tk.Frame(master=master_frame, bg="#66CDAA")
    row_frame.rowconfigure(0, weight=1, minsize=20)

    for index, heading in enumerate(headings):
        row_label = tk.Label(master=row_frame, font=label_font, bg="#008080", fg="#7CFC00")
        if heading in ("book_id", "member_id"):
            row_frame.columnconfigure(index, weight=1, minsize=75)
            row_label['text'] = f"{row_data[heading]}".zfill(4)
        elif heading == "title":
            row_frame.columnconfigure(index, weight=0, minsize=10)
            row_label['text'] = format_text(row_data[heading], 35)
        elif heading == "is_overdue":
            row_frame.columnconfigure(index, weight=1, minsize=10)
            row_label['text'] = "Overdue" if row_data[heading] else "On time"
        else:
            row_frame.columnconfigure(index, weight=1, minsize=10)
            row_label['text'] = f"{row_data[heading]}"
        row_label.grid(row=0, column=index, pady=5, padx=5, sticky="ew")
    
    row_frame.columnconfigure(len(headings), weight=1, minsize=10)
    return_checkbox = ttk.Checkbutton(
                        master=row_frame, 
                        text="Select book for return", 
                        onvalue="on", 
                        offvalue="off"
                    )
    return_checkbox.grid(row=0, column=len(headings), pady=5, padx=5, sticky="e")

    if (row_data['log_id'], row_data['book_id']) in loan_manager_state['return_books']:
        return_checkbox.invoke()
    else:
        return_checkbox.invoke()
        return_checkbox.invoke()
    
    return_checkbox['command'] = lambda: select_for_return(row_data['log_id'], row_data['book_id'])
    
    return row_frame

## Loan Manager Functionality =========================================================
def book_return_handler():
    selected_books = loan_manager_state['return_books']
    try:
        br.return_handler(selected_books)
        clear_selected_loan_books()
        loan_book_search_handler(loan_manager_state['search_var'].get())
    except:
        print('something went wrong...')

def loan_book_search_handler(search_phrase):
    current_page = loan_manager_state['current_page']
    show_on_time_books, show_overdue_books = loan_manager_state['show_on_time_books'], loan_manager_state['show_overdue_books']

    if len(current_page) == 3:
        loan_manager_state['current_page'][2].destroy()
            
    search_results = bs.loan_search_handler(search_phrase, only_on_time=show_on_time_books, only_overdue=show_overdue_books)
    # for key in search_results:
    #     print(f"Page {key}:", search_results[key], sep="\n")

    if search_results:
        current_page = [0, search_results[0], None]
        page_label = f"Page 1 of {len(search_results)}"
    else:
        current_page = [0, [], None]
        page_label = "Page 1 of 1"

    loan_manager_state['search_results'] = search_results
    loan_manager_state['current_page'] = current_page
    loan_manager_state['page_label']['text'] = page_label

    build_loan_results_page()

def change_loan_results_page(increment):
    page_num, page_data, page_frame = loan_manager_state['current_page']
    num_results = len(loan_manager_state['search_results'])

    if increment and page_num + 1 < num_results:
        new_page_num, new_search_results = page_num + 1, loan_manager_state['search_results'][page_num + 1]
    elif not increment and page_num - 1 >= 0:
        new_page_num, new_search_results = page_num - 1, loan_manager_state['search_results'][page_num - 1]
    else:
        return

    loan_manager_state['current_page'][0], loan_manager_state['current_page'][1] = new_page_num, new_search_results
    loan_manager_state['page_label']['text'] = f"Page {new_page_num + 1} of {num_results}"
    page_frame.destroy()
    build_loan_results_page()

def change_book_view():
    selected_option = loan_manager_state['selector_var'].get()
    
    options = {1: (False, False), 2: (True, False), 3: (False, True)}
    
    loan_manager_state['show_on_time_books'], loan_manager_state['show_overdue_books'] = options[selected_option]
    loan_book_search_handler(loan_manager_state['search_var'].get())

def select_for_return(log_id, book_id):
    selected_books = loan_manager_state['return_books']
    pre_existing_books = bool(selected_books)

    if (log_id, book_id) in selected_books:
        selected_books.remove((log_id, book_id))
    else:
        selected_books.append((log_id, book_id))
    
    if not selected_books:
        loan_manager_state['return_form'].grid_remove()
    elif loan_manager_state and not pre_existing_books:
        loan_manager_state['return_form'].grid()
    
    print(selected_books)
    loan_manager_state['return_books'] = selected_books

def clear_selected_loan_books():
    current_page_frame = loan_manager_state['current_page'][2]
    current_page_frame.destroy()
    loan_manager_state['return_books'] = []
    loan_manager_state['return_form'].grid_remove()
    build_loan_results_page()

# ======================================================================================= ANALYTICS PAGE =======================================================================================
## Analytics Page State Variables =======================================================
analytics_page_state = {
    'current_figure': None,
    'figure_frame': None,
    'unused_titles': [],
    'unused_titles_page': None,
    'figure_funcs': [
        bw.display_popular_titles, 
        bw.display_least_popular_titles,
        bw.display_nonfiction_categories,
        bw.display_fiction_categories,
        bw.display_book_usage_data
    ],
    'sidebar_btn_labels': [
        ('Most Popular Titles', lambda: change_current_figure(1)),
        ('Least Popular Titles', lambda: change_current_figure(2)),
        ('Unused Titles', lambda: change_current_figure(0)),
        ('Popular Categories\n(Non-Fiction)', lambda: change_current_figure(3)),
        ('Popular Categories\n(Fiction)',lambda: change_current_figure(4)),
        ('Book Usage Over Time', lambda: change_current_figure(5))
    ],
    'data_graphs' : {
        1: None,
        2: None,
        3: None,
        4: None,
        5: None,
    }
}

## Analytics Page UI Components =========================================================
def build_analytics_page(master_frame):
    analytics_page = tk.Frame(master=master_frame)
    analytics_page.rowconfigure(0, weight=1, minsize=10)
    analytics_page.columnconfigure(0,weight=1, minsize=10)
    analytics_page.columnconfigure(1,weight=10, minsize=10)

    sidebar = build_sidebar(analytics_page)
    figure_frame = build_figure_frame(analytics_page)

    sidebar.grid(row=0, column=0, sticky="news")
    figure_frame.grid(row=0, column=1, sticky="news")

    analytics_page_state['figure_frame'] = figure_frame

    set_unused_titles()
    build_figures()
    build_unused_titles_page()
    return analytics_page

def build_sidebar(master_frame):
    sidebar = tk.Frame(master=master_frame, bg="#FF4500")
    sidebar.columnconfigure(0, weight=1, minsize=10)
    btn_labels = analytics_page_state['sidebar_btn_labels']

    for i, btn_tup in enumerate(btn_labels):
        sidebar.rowconfigure(i, weight=1, minsize=10)
        new_button = tk.Button(master=sidebar, text=btn_tup[0], command=btn_tup[1], bg="orange", fg="black")
        new_button.grid(row=i, column=0, sticky="news", padx=10, pady=10)

    return sidebar

def build_figure_frame(master_frame):
    figure_frame = tk.Frame(master=master_frame, bg="#FFFACD")
    figure_frame.rowconfigure(0, weight=1, minsize=1)
    figure_frame.columnconfigure(0, weight=1, minsize=1)
    return figure_frame

def build_figures():
    for i, figure_func in enumerate(analytics_page_state['figure_funcs']):
        graph_frame = tk.Frame(master=analytics_page_state['figure_frame'])
        new_graph = figure_func()
        new_canvas = FigureCanvasTkAgg(new_graph, master=graph_frame)
        new_canvas.draw()
        new_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        analytics_page_state['data_graphs'][i+1] = graph_frame

def display_current_figure():
    current_figure = analytics_page_state['current_figure']
    current_figure.grid(row=0, column=0, sticky="news")

def build_unused_titles_page():
    unused_titles = analytics_page_state['unused_titles']
    unused_titles_page = tk.Frame(master=analytics_page_state['figure_frame'])
    
    heading_label = tk.Label(master=unused_titles_page, text="Books with the following titles have never been checked out\nWe should consider removing them", bg="#FFFACD")

    title_listbox = tk.Listbox(master=unused_titles_page, bg="#FFFACD")
    scrollbar = tk.Scrollbar(master=unused_titles_page, bg="#FFFACD")

    for title in unused_titles:
        title_listbox.insert(tk.END, f" {title}")

    heading_label.pack(fill=tk.X, side=tk.TOP, expand=0)
    title_listbox.pack(fill=tk.BOTH, side=tk.LEFT, expand=1)
    scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=0)

    title_listbox.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = title_listbox.yview)

    analytics_page_state['unused_titles_page'] = unused_titles_page

## Analytics Page Functionality =========================================================
def change_current_figure(index):
    clear_current_figure()
    
    if index in range(1,6):
        new_figure = analytics_page_state['data_graphs'][index]
    else:
        new_figure = analytics_page_state['unused_titles_page']
    
    analytics_page_state['current_figure'] = new_figure
    display_current_figure()

def clear_current_figure():
    current_figure = analytics_page_state['current_figure']
    print(current_figure)

    if current_figure:
        current_figure.grid_remove()

def set_unused_titles():
    analytics_page_state['unused_titles'] = bw.get_unused_titles()

# ==================================================================================== SYSTEM INFO PAGES ====================================================================================
## System Info Page State Variables ==================================================
system_info_state = {
    'info_list' : [],
    'system_info_page': None,
    'current_info_box': None,
}

## System Info UI Components =========================================================
def build_system_info_page(master_frame):
    system_info_page = tk.Frame(master=master_frame, bg="grey")
    system_info_page.columnconfigure(0, weight=1, minsize=10)
    system_info_page.rowconfigure(0, weight=1, minsize=10)

    system_info_state['system_info_page'] = system_info_page

    set_system_info()

    return system_info_page

def build_info_box(master_frame):
    current_info_box = system_info_state['current_info_box']
    if current_info_box:
        current_info_box.destroy()

    info_box = tk.Frame(master=master_frame, bg="navy")
    info_box.columnconfigure(0, weight=1, minsize=10)
    info_box.rowconfigure(0, weight=1, minsize=10)

    info_list = system_info_state['info_list']
    heading_label = tk.Label(master=info_box, text="System Information")
    heading_label.grid(row=0, column=0, sticky="news")
    for i, tup in enumerate(info_list):
        info_box.rowconfigure(i+1, weight=1, minsize=10)
        new_label = tk.Label(master=info_box, text=f"{tup[0]} {tup[1]}", anchor="w")
        new_label.grid(column=0, row=i+1, sticky="news")
    
    info_box.grid(row=0, column=0)
    system_info_state['current_info_box'] = info_box

## System Info Functionality =========================================================
def set_system_info():
    system_info_state['info_list'] = bw.get_system_info()
    build_info_box(system_info_state['system_info_page'])

# ==================================================================================== MOVING BETWEEN PAGES ====================================================================================
### Assignments/function calls =======================================================
page_manager['pages_section'] = build_page_container()

def page_change():
    notebook = page_manager['pages_section']
    selected_tab = notebook.index(notebook.select())

    if selected_tab == 0:
        transition(to_home=True)
    elif selected_tab == 1:
        clear_selected_books()
        book_search_handler(books_page_state['search_var'].get())
    elif selected_tab == 2:
        clear_selected_loan_books()
        loan_book_search_handler(loan_manager_state['search_var'].get())
    elif selected_tab == 3:
        clear_current_figure()
        set_unused_titles()
        build_figures()
        build_unused_titles_page()
    elif selected_tab == 4:
        set_system_info()
    else:
        print(selected_tab)

def transition(to_home=False, pages_index=1):
    if not to_home:
        page_manager['home_page'].pack_forget()
        tab_list = page_manager['pages_section'].tabs()
        page_manager['pages_section'].select(tab_list[pages_index])
        page_manager['pages_section'].pack(fill=tk.BOTH, expand=1)
    else:
        page_manager['pages_section'].pack_forget()
        page_manager['home_page'].pack(fill=tk.BOTH, expand=1)


# ======================================================================================= FUNCTION CALLS =======================================================================================
page_manager['home_page'].pack(fill=tk.BOTH, expand=1)

book_search_handler('')
loan_book_search_handler('')

root.mainloop()
