#! /usr/bin/env python

# TODO: Convert key exchange protocol part into function to reduce repetition of code.
# TODO: Thread are getting desync on certain conditions. Find and resolve them.

import threading
import time
import sys
import network
from diffie_hellman import DiffieHellman
from crypto_protocol import CryptoProtocol


def usage():
    print "Usage:"
    print "    " + sys.argv[0] + "server_ip server_port client_ip client_port"
    sys.exit()

if len(sys.argv) != 5:
    usage()


def get_line(conn):
    line = None
    while line is None:
        line = conn.recv()
    return line

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
client_ip = sys.argv[3]
client_port = int(sys.argv[4])

conn_server = network.Connection()  # connection with server
conn_client = network.Connection()  # connection with client
dh_server = None
dh_client = None
crypto_protocol_server = None
crypto_protocol_client = None

try:
    conn_client.listen(client_port)
except:
    print "Unable to open port %d" % client_port
    sys.exit()

try:
    conn_server.connect(server_ip, server_port)
except:
    print "Unable to connect to %s at port %d" % (server_ip, server_port)

####### Key exchange: Later can be added some other variants too.#######

p_server = int(get_line(conn_server))
g_server = int(get_line(conn_server))
A_server = int(get_line(conn_server))

dh_server = DiffieHellman(p_server, g_server)
_, _, B_server = dh_server.generate_public_broadcast()
conn_server.send(str(B_server))
crypto_protocol_server = CryptoProtocol(dh_server.get_shared_secret(A_server))

p_client = p_server
g_client = g_server

dh_client = DiffieHellman(p_server, g_server)
_, _, A_client = dh_client.generate_public_broadcast()

conn_client.send(str(p_client))
conn_client.send(str(g_client))
conn_client.send(str(A_client))

B_client = int(get_line(conn_client))
crypto_protocol_client = CryptoProtocol(dh_client.get_shared_secret(B_client))

# KEY EXCHANGE ENDS


class GUIThread (threading.Thread):

    def run(self):
        import gui
        gui.start()

GUIThread().start()


def session(conn_receive, cp_receive, conn_send, cp_send, name):
    while True:
        line = conn_receive.recv()
        if line is not None:
            import gui
            if line != '':
                line = cp_receive.decrypt(line)
                gui.add_new_text("[" + name + "] " + line)
                conn_send.send(cp_send.encrypt(line))
        else:
            break

t = threading.Thread(target=session, args=(
    conn_server, crypto_protocol_server, conn_client, crypto_protocol_client, "server"))
t.daemon = True
t.start()

session(conn_client, crypto_protocol_client, conn_server, crypto_protocol_server, "client")
