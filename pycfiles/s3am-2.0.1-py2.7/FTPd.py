# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s3am/test/FTPd.py
# Compiled at: 2016-11-03 16:06:47
import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class FTPd(threading.Thread):

    def __init__(self, root_dir, address=None, timeout=0.001, dtp_handler=None):
        threading.Thread.__init__(self)
        self.__flag = threading.Event()
        self.__timeout = timeout
        authorizer = DummyAuthorizer()
        authorizer.add_anonymous(root_dir)
        handler = FTPHandler
        handler.authorizer = authorizer
        if dtp_handler is not None:
            handler.dtp_handler = dtp_handler
        self.server = FTPServer(address, handler)
        return

    def start(self):
        self.__flag.clear()
        threading.Thread.start(self)
        self.__flag.wait()

    def run(self):
        self.__flag.set()
        while self.__flag.is_set():
            self.server.serve_forever(timeout=self.__timeout, blocking=False)

        self.server.close_all()
        self.server.close()

    def stop(self):
        self.__flag.clear()
        self.join()