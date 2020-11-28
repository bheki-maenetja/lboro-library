import tkinter as tk
import tkinter.font as tkFont

# ============================================================ HOME PAGE ============================================================
root = tk.Tk()
root.geometry('900x630')
root.minsize(600, 420)
root.maxsize(1350, 945)
root.aspect(10,7,10,7)

def build_home_page():
    home_frame = tk.Frame(master=root, height=100, width=100)
    home_frame.columnconfigure(0, weight=1, minsize=root.winfo_height())
    home_frame.rowconfigure(0, weight=1, minsize=root.winfo_width())
    home_frame.rowconfigure(1, weight=1, minsize=root.winfo_width())

    hero_section = tk.Frame(master=home_frame, bg="blue")
    button_section = tk.Frame(master=home_frame, bg="green")
    hero_section.grid(row=0, column=0, sticky="nesw")
    button_section.grid(row=1, column=0, sticky="nesw")

    return home_frame

my_home = build_home_page()
my_home.pack(fill=tk.BOTH, expand=1)


if __name__ == '__main__':
    root.mainloop()