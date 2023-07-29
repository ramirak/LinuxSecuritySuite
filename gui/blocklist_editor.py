
from gui.ui_tools import *
from tkinter import PhotoImage
import os
from policy.blocklist import *


def create_editor_buttons(table_window):
    root = table_window.window 
    frame1 = table_window.frames[0]
    frame2 = table_window.frames[1]
    treeview = table_window.tree

    # Create all buttons
    Button(frame1, text="Apply", **button_args_small, command=lambda:apply(treeview)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Disable rules", **button_args_small, command=lambda:clear()).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Close", **button_args_small, command=lambda: root.destroy()).pack(pady=5,side=LEFT, expand=True)

    def clear():
        BlocklistTable.clear_all()
        show_info("Blocklist disabled successfully" ,root)

    def apply(tree):
        try:
            focused = treeview.focus()
            name = treeview.item(focused)["values"][0]
            BlocklistTable.apply_blocklist(name)
            show_info("List applied successfully !" ,root)
        except:
            return

    def update_table(tree):
        clear_all_tree_vals(tree)
        i = 1
        for row in BlocklistTable.get_all_lists():
            columns = [ i, row[0], row[1]]
            tree.insert("", "end", values=tuple(columns))
            i+=1 

    def selectItem(a):                   
        curItem = treeview.focus()
        if curItem:
            pass

    treeview.bind('<ButtonRelease-1>', selectItem)
    update_table(treeview)


def edit_blocklists():
    # Configure main window
    keys = ["ID", "List name", "Total number of IPs / Domains"]
    table_window = TableWindow("Blocklist management", keys)
    table_window.init_window()
    # Buttons
    create_editor_buttons(table_window)


