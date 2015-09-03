#! /usr/bin/env python

import threading
import time
import sys
import network


def usage():
    print "Usage:"
    print "    Server: " + sys.argv[0] + " port_number"
    print "    Client: " + sys.argv[0] + " ip_address port_number"
    sys.exit()

if not (len(sys.argv) == 2 or len(sys.argv) == 3):
    usage()

conn = network.Connection()

if len(sys.argv) == 2:  # server
    try:
        conn.listen(int(sys.argv[1]))
    except:
        print "Unable to open port %d" % int(sys.argv[1])
        sys.exit()
elif len(sys.argv) == 3:  # client
    try:
        conn.connect(sys.argv[1], int(sys.argv[2]))
    except:
        print "Unable to connect to %s at port %d" % (sys.argv[1], int(sys.argv[2]))
        sys.exit()
else:
    print "Unreachable code reached!!!"
    sys.exit()


def send_message(text):
    conn.send(text)


class GUIThread (threading.Thread):

    def run(self):
        import gui
        gui.set_send_message_callback(send_message)
        gui.start()

GUIThread().start()

while True:
    line = conn.recv()
    if line is not None:
        import gui
        if line != '':
            gui.add_new_text("[Other] " + line)
    else:
        break
