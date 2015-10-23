#! /usr/bin/env python

import Tkinter
import sys

message_sender_callback = None
input_text_box = None
scrolling_text_box = None


def add_new_text(text):
    scrolling_text_box.insert(Tkinter.INSERT, text + "\n")
    scrolling_text_box.see(Tkinter.END)


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


def start(disable_input=False):
    global input_text_box, scrolling_text_box

    top = Tkinter.Tk()

    scrolling_text_box = Tkinter.Text(top, height=10)
    scrolling_text_box.pack(fill=Tkinter.X)

    if not disable_input:
        input_text_box = Tkinter.Entry(top)
        input_text_box.pack(fill=Tkinter.X)
        Tkinter.Button(top, text="Send Message",
                       command=send_message_callback).pack()

    top.mainloop()
