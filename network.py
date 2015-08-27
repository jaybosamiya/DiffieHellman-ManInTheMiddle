#! /usr/bin/env python

import socket
import threading

class Collector (threading.Thread):
    def set_sock_buff(self, s, b):
        self.s = s
        self.b = b
        return self

    def run(self):
        while True:
            self.b.append(self.s.recv(1024))


class Connection():
    def __init__(self):
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_buffer = []
        self.listener_thread = Collector().set_sock_buff(self.skt, self.data_buffer)

    def listen(self, port_no):
        print repr((socket.gethostname(), port_no))
        self.skt.bind((socket.gethostname(), port_no))
        self.skt.listen(5)
        self.skt, addr = self.skt.accept()
        print addr
        self.listener_thread.start()

    def connect(self, ip, port_no):
        print repr((ip, port_no))
        self.skt.connect((ip, port_no))
        self.listener_thread.start()

    def ready(self):
        total_string = ''.join(self.data_buffer)
        loc = total_string.find('\x0d\x0a')
        if ( loc == -1 ):
            return False
        else:
            return True

    def recv(self):
        total_string = ''.join(self.data_buffer)
        ret = total_string[:loc]
        self.data_buffer = [total_string[2+loc:]]
        return ret

    def send(self, data):
        self.skt.send(data)
