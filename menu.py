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
    button_section = tk.Frame(master=home_frame, bg="grey")
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

my_home = build_home_page()
my_home.pack(fill=tk.BOTH, expand=1)


if __name__ == '__main__':
    root.mainloop()