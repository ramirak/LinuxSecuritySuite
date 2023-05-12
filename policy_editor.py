from ui_tools import *


def create_editor_buttons(root, frame1, frame2, treeview):
    # Get data from jsons
    all_policies = retrieve_from_file("data/policies.json")
    my_config = retrieve_from_file("data/config.json")

    # Change policy menu
    drop_down, menu_var = create_dropdown(frame1, list(all_policies))

    # Entries for editor buttons 
    entries = []
    for i in range(7):
        entries.append(Entry(frame2, background=main_color, justify=CENTER,foreground=font_color, borderwidth=0, font=(font_family, 10)))
        entries[i].pack(side = LEFT, fill=X, expand=True)

    # Create all buttons
    Button(frame1, text="Add rule", **button_args_small, command=lambda:add_tree_val(treeview, tuple([entry.get() for entry in entries]))).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Remove rule", **button_args_small, command = lambda:delete_tree_val(treeview)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Save rules", **button_args_small, command=lambda: save_polciy()).pack(pady=5,side=LEFT, expand=True) 
    Button(frame1, text="Mark active", **button_args_small, command=lambda: mark_active()).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Close", **button_args_small, command=lambda: root.destroy()).pack(pady=5,side=LEFT, expand=True)

    def save_polciy():
        policy_keys = ["dir", "src", "dst", "sport", "dport", "proto", "action"] 
        policy = []
        for child in treeview.get_children():
            policy.append(list_to_json(policy_keys,treeview.item(child)["values"]))
        replace_val_from_key(menu_var.get(), policy, "data/policies.json")
        nonlocal all_policies
        all_policies = retrieve_from_file("data/policies.json")

    def mark_active():
        nonlocal my_config
        replace_val_from_key('active_policy', menu_var.get(), "data/config.json")
        my_config = retrieve_from_file("data/config.json")
 
    def update_table(tree):
        clear_all_tree_vals(tree)
        for row in all_policies[menu_var.get()]:
            tree.insert("", "end", values=(row["dir"], row["src"], row["dst"], row["sport"], row["dport"], row["proto"], row["action"]))

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
    window = Toplevel()
    window.minsize(width=window_width, height=window_height)
    window.configure(bg=main_color)
    center(window)

    # Set title
    header = Label(window, text="Policy Editor", bg=main_color, fg=font_secondary_color, font=(font_family, 18, "bold", "italic"))
    header.bind('<Enter>', lambda e: e.widget.config(fg=hover_color))
    header.bind('<Leave>', lambda e: e.widget.config(fg=font_secondary_color))
    header.pack(pady=10)
    
    # Create frames
    frame_args = {"border":0, "bg":main_color }
    TOP_FRAME_1 = Frame(window, **frame_args)
    TOP_FRAME_1.pack(side=TOP, fill=X)
    TOP_FRAME_2 = Frame(window, **frame_args)
    TOP_FRAME_2.pack(side=TOP, fill=X, padx=10, pady=10)
    BOTTOM_FRAME = Frame(window, **frame_args) 
    BOTTOM_FRAME.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
    BOTTOM_FRAME.grid_columnconfigure(0, weight=1)
    BOTTOM_FRAME.grid_rowconfigure(0, weight=1)
    BOTTOM_FRAME.grid_rowconfigure(1, weight=1)
      
                       
    # Create table
    treeview = create_tree(BOTTOM_FRAME, ["Direction", "Source", "Destination", "S-Port", "D-Port", "Protocol", "Action"])

    # Configure rules scrolling
    scrollbar = Scrollbar(treeview, bg=main_color, border=1, highlightthickness=0)
    scrollbar.config(command=treeview.yview) 
    scrollbar.pack(side=RIGHT, fill=Y)  
    treeview.configure(yscrollcommand=scrollbar.set)

    # Buttons
    create_editor_buttons(window, TOP_FRAME_1, TOP_FRAME_2, treeview)


