# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/hello_client.py
# Compiled at: 2020-04-19 19:55:58
from dez.network.client import SocketClient
import event

def main(**kwargs):
    port = kwargs['port']
    domain = kwargs['domain']
    x = SocketClient()
    x.get_connection(domain, port, get_connection_cb, ['hello10'])
    x.get_connection(domain, port, get_connection_cb, ['hello9'])
    x.get_connection(domain, port, get_connection_cb, ['hello8'])
    x.get_connection(domain, port, get_connection_cb, ['hello7'])
    x.get_connection(domain, port, get_connection_cb, ['hello6'])
    x.get_connection(domain, port, get_connection_cb, ['hello5'])
    x.get_connection(domain, port, get_connection_cb, ['hello4'])
    x.get_connection(domain, port, get_connection_cb, ['hello3'])
    x.get_connection(domain, port, get_connection_cb, ['hello2'])
    x.get_connection(domain, port, get_connection_cb, ['hello1'])
    event.signal(2, event.abort)
    event.dispatch()


def get_connection_cb(conn, payload):
    conn.write(payload, hello_world_cb, [conn])


def hello_world_cb(conn):
    conn.release()
    print 'releasing'