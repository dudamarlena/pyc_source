# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/omnilog/server.py
# Compiled at: 2016-03-08 18:23:57
# Size of source mod 2**32: 1752 bytes
import http.server as Server, threading
from omnilog.strings import Strings
from omnilog.ipcactions import IPCActions
from omnilog.ipcmessage import IPCMessage
from omnilog.logger import Logger

class RequestHandler(Server.SimpleHTTPRequestHandler):
    __doc__ = '\n    Class to implement document root in simple.http server\n    '
    routes = None

    def translate_path(self, path):
        return_path = False
        for patt, rootDir in self.routes:
            if path.startswith(patt):
                return_path = rootDir + path
                break

        return return_path


class HTTPServer(threading.Thread):
    __doc__ = '\n    Our HTTP server wrapper class.\n    '
    name = 'SUB-HTTPServer'
    runner = None

    def __init__(self, config, runner, vertical_queue):
        super().__init__()
        self.config = config
        self.request_handler = RequestHandler
        self.runner = runner
        self.logger = Logger()
        self.routes = [
         (
          '/', self.config['docRoot'])]
        self.vertical_queue = vertical_queue

    def run(self):
        """
        Runner for http server, uses user defined config for server.

        """
        try:
            self.logger.info(self.name + ' ' + Strings.SUB_SYSTEM_START)
            address = (
             self.config['listenAddress'], self.config['listenPort'])
            self.request_handler.routes = self.routes
            httpd = Server.HTTPServer(address, self.request_handler)
            httpd.timeout = 2
            while self.runner.is_set():
                httpd.handle_request()

        except KeyError:
            comm = IPCMessage(self.name, IPCActions.ACTION_SHUTDOWN, Strings.CONFIG_ERROR)
            self.vertical_queue.put(comm)