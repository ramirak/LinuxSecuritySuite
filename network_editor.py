from ui_tools import *
from tkinter import PhotoImage
import os
from networking import *
from ip_checks import is_valid_ip2
from utils import *

def create_editor_buttons(table_window):
    root = table_window.window 
    frame1 = table_window.frames[0]
    frame2 = table_window.frames[1]
    treeview = table_window.tree
    
    path = get_data_dir() + "/network.json"
    table = NetworkTable(path)
    table.reload_data()

    entries = []
    for i in range(2):
        entries.append(Entry(frame2, background=main_color, justify=CENTER,foreground=font_color, borderwidth=0, font=(font_family, 10)))
        entries[i].pack(side = LEFT, fill=X, expand=True)

    def set_entry_text(entry, text):
        entry.delete(0, END)
        entry.insert(0, text)

    set_entry_text(entries[0],"192.168.1.1")
    set_entry_text(entries[1],"255.255.255.0")

    # Create all buttons
    Button(frame1, text="Quick Scan", **button_args_small, command=lambda:scan(1)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Slow Scan", **button_args_small, command=lambda:scan(0)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Close", **button_args_small, command=lambda: root.destroy()).pack(pady=5,side=LEFT, expand=True)

    def scan(quick):
        tmo = 1
        if quick:
            tmo = 0.2
        IP = entries[0].get()
        SUBNET = entries[1].get()
        if is_valid_ip2(IP) and is_valid_ip2(SUBNET):
            table.probe_network(IP, SUBNET, tmo)
            table.save_data()
            update_table(treeview)
        else:
           show_info("Invalid IP address", root) 

    def update_table(tree):
        clear_all_tree_vals(tree)
        i = 1
        for row in table.get_data():
            columns = [ row[key.name] for key in Network_Keys ]
            columns.insert(0, i)
            tree.insert("", "end", values=tuple(columns))
            i+=1

    def selectItem(a):                   
        curItem = treeview.focus()
        if curItem:
            pass

    treeview.bind('<ButtonRelease-1>', selectItem)
    update_table(treeview)


def edit_network():
    # Configure main window
    keys = ["ID", "IP address", "Mac Address"]
    table_window = TableWindow("Network Discovery", keys)
    table_window.init_window()
    # Buttons
    create_editor_buttons(table_window)


