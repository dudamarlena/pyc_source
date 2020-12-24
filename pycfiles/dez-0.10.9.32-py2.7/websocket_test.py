# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/websocket_test.py
# Compiled at: 2020-04-19 19:55:58
from dez.network import WebSocketDaemon

def new_conn(conn):
    conn.write('you are connected!')

    def recv(frame):
        conn.write('ECHO: %s' % frame)

    conn.set_cb(recv)


def log(msg):
    print '* ' + msg


def main(domain, port):
    log('starting WebSocket Test')
    log("a sample client is provided in the 'dez/samples/html' directory")
    server = WebSocketDaemon(domain, port, new_conn, report_cb=log)
    server.start()