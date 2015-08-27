#! /usr/bin/env python

import pwn
import threading

class Collector (threading.Thread):
    def set_conn_buff(self, c, b):
        self.c = c
        self.b = b
        return self

    def run(self):
        while True:
            self.b.append(self.c.recv(1024)) ##


class Connection():
    def __init__(self):
        self.data_buffer = []

    def listen(self, port_no):
        l = pwn.listen(port_no)
        self.conn = l.wait_for_connection()
        Collector().set_conn_buff(self.conn, self.data_buffer).start()

    def connect(self, ip, port_no):
        self.conn = pwn.remote(ip, port_no)
        Collector().set_conn_buff(self.conn, self.data_buffer).start()

    def ready(self):
        total_string = ''.join(self.data_buffer)
        loc = total_string.find('\x0d\x0a')
        if ( loc == -1 ):
            return False
        else:
            return True

    def recv(self):
        total_string = ''.join(self.data_buffer)
        loc = total_string.find('\x0d\x0a')
        ret = total_string[:loc]
        self.data_buffer = [total_string[2+loc:]]
        return ret

    def send(self, data):
        self.conn.send(data)
