#! /usr/bin/env python

import threading
import time
import sys
import network
from diffie_hellman import DiffieHellman
import crypto_protocol


def usage():
    print "Usage:"
    print "    Server: " + sys.argv[0] + " port_number"
    print "    Client: " + sys.argv[0] + " ip_address port_number"
    sys.exit()

if not (len(sys.argv) == 2 or len(sys.argv) == 3):
    usage()

conn = network.Connection()
dh = None


def get_line():
    line = None
    while line is None:
        line = conn.recv()
    return line

if len(sys.argv) == 2:  # server
    try:
        conn.listen(int(sys.argv[1]))
        dh = DiffieHellman()
        p, g, A = dh.generate_public_broadcast()
        conn.send(str(p))
        conn.send(str(g))
        conn.send(str(A))
        B = int(get_line())
        crypto_protocol.init(dh.get_shared_secret(B))
    except:
        print "Unable to open port %d" % int(sys.argv[1])
        sys.exit()
elif len(sys.argv) == 3:  # client
    try:
        conn.connect(sys.argv[1], int(sys.argv[2]))
        p = int(get_line())
        g = int(get_line())
        A = int(get_line())
        dh = DiffieHellman(p, g)
        _, _, B = dh.generate_public_broadcast()
        conn.send(str(B))
        crypto_protocol.init(dh.get_shared_secret(A))
    except:
        print "Unable to connect to %s at port %d" % (sys.argv[1], int(sys.argv[2]))
        sys.exit()
else:
    print "Unreachable code reached!!!"
    sys.exit()


def send_message(text):
    conn.send(crypto_protocol.encrypt(text))


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
            gui.add_new_text("[Other] " + crypto_protocol.decrypt(line))
    else:
        break
