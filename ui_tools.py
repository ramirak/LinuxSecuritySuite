from tkinter import *
from tkinter import messagebox
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

class TableWindow():
    window = None
    tree = None
    frames = []

    def __init__(self, title, keys):
        self.title = title
        self.keys = keys


    def init_window(self):
        # Configure main window
        self.window = Toplevel()
        self.window.minsize(width=window_width, height=window_height)
        self.window.configure(bg=main_color)
        self.window.resizable(True, True)
        center(self.window)

        p = PhotoImage(file = 'Screenshots/lss_icon.png')
        self.window.iconphoto(False, p)

        # Set title
        header = Label(self.window, text=self.title, bg=main_color, fg=font_secondary_color, font=(font_family, 18, "bold", "italic"))
        header.bind('<Enter>', lambda e: e.widget.config(fg=hover_color))
        header.bind('<Leave>', lambda e: e.widget.config(fg=font_secondary_color))
        header.pack(pady=10)
        
        # Create frames
        frame_args = {"border":0, "bg":main_color }
        TOP_FRAME_1 = Frame(self.window, **frame_args)
        TOP_FRAME_1.pack(side=TOP, fill=X)
        TOP_FRAME_2 = Frame(self.window, **frame_args)
        TOP_FRAME_2.pack(side=TOP, fill=X, padx=10, pady=10)
        BOTTOM_FRAME = Frame(self.window, **frame_args) 
        BOTTOM_FRAME.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
        BOTTOM_FRAME.grid_columnconfigure(0, weight=1)
        BOTTOM_FRAME.grid_rowconfigure(0, weight=1)
        BOTTOM_FRAME.grid_rowconfigure(1, weight=1)
        self.frames = [TOP_FRAME_1, TOP_FRAME_2, BOTTOM_FRAME]
                             
        # Create table
        treeview = create_tree(BOTTOM_FRAME, self.keys)

        # Configure rules scrolling
        scrollbar = Scrollbar(treeview, bg=main_color, border=1, highlightthickness=0)
        scrollbar.config(command=treeview.yview) 
        scrollbar.pack(side=RIGHT, fill=Y)  
        treeview.configure(yscrollcommand=scrollbar.set)
        self.tree = treeview


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


def show_info(text, window):
    messagebox.showinfo("LSS", text, parent=window)

def create_tree(frame, cols):
    treeview = ttk.Treeview(frame, show="headings", columns=tuple(cols))
    for i in range(len(cols)):
        treeview.heading("#" + str(i+1), text=cols[i])
        treeview.column(cols[i], anchor=CENTER, width=100)
    style = ttk.Style(frame)
    style.theme_use("clam")
    style.configure("Treeview", background=secondary_color,fieldbackground="black", foreground=font_color, relief='flat')
    style.configure("Treeview.Heading", background=main_color, foreground=font_color, fieldbackground="black", relief="flat")
    treeview.pack(fill=BOTH,expand=True)  
    return treeview


def add_tree_val(tree, vals):
    tree.insert("",'end',values=tuple(vals))


def delete_specific_tree_val(tree, item):
    try:
        tree.delete(item)
    except:
        return

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
