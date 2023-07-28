import os, sys
from tkinter import *
from tkinter import ttk
from json_handler import *
from ui_tools import *
from policy_editor import *
from snapshots_editor import *
from blocklist_editor import *
from network_editor import *
from utils import *
from iptable_tools import clear_chains, set_rule_return, save_all

title = "Linux Security Suite"

def set_main_buttons(root, text, LEFT_FRAME, RIGHT_FRAME):
    sec_status = '''echo -e "~~~ My Configurations: ~~~\n" ; 
                systemctl status iptables.service ; 
                echo -e "\n" ;systemctl status apparmor ; 
                echo -e "\n~~~ Listening ports ~~~ \n"; 
                netstat -tuln ;
                echo -e "\n~~~ Sessions ~~~ \n"; 
                last | head -10'''

    buttons = [
            Button(LEFT_FRAME,text="Security dashboard", **button_args, command=lambda: update_window_text(text, sec_status)),
            Button(LEFT_FRAME,text="My rulebase", **button_args, command=lambda: update_window_text(text, 'sudo iptables -nL')),
              Button(LEFT_FRAME,text="Active connections", **button_args, command = lambda : update_window_text(text, 'netstat -tun')),
              Button(LEFT_FRAME,text="Processes", **button_args, command =lambda: update_window_text(text, "ps -eM | awk '{up=toupper($5);a[up]}END{for(i in a) print i}'")),
              Button(LEFT_FRAME,text="Exit", **button_args, command=lambda:root.destroy()), 
              Button(RIGHT_FRAME,text="My policies", **button_args, command=lambda:edit_policies()),
              Button(RIGHT_FRAME,text="System snapshots", **button_args, command=lambda:edit_snapshots()),
              Button(RIGHT_FRAME,text="Blocklists", **button_args, command=lambda:edit_blocklists()),
              Button(RIGHT_FRAME,text="Network probe", **button_args, command=lambda:edit_network()),
              Button(RIGHT_FRAME,text="Firewall Logs", **button_args, command=lambda: update_window_text(text, 'sudo tail -50  /var/log/iptables.log'))]
    for b in buttons:
        b.bind('<Enter>', lambda e: e.widget.config(bg=hover_color))
        b.bind('<Leave>', lambda e: e.widget.config(bg=secondary_color))
        b.pack(padx=3, pady=3,side=TOP)


def create_main_window():    
    root = Tk()
    root.configure(bg=main_color)
    root.minsize(window_width, window_height)
    root.resizable(True, True)
    root.title(title) 
    center(root)
    
    p1 = PhotoImage(file = 'Screenshots/lss_icon.png')
    root.iconphoto(False, p1)

    # Set title
    header = Label(text=title, bg=main_color, fg=font_secondary_color, font=(font_family, 18, "bold", "italic"))
    header.bind('<Enter>', lambda e: e.widget.config(fg=hover_color))
    header.bind('<Leave>', lambda e: e.widget.config(fg=font_secondary_color))
    header.pack(pady=10)

    # Set all frames
    frame_args = {"border":0, "bg":main_color }
    RIGHT_FRAME = Frame(root, **frame_args)
    RIGHT_FRAME.pack(side=RIGHT, fill=Y, padx=10, pady=10)
    LEFT_FRAME = Frame(root, **frame_args)
    LEFT_FRAME.pack(side=LEFT, fill=Y, padx=10, pady=10)
    TOP_FRAME = Frame(root, **frame_args) 
    TOP_FRAME.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
    TOP_FRAME.grid_columnconfigure(0, weight=1)
    TOP_FRAME.grid_rowconfigure(0, weight=1)
    TOP_FRAME.grid_rowconfigure(1, weight=1)

    # Set scrolling and main text window
    scrollbar = Scrollbar(TOP_FRAME, bg=secondary_color, border=0, highlightthickness=0)
    T=Text(TOP_FRAME, bg=main_color, fg=font_color,font=('Serif-bold', 11), border=0, highlightthickness=0,yscrollcommand=scrollbar.set)
    scrollbar.config(command=T.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    T.pack(expand=True,fill="both")
  
    # Set buttons 
    set_main_buttons(root, T, LEFT_FRAME, RIGHT_FRAME)

    # Init
    update_window_text(T, "netstat -tun")
    root.mainloop()


