# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/websocket_proxy_test.py
# Compiled at: 2015-11-19 18:49:54
from dez.network import WebSocketProxy

def main(domain, port):
    proxy = WebSocketProxy('localhost', 81, domain, port)
    proxy.start()