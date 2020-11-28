import tkinter as tk
import tkinter.font as tkFont

from datetime import datetime as dt

# ============================================================ HOME PAGE ============================================================
root = tk.Tk()
root.title('Loughborough Library Management System - Firat Batmaz')
root.geometry('900x630')
root.minsize(600, 420)
root.maxsize(1350, 945)
root.aspect(10,7,10,7)

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

    heading_font = tkFont.Font(family="Verdana", size=40)
    sub_heading_font = tkFont.Font(family="Verdana", size=20)

    heading = tk.Label(master=hero_section, text="Loughborough Library", font=heading_font, bg="purple", fg="magenta")
    sub_heading = tk.Label(master=hero_section, text=f"{dt.strftime(dt.now(), '%d %B, %Y')}", font=sub_heading_font, bg="purple", fg="magenta")

    heading.grid(row=0, column=0, sticky="ws", padx=10)
    sub_heading.grid(row=1, column=0, sticky="wn", padx=15)

    return hero_section

def build_button_section(master_frame):
    button_section = tk.Frame(master=master_frame, bg="grey")
    button_info = [('Books', 'blue'), ('Loan Manager', 'green'), ('Analytics', 'orange'), ('System Info', 'grey')]
    button_font = tkFont.Font(family="helvetica", size=20)

    for i in range(2):
        button_section.columnconfigure(i, weight=1, minsize=25)
        button_section.rowconfigure(i, weight=1, minsize=25)
        for j in range(2):
            new_button_info = button_info[j + i * 2]
            new_button = tk.Button(button_section, text=new_button_info[0], font=button_font, highlightbackground=new_button_info[1], bg=new_button_info[1], highlightthickness=10, fg="black", relief=tk.RAISED)
            new_button.grid(row=i, column=j, sticky="nesw")
    
    return button_section

if __name__ == '__main__':
    my_home = build_home_page()
    my_home.pack(fill=tk.BOTH, expand=1)
    root.mainloop()