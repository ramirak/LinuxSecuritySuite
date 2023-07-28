from ui_tools import *
from utils import *
from snapshot import *
from tkinter import PhotoImage

def create_editor_buttons(table_window):
    root = table_window.window 
    frame1 = table_window.frames[0]
    frame2 = table_window.frames[1]
    treeview = table_window.tree

    restore_request = 0
    snapshot_request = 0
    path = get_data_dir() + "/snapshots.json"
    table = SnapshotTable(path)
    table.reload_data()

    # Create all buttons
    Button(frame1, text="Execute", **button_args_small, command=lambda:execute_all()).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Save", **button_args_small, command=lambda:table.save_data()).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Quick Snapshot", **button_args_small, command=lambda:set_op(SnapshotOperation.CREATE.name, SnapshotType.QUICK.name)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Full Snapshot", **button_args_small, command=lambda:set_op(SnapshotOperation.CREATE.name, SnapshotType.FULL.name)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Restore", **button_args_small, command=lambda: set_op(SnapshotOperation.RESTORE.name, None)).pack(pady=5,side=LEFT, expand=True) 
    Button(frame1, text="Delete", **button_args_small, command=lambda: set_op(SnapshotOperation.DELETE.name, None)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Close", **button_args_small, command=lambda: root.destroy()).pack(pady=5,side=LEFT, expand=True)
   
    def set_op(op, op_type):
        try:
            if (op == SnapshotOperation.CREATE.name):
                uuid = None
            else:
                if len(treeview.get_children()) == 0:
                    return
                focused = treeview.focus()
                uuid = treeview.item(focused)["values"][0] 
            table.mark_for_op(uuid, op, op_type)
            update_table(treeview)
        except Exception as e:
            return e

    def execute_all():
        show_info("In development ..", root)
        return
        table.execute()
        update_table(treeview)
        show_info("Operations execution finished", root)
    
    def update_table(tree):
        clear_all_tree_vals(tree)
        for row in table.get_data():
            tree.insert("", "end", values=(row["Title"], row["Date"], row["Type"], row["Status"]))

    def menu_change(*args):
        update_table(treeview)

    # bindings and initializations 
    update_table(treeview)


def edit_snapshots():
    table_window = TableWindow("Snapshot Management", ["Snapshot title", "Date", "Type", "Status"])
    table_window.init_window()
    # Buttons
    create_editor_buttons(table_window)



