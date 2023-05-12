import os, sys
from tkinter import *
from tkinter import ttk
from json_handler import *
from ui_tools import *
from policy_editor import *
from policy import apply_current_policy, apply_blocklist

title = "Linux Security Suite"

def set_main_buttons(root, text, LEFT_FRAME, RIGHT_FRAME):
    buttons = [
            Button(LEFT_FRAME,text="Status", **button_args, command=lambda: update_window_text(text, 'systemctl status iptables.service ; echo -e "\n~~~ My Configurations: ~~~\n" ; cat data/config.json')),
              Button(LEFT_FRAME,text="Active connections", **button_args, command = lambda : update_window_text(text, 'netstat -tupn')),
              Button(LEFT_FRAME,text="Processes", **button_args, command =lambda: update_window_text(text, "ps -eM | awk '{up=toupper($5);a[up]}END{for(i in a) print i}'")),
              Button(LEFT_FRAME,text="Patch system", **button_args),
              Button(LEFT_FRAME,text="Exit", **button_args, command=lambda:root.destroy()), 
              Button(RIGHT_FRAME,text="Apply policy", **button_args, command=lambda:apply_current_policy()),
              Button(RIGHT_FRAME,text="Edit policies", **button_args, command=lambda:edit_policies()),
              Button(RIGHT_FRAME,text="Apply blocklist", **button_args, command=lambda:apply_blocklist()),
              Button(RIGHT_FRAME,text="Firewall Logs", **button_args, command=lambda: update_window_text(text, 'sudo tail -50  /var/log/iptables.log'))]
    for b in buttons:
        b.bind('<Enter>', lambda e: e.widget.config(bg=hover_color))
        b.bind('<Leave>', lambda e: e.widget.config(bg=secondary_color))
        b.pack(padx=3, pady=3,side=TOP)


def create_main_window():    
    root = Tk()
    root.configure(bg=main_color)
    root.minsize(window_width, window_height)
    root.title(title) 
    center(root)
    
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
    update_window_text(T, "netstat -tupn")
    root.mainloop()


