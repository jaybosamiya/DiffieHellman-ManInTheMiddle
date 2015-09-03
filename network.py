#! /usr/bin/env python

import pwn

encoding_method = 'base64'


class Connection():

    def __init__(self):
        self.data_buffer = []

    def listen(self, port_no):
        l = pwn.listen(port_no)
        self.conn = l.wait_for_connection()

    def connect(self, ip, port_no):
        self.conn = pwn.remote(ip, port_no)

    def recv(self):
        try:
            return self.conn.recvline().strip().decode(encoding_method).strip()
        except EOFError:
            return None

    def send(self, data):
        self.conn.send(data.strip().encode(encoding_method) + '\n')
