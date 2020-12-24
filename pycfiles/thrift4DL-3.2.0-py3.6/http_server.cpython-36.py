# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thrift4DL/server/http/http_server.py
# Compiled at: 2020-01-12 21:21:44
# Size of source mod 2**32: 791 bytes
import sys, os
from .api import create_app
from multiprocessing import Process
from wsgiserver import WSGIServer

class HTTPServer(Process):

    def __init__(self, host, port, http_port):
        Process.__init__(self)
        self.host = host
        self.port = port
        self.http_port = http_port

    def start_http_server(self, host, port, http_port):
        app = create_app(host=host, port=port)
        http_server = WSGIServer(app, host='0.0.0.0', port=(int(http_port)))
        http_server.start()

    def run(self):
        print(f"Start HTTPServer on 0.0.0.0:{self.http_port}")
        self.start_http_server(self.host, self.port, self.http_port)