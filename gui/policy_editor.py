from gui.ui_tools import *
from tools.utils import *
from tkinter import PhotoImage
from policy.policy import *


def create_editor_buttons(table_window):
    root = table_window.window 
    frame1 = table_window.frames[0]
    frame2 = table_window.frames[1]
    treeview = table_window.tree

    # Get data from jsons
    all_policies = PolicyTable.get_all_policies()
    
    # Change policy menu
    drop_down, menu_var = create_dropdown(frame1, list(all_policies))

    # Entries for editor buttons 
    entries = []
    for i in range(7):
        entries.append(Entry(frame2, background=main_color, justify=CENTER,foreground=font_color, borderwidth=0, font=(font_family, 10)))
        entries[i].pack(side = LEFT, fill=X, expand=True)

    # Create all buttons
    Button(frame1, text="Add rule", **button_args_small, command=lambda:exec_op(PolicyOperation.ADD.name)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Remove rule", **button_args_small, command = lambda:exec_op(PolicyOperation.DELETE.name)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Edit rule", **button_args_small,  command = lambda:exec_op(PolicyOperation.EDIT.name)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Save rules", **button_args_small, command=lambda:exec_op(PolicyOperation.SAVE.name)).pack(pady=5,side=LEFT, expand=True)   
    Button(frame1, text="Apply", **button_args_small, command=lambda:exec_op(PolicyOperation.APPLY.name)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Close", **button_args_small, command=lambda: root.destroy()).pack(pady=5,side=LEFT, expand=True)

    
    def exec_op(op):
        try:
            my_policy = all_policies[menu_var.get()]
            if (op == PolicyOperation.ADD.name):
                my_policy.add_row([key.name for key in PolicyKeys], [entry.get() for entry in entries ])
            elif (op == PolicyOperation.EDIT.name):
                my_policy.replace_row([key.name for key in PolicyKeys], [entry.get() for entry in entries], treeview.index(treeview.selection())) 
            elif (op == PolicyOperation.DELETE.name):
                my_policy.remove_row_by_index(treeview.index(treeview.selection()))
            elif (op == PolicyOperation.SAVE.name):
                my_policy.save_data()
                show_info("Policy rules were saved.", root)
            elif (op == PolicyOperation.APPLY.name):
                my_policy.load_policy()
                show_info("Policy loaded successfully", root)
            update_table(treeview)
        except Exception as e:
            print("Failed to execute operation - " + str(e))

    def update_table(tree):
        try:
            clear_all_tree_vals(tree)
            for row in all_policies[menu_var.get()].get_data():
                columns = [ row[key.name] for key in PolicyKeys ]
                tree.insert("", "end", values=tuple(columns))
        except Exception as e:
            print("Failed to update table - " + str(e))


    def menu_change(*args):
        update_table(treeview)

    def selectItem(a):                   
        curItem = treeview.focus()
        if curItem:
            for i in range(len(entries)):
                entries[i].delete(0, END)
                entries[i].insert(0, (treeview.item(curItem)['values'][i]))
      
    # bindings and initializations 
    menu_var.trace("w", menu_change)
    treeview.bind('<ButtonRelease-1>', selectItem)
    update_table(treeview)


def edit_policies():
    # Configure main window
    table_window = TableWindow("Policy Editor", ["Direction", "Source", "Destination", "S-Port", "D-Port", "Protocol", "Action"])
    table_window.init_window()
    # Buttons
    create_editor_buttons(table_window)


