from tkinter import *
from tkinter import ttk
import os, sys
from json_handler import *

main_color = "#191A19"
secondary_color = "#1E5128"
hover_color = "#D8E9A8"
font_color = "#D8E9A8"
font_secondary_color = "#4E9F3D"
font_family = "Segoe UI Semilight"

window_width = 1280
window_height = 720

button_args = {"height":3, "width":15,"borderwidth":0,"highlightthickness":0, "bg":secondary_color, "fg":font_color, "font":("Serif-bold", 10) }
button_args_small = {"height":1, "width":10,"borderwidth":0,"highlightthickness":0, "bg":main_color, "fg":font_color, "font":("Serif-bold", 10) }

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def update_window_text(text, command):
    text.config(state="normal"), text.delete("1.0", "end")
    text.insert(INSERT,os.popen(command).read()),
    text.config(state="disabled")


def create_tree(frame, cols):
    treeview = ttk.Treeview(frame, show="headings", columns=tuple(cols))
    for i in range(len(cols)):
        treeview.heading("#" + str(i+1), text=cols[i])
    style = ttk.Style(frame)
    style.theme_use("clam")
    style.configure("Treeview", background=secondary_color,fieldbackground="black", foreground=font_color, relief='flat')
    style.configure("Treeview.Heading", background=main_color, foreground=font_color, fieldbackground="black", relief="flat")
    treeview.pack(fill=BOTH,expand=True)  
    return treeview


def add_tree_val(tree, vals):
    tree.insert("",'end',values=tuple(vals))


def delete_tree_val(tree):
    # Get selected item to Delete
    selected_item = tree.selection()[0]
    tree.delete(selected_item)


def clear_all_tree_vals(tree):
    for item in tree.get_children():
        tree.delete(item)


def create_dropdown(frame, menu_items):
    OPTIONS=menu_items
    variable = StringVar(frame)
    variable.set(OPTIONS[0]) # default value
    w = OptionMenu(frame, variable, *OPTIONS)
    w.config(bg=main_color, fg=font_color,width=25, height=1, border=0, highlightthickness=0, font=(font_family, 10, "bold", "italic"))
    w["menu"].config(bg=secondary_color, fg=font_color, border=0)
    w.pack()
    return w, variable
