# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/youdao/customizer.py
# Compiled at: 2019-02-16 23:51:48
"""
    fetch result from the backup server, default backup server hellflame.net:3679 (abandoned !)
    btw: customized server is not a must, but it will speed up a little the query progress
"""
import socket, json
from contextlib import contextmanager

class Customize(object):

    def __init__(self, target, host='hellflame.net', port=3697):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(7)
        self.target = target
        self.address = (host, port)

    @contextmanager
    def connection(self):
        try:
            self.socket.connect(self.address)
            self.socket.send(self.target.replace('\r\n', '') + '\r\n')
            yield self.socket.recv(100000)
            self.socket.close()
        except:
            yield ''

    def server_fetch(self):
        with self.connection() as (result):
            if result:
                return json.loads(result)
            else:
                return

        return


if __name__ == '__main__':
    Customize('localhost', 'localhost', 5001).server_fetch()