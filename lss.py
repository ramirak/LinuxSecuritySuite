from tkinter import *
import os, sys

main_color = "#191A19"
secondary_color = "#1E5128"
hover_color = "#D8E9A8"
font_color = "#D8E9A8"
font_secondary_color = "#4E9F3D"
font_family = "Segoe UI Semilight"


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
    os.setuid(os.geteuid())

    T.insert(INSERT,os.popen('netstat -tupn').read())
    T.config(state=DISABLED)
    T.pack(expand=True,fill="both")

    button_args = {"height":3, "width":15,"borderwidth":0,"highlightthickness":0, "bg":secondary_color, "fg":font_color, "font":("Serif-bold", 10) }

    buttons = [
            Button(frame2,text="Status", **button_args),
              Button(frame2,text="My rules", **button_args), 
            Button(frame2,text="Active connections", **button_args, command = lambda : [T.config(state="normal"),T.delete("1.0", "end"), T.insert(INSERT,os.popen('netstat -tupn').read()),T.config(state="disabled")]),
            Button(frame2,text="Processes", **button_args, command = lambda : [T.config(state="normal"),T.delete("1.0", "end"), T.insert(INSERT,os.popen("ps -eM | awk '{up=toupper($5);a[up]}END{for(i in a) print i}'").read().title()),T.config(state="disabled")]),
              Button(frame2,text="Settings", **button_args),
              Button(frame2,text="Exit", **button_args, command=lambda:root.destroy()), 
              Button(frame3,text="Apply policy", **button_args),
              Button(frame3,text="Edit policies", **button_args),
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
