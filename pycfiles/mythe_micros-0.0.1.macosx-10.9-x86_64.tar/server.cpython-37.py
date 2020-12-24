# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/mythe_micros/server.py
# Compiled at: 2019-12-22 13:03:48
# Size of source mod 2**32: 1410 bytes
import socket, sys, time
from multiprocessing import Process
from utils import cprint

class server(Process):

    def __init__(self, addr, name, role='worker', links=10):
        Process.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        self.name = name
        self.links = links
        self.role = 'worker'
        self.func_route = {}
        self.bind()

    def bind(self):
        try:
            self.s.bind(self.addr)
            print('INFO: Server %s:%s will run on - IP : %s, PORT : %s.' % (cprint(self.name, 'yellow', False),
             cprint(self.role, 'sky', False), cprint(self.addr[0], 'Green', False), cprint(self.addr[1], 'Green', False)))
        except Exception as e:
            try:
                print('Bind Error.\n', e)
                sys.exit()
            finally:
                e = None
                del e

    def add(self, msg_type, func):
        pass

    def test(self, ss):
        cprint(ss, 'red')

    def add_work(self, key_word, func):
        self.func_route[key_word] = func

    def run(self):
        self.s.listen(self.links)
        while True:
            conn, addr = self.s.accept()


if __name__ == '__main__':
    s = server(('localhost', 60001), 'master')
    s.start()