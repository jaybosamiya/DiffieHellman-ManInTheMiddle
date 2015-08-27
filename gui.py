#! /usr/bin/env python

import Tkinter

top = Tkinter.Tk()

scrolling_text_box = Tkinter.Text(top, height=10)
scrolling_text_box.pack(fill=Tkinter.X)

input_text_box = Tkinter.Entry(top)
input_text_box.pack(fill=Tkinter.X)

def add_new_text(text):
    scrolling_text_box.insert(Tkinter.INSERT, text + "\n")
    scrolling_text_box.see(Tkinter.END)

def send_message_callback():
    # TODO: Write stuff here
    pass

Tkinter.Button(top, text ="Send Message", command = send_message_callback).pack()

top.mainloop()
