# Standard Library Imports
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from datetime import datetime as dt

# Local Imports
import booksearch as bs

# ============================================================ MAIN WINDOW ============================================================
root = tk.Tk()
root.title('Loughborough Library Management System')
root.geometry('900x630')
root.minsize(600, 420)
root.maxsize(1350, 945)
root.aspect(10,7,10,7)

page_manager = dict()

# ============================================================ HOME PAGE ============================================================
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

# ============================================================ OTHER PAGES ============================================================
## The Main Page Container
def build_page_container():
    page_notebook = ttk.Notebook(master=root)
    page_notebook.add(tk.Frame(), text="Home")

    books_page = bs.build_books_page(page_notebook)

    page_notebook.add(books_page, text="Books")
    page_notebook.add(tk.Frame(master=page_notebook, bg="green"), text="Loan Manager")
    page_notebook.add(tk.Frame(master=page_notebook, bg="orange"), text="Analytics")
    page_notebook.add(tk.Frame(master=page_notebook, bg="grey"), text="System Info")

    page_notebook.bind('<<NotebookTabChanged>>', lambda e: go_to_home_page(e))

    return page_notebook


page_manager['pages_section'] = build_page_container()

# ============================================================ MOVING BETWEEN PAGES ============================================================
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

# ============================================================ FUNCTION CALLS ============================================================
page_manager['home_page'].pack(fill=tk.BOTH, expand=1)
root.mainloop()

    