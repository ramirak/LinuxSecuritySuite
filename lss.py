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


def create_main_window():
    window = Tk()
    window.configure(bg=main_color)
    window.minsize(width=1100, height=750)
    window.title("Linux Security Suite")
    return window


def edit_policies():
    window = Toplevel()
    window.minsize(width=1200, height=700)
    window.configure(bg=main_color)
    center(window)
    header = Label(window, text="Policy Editor", bg=main_color, fg=font_secondary_color, font=(font_family, 18, "bold", "italic"))
    header.bind('<Enter>', lambda e: e.widget.config(fg=hover_color))
    header.bind('<Leave>', lambda e: e.widget.config(fg=font_secondary_color))
    header.pack(pady=10)
    frame_args = {"border":0, "bg":main_color }
    frame1 = Frame(window, **frame_args)
    frame1.pack(side=TOP, fill=X)
    frame2 = Frame(window, **frame_args)
    frame2.pack(side=TOP, fill=X, padx=10, pady=10)
    frame = Frame(window, **frame_args) 
    frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    
    scrollbar = Scrollbar(frame, bg=secondary_color, border=0, highlightthickness=0)
   # scrollbar.config(command=T.yview) 
    scrollbar.pack(side=RIGHT, fill=Y)    
    all_policies = retrieve_from_file("data/policies.json")
    my_config = retrieve_from_file("data/config.json")

    def menu_change(*args):
        update_table(treeview)

    def add(tree):
        tree.insert("",'end',values=tuple([entry.get() for entry in entries]))

    def delete(tree):
        # Get selected item to Delete
        selected_item = tree.selection()[0]
        tree.delete(selected_item)

    def save_polciy():
        policy_keys = ["dir", "src", "dst", "dport", "proto", "action"] 
        policy = []
        for child in treeview.get_children():
            policy.append(list_to_json(policy_keys,treeview.item(child)["values"]))
        replace_val_from_key("basic", policy, "data/policies.json")

    def selectItem(a):
        curItem = treeview.focus()
        if curItem:
            for i in range(len(entries)):
                entries[i].delete(0, END)
                entries[i].insert(0, (treeview.item(curItem)['values'][i]))
  
    def clear_all(tree):
        for item in tree.get_children():
            tree.delete(item)

    def update_table(tree):
        clear_all(tree)
        for row in all_policies[variable.get()]:
            tree.insert("", "end", values=(row["dir"], row["src"], row["dst"], row["dport"], row["proto"], row["action"]))


    # Change policy menu
    OPTIONS=list(all_policies)
    variable = StringVar(window)
    variable.set(OPTIONS[0]) # default value
    w = OptionMenu(frame1, variable, *OPTIONS)
    w.config(bg=main_color, fg=font_color,width=25, height=1, border=0, highlightthickness=0, font=(font_family, 10, "bold", "italic"))
    w["menu"].config(bg=secondary_color, fg=font_color, border=0)
    w.pack()
 
    # Editor 
    entries = []
    for i in range(6):
        entries.append(Entry(frame2, background=main_color, justify=CENTER,foreground=font_color, borderwidth=0, font=(font_family, 10)))
        entries[i].pack(side = LEFT, fill=X, expand=True)

    # Table
    treeview = ttk.Treeview(frame, show="headings", columns=("Direction", "Source", "Destination", "DPORT", "PROTOCOL", "ACTION"))
    treeview.heading("#1", text="Direction")
    treeview.heading("#2", text="Source")
    treeview.heading("#3", text="Destination")
    treeview.heading("#4", text="Dport")
    treeview.heading("#5", text="Protocol")
    treeview.heading("#6", text="Action") 
    style = ttk.Style(frame)
    style.theme_use("clam")
    style.configure("Treeview", background=secondary_color,fieldbackground="black", foreground=font_color, relief='flat')
    style.configure("Treeview.Heading", background=main_color, foreground=font_color, fieldbackground="black", relief="flat")

    # Buttons
    Button(frame1, text="Add rule", **button_args_small, command=lambda:add(treeview)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Remove rule", **button_args_small, command = lambda:delete(treeview)).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="New policy", **button_args_small).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Save rules", **button_args_small, command=lambda: save_polciy()).pack(pady=5,side=LEFT, expand=True)
    Button(frame1, text="Close", **button_args_small, command=lambda: window.destroy()).pack(pady=5,side=LEFT, expand=True)

    # bindings and initializations 
    treeview.bind('<ButtonRelease-1>', selectItem)
    treeview.pack(fill=BOTH,expand=True)  
    update_table(treeview)
    variable.trace("w", menu_change)


def create_buttons(root):    
    frame_args = {"border":0, "bg":main_color }
    frame1 = Frame(root, **frame_args)
    frame1.pack(side=TOP, fill=X)
    frame3 = Frame(root, **frame_args)
    frame3.pack(side=RIGHT, fill=Y, padx=10, pady=10)
    frame2 = Frame(root, **frame_args)
    frame2.pack(side=LEFT, fill=Y, padx=10, pady=10)
    frame = Frame(root, **frame_args) 
    frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    scrollbar = Scrollbar(frame, bg=secondary_color, border=0, highlightthickness=0)
    T=Text(frame, bg=main_color, fg=font_color,font=('Serif-bold', 11), border=0, highlightthickness=0,yscrollcommand=scrollbar.set)
    scrollbar.config(command=T.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    T.insert(INSERT,os.popen('netstat -tupn').read())
    T.config(state=DISABLED)
    T.pack(expand=True,fill="both")


    buttons = [
            Button(frame2,text="Status", **button_args),
              Button(frame2,text="My rules", **button_args), 
            Button(frame2,text="Active connections", **button_args, command = lambda : [T.config(state="normal"),T.delete("1.0", "end"), T.insert(INSERT,os.popen('netstat -tupn').read()),T.config(state="disabled")]),
            Button(frame2,text="Processes", **button_args, command = lambda : [T.config(state="normal"),T.delete("1.0", "end"), T.insert(INSERT,os.popen("ps -eM | awk '{up=toupper($5);a[up]}END{for(i in a) print i}'").read().title()),T.config(state="disabled")]),
              Button(frame2,text="Settings", **button_args),
              Button(frame2,text="Exit", **button_args, command=lambda:root.destroy()), 
              Button(frame3,text="Apply policy", **button_args),
              Button(frame3,text="Edit policies", **button_args, command=lambda:edit_policies()),
              Button(frame3,text="Firewall Logs", **button_args)]
    for b in buttons:
        b.bind('<Enter>', lambda e: e.widget.config(bg=hover_color))
        b.bind('<Leave>', lambda e: e.widget.config(bg=secondary_color))
        b.pack(padx=3, pady=3,side=TOP)
  

def init():
    root = create_main_window()
    center(root)
    header = Label(text="Linux Security Suite", bg=main_color, fg=font_secondary_color, font=(font_family, 18, "bold", "italic"))
    header.bind('<Enter>', lambda e: e.widget.config(fg=hover_color))
    header.bind('<Leave>', lambda e: e.widget.config(fg=font_secondary_color))
    header.pack(pady=10)
    create_buttons(root)
    root.mainloop()


init()
