# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/berrymq/jsonrpc/server25.py
# Compiled at: 2009-10-07 12:34:23
import sys, simplejson as json, select, threading, SocketServer
from server_common import SimpleJSONRPCDispatcher, SimpleJSONRPCRequestHandler

class SimpleJSONRPCServer(SocketServer.TCPServer, SimpleJSONRPCDispatcher):
    """Simple JSON-RPC server.

    Simple JSON-RPC server that allows functions and a single instance
    to be installed to handle requests. The default implementation
    attempts to dispatch JSON-RPC calls to the functions or instance
    installed in the server. Override the _dispatch method inhereted
    from SimpleJSONRPCDispatcher to change this behavior.
    """
    __module__ = __name__
    allow_reuse_address = True

    def __init__(self, addr, requestHandler=SimpleJSONRPCRequestHandler, logRequests=True):
        self.logRequests = logRequests
        if sys.version_info[:2] == (2, 4):
            SimpleJSONRPCDispatcher.__init__(self)
        else:
            SimpleJSONRPCDispatcher.__init__(self, allow_none=True, encoding=None)
        SocketServer.TCPServer.__init__(self, addr, requestHandler)
        self.__serving = False
        self.__thread = None
        self.__is_shut_down = threading.Event()
        return

    def serve_forever(self, in_thread=False):

        def serve_thread(server):
            server.serve_forever()

        if in_thread:
            self.__thread = threading.Thread(target=serve_thread, args=[self])
            self.__thread.setDaemon(True)
            self.__thread.start()
        else:
            self.__serving = True
            self.__is_shut_down.clear()
            while self.__serving:
                self.handle_request()

            self.__is_shut_down.set()

    def get_request(self):
        while True:
            r = select.select([self.socket], [], [], 1)
            if len(r[0]) > 0:
                return self.socket.accept()
            if not self.__serving:
                return (None, None)

        return

    def verify_request(self, request, client_address):
        return request is not None

    def shutdown(self, immediately=True):
        self.__serving = False
        if not immediately:
            return
        self.__is_shut_down.wait()
        if self.__thread:
            self.__thread.join()
            self.__thread = None
        return