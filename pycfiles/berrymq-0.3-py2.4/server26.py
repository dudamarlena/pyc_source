# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/berrymq/jsonrpc/server26.py
# Compiled at: 2009-10-07 12:34:23
import json, select, threading, SocketServer
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
        SimpleJSONRPCDispatcher.__init__(self, allow_none=True, encoding=None)
        SocketServer.TCPServer.__init__(self, addr, requestHandler)
        self.__thread = None
        return

    def serve_forever(self, in_thread=False, poll_interval=0.5):

        def serve_thread(server, poll_interval):
            server.serve_forever(poll_interval=poll_interval)

        if in_thread:
            args = [
             self, poll_interval]
            self.__thread = threading.Thread(target=serve_thread, args=args)
            self.__thread.setDaemon(True)
            self.__thread.start()
        else:
            SocketServer.TCPServer.serve_forever(self, poll_interval)

    def shutdown(self, immediately=True):
        if not immediately:
            self._BaseServer__serving = False
            return
        SocketServer.TCPServer.shutdown(self)
        if self.__thread:
            self.__thread.join()
            self.__thread = None
        return