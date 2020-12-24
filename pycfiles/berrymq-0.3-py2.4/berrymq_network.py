# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/berrymq/berrymq_network.py
# Compiled at: 2009-07-31 20:32:46
import urlparse, xmlrpclib, threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
_stop_server = False
_server = None
_receiver = None
_server_thread = None

def _is_network_init():
    global _server
    return _server is not None


def network_init(url):
    global _receiver
    global _server
    global _server_thread
    global _stop_server
    if _is_network_init():
        raise RuntimeError('network connection is already initialized')
    netloc = urlparse.urlparse(url)[1]
    (host, port) = netloc.split(':')
    _server = SimpleXMLRPCServer((host, int(port)))
    _receiver = mqas.MessageQueueReceiver(url)
    _server.register_instance(_receiver)
    _stop_server = False

    def _network_main():
        while not _stop_server:
            _server.handle_request()

    _server_thread = threading.Thread(target=_network_main)
    _server_thread.start()


def network_connect(url):
    if not _is_network_init():
        raise RuntimeError('network connection is not initialized')
    _receiver._add_connection(url)


def network_quit():
    global _stop_server
    if not _is_network_init():
        raise RuntimeError('network connection is not initialized')
    _stop_server = True
    network_mainloop()


def network_mainloop():
    if not _is_network_init():
        raise RuntimeError('network connection is not initialized')
    _server_thread.join()