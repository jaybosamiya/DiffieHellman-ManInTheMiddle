#! /usr/bin/env python

import Tkinter
import sys

top = Tkinter.Tk()

scrolling_text_box = Tkinter.Text(top, height=10)
scrolling_text_box.pack(fill=Tkinter.X)

input_text_box = Tkinter.Entry(top)
input_text_box.pack(fill=Tkinter.X)


def add_new_text(text):
    scrolling_text_box.insert(Tkinter.INSERT, text + "\n")
    scrolling_text_box.see(Tkinter.END)

message_sender_callback = None


def send_message_callback():
    if message_sender_callback is None:
        print "Sender callback not registered properly :("
        sys.exit
    else:
        message = input_text_box.get()
        if message.strip() != '':
            message_sender_callback(message)
            add_new_text("[Me] " + message)
            input_text_box.delete(0, Tkinter.END)


def set_send_message_callback(callback):
    global message_sender_callback
    message_sender_callback = callback

Tkinter.Button(top, text="Send Message",
               command=send_message_callback).pack()


def start():
    top.mainloop()
