# Standard Library Imports
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from datetime import datetime as dt

# Local Imports
import booksearch as bs

# =============================================================================== MAIN WINDOW & GLOBAL VARIABLES ===============================================================================  
## Window Setup =================================================================
root = tk.Tk()
root.title('Loughborough Library Management System')
root.geometry('900x630')
root.minsize(600, 420)
root.maxsize(1350, 945)
root.aspect(10,7,10,7)

## Global & State Variables =====================================================
page_manager = dict()

books_page_state = {
    'search_var': tk.StringVar(),
    'search_bar': None,
    'result_headings': ["id", "isbn", "title", "author", "purchase_date", "language", "member_id"],
    'search_results': {},
    'results_section': None,
    'current_page': [],
    'page_label': None,
    'selected_categories': [],
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

# ======================================================================================== UPDATING UI ========================================================================================
## Updating UI Components ================================================================
def book_search_handler(search_phrase):
    current_page = books_page_state['current_page']

    if len(current_page) == 3:
        books_page_state['current_page'][2].destroy()

    search_results = bs.search_handler(search_phrase, books_page_state['selected_categories'])
    for key in search_results:
        print(f"Page {key}:", search_results[key], sep="\n")

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

def build_header_row(master_frame, headings, is_header=False):
    header_frame = tk.Frame(master=master_frame, bg="red", relief=tk.RAISED)
    header_frame.rowconfigure(0, weight=1, minsize=1)
    for index, heading in enumerate(headings):
        header_frame.columnconfigure(index, weight=1, minsize=10)
        heading_label = tk.Label(master=header_frame, text=heading.upper())
        heading_label.grid(row=0, column=index, pady=5)
    return header_frame

def build_results_page():
    page_data = books_page_state['current_page'][1]

    page_frame = tk.Frame(master=books_page_state['results_section'], bg="yellow")
    page_frame.columnconfigure(0, weight=1, minsize=1)
    for i, row in enumerate(page_data):
        page_frame.rowconfigure(i, weight=1, minsize=1)
        new_row = build_results_row(page_frame, row)
        new_row.grid(row=i, column=0, padx=5, pady=3, sticky="nesw")
    page_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=1)
    books_page_state['current_page'][2] = page_frame
    
def build_results_row(master_frame, row_data):
    headings = books_page_state['result_headings']

    row_frame = tk.Frame(master=master_frame, bg="blue")
    row_frame.rowconfigure(0, weight=1, minsize=10)
    for index, heading in enumerate(headings):
        row_frame.columnconfigure(index, weight=1, minsize=10)
        row_label = tk.Label(master=row_frame, text=row_data[heading])
        row_label.grid(row=0, column=index, pady=5, padx=5, sticky="w")
    return row_frame

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

# ========================================================================================= HOME PAGE =========================================================================================
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
    button_section = tk.Frame(master=master_frame, bg="grey")
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

page_manager['home_page'] = build_home_page()

# ======================================================================================== OTHER PAGES ========================================================================================
## The Main Page Container ===============================================================
def build_page_container():
    page_notebook = ttk.Notebook(master=root)
    page_notebook.add(tk.Frame(), text="Home")

    books_page = build_books_page(page_notebook)

    page_notebook.add(books_page, text="Books")
    page_notebook.add(tk.Frame(master=page_notebook, bg="green"), text="Loan Manager")
    page_notebook.add(tk.Frame(master=page_notebook, bg="orange"), text="Analytics")
    page_notebook.add(tk.Frame(master=page_notebook, bg="grey"), text="System Info")

    page_notebook.bind('<<NotebookTabChanged>>', lambda e: go_to_home_page(e))

    return page_notebook

## Books Page ============================================================================
def build_books_page(master_frame):
    books_page = tk.Frame(master=master_frame)
    books_page.columnconfigure(0, weight=1, minsize=10)
    books_page.rowconfigure(0, weight=1, minsize=10)
    books_page.rowconfigure(1, weight=2, minsize=10)
    books_page.rowconfigure(2, weight=0, minsize=10)
    books_page.rowconfigure(3, weight=8, minsize=10)

    search_section = build_search_section(books_page)
    category_section = build_category_section(books_page)

    headings = books_page_state['result_headings']
    header = build_header_row(books_page, headings, is_header=True)
    results_section = build_results_section(books_page)

    search_section.grid(row=0, column=0, sticky="nesw")
    category_section.grid(row=1, column=0, sticky="nesw")
    header.grid(row=2, column=0, sticky="news", pady=0)
    results_section.grid(row=3, column=0, sticky="nesw")
    return books_page

def build_category_section(master_frame):
    category_section = tk.Frame(master_frame, bg="grey")

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
                bg="green", 
                command=books_page_state['book_categories'][index][1]
            )
            new_checkbox.deselect()
            new_checkbox.grid(row=j, column=i, padx=0, pady=0, sticky="w")
    
    return category_section

def build_search_section(master_frame):
    global search_bar
    search_section = tk.Frame(master=master_frame, bg="darkgrey")
    search_bar = tk.Entry(master=search_section, textvariable=books_page_state['search_var'])
    search_button = tk.Button(master=search_section, text="Search")
    search_bar.pack(fill=tk.X, expand=3, side=tk.LEFT)
    search_button.pack(fill=tk.X, expand=1, side=tk.LEFT)

    return search_section

def build_results_section(master_frame):
    results_section = tk.Frame(master=master_frame, bg="pink")
    results_section.rowconfigure(0, weight=1, minsize=10)
    results_section.columnconfigure(0, weight=1, minsize=10)
    
    footer_frame = tk.Frame(master=results_section, bg="purple")
    previous_button = tk.Button(footer_frame, text="Previous", command=lambda: change_book_results_page(False))
    next_button = tk.Button(footer_frame, text="Next", command=lambda: change_book_results_page(True))
    page_label = tk.Label(footer_frame, text="Page")

    books_page_state['page_label'] = page_label

    previous_button.pack(fill=tk.Y, side=tk.LEFT)
    next_button.pack(fill=tk.Y, side=tk.LEFT)
    page_label.pack(fill=tk.Y, side=tk.RIGHT)

    footer_frame.pack(fill=tk.X, side=tk.BOTTOM, expand=0)
    books_page_state['results_section'] = results_section
    return results_section
    
### Assignments/function calls ===========================================================
page_manager['pages_section'] = build_page_container()

# ==================================================================================== MOVING BETWEEN PAGES ====================================================================================
def go_to_home_page(e):
    notebook = page_manager['pages_section']
    active_tab = notebook.index(notebook.select())
    if active_tab == 0:
        transition(to_home=True)

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

root.mainloop()
