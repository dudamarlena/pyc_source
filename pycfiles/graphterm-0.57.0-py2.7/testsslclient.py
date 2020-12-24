# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/testsslclient.py
# Compiled at: 2012-07-11 17:28:41
import os, socket, ssl, sys, pprint, time
host_port = ('localhost', 8899)
ssl_options = {'cert_reqs': ssl.CERT_REQUIRED, 'ca_certs': os.getenv('HOME') + '/.ssh/localhost.crt'}

def on_connect():
    print 'Connected'
    time.sleep(5)


import tornado.iostream, tornado.ioloop, packetserver

class MyClient(packetserver.PacketClient):
    _all_connections = {}

    def __init__(self, host, port, lterm_cookie='', io_loop=None, ssl_options={}):
        super(MyClient, self).__init__(host, port, io_loop=io_loop, ssl_options=ssl_options, max_packet_buf=3, reconnect_sec=300, server_type='frame')


conn2 = MyClient.get_client('conn2', connect=host_port, connect_kw={'ssl_options': ssl_options})
tornado.ioloop.IOLoop.instance().start()
print 'conn2', conn2