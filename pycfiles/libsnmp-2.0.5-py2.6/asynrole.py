# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libsnmp/asynrole.py
# Compiled at: 2008-10-18 18:59:45
import sys, asyncore, types
from libsnmp import rfc1155
from libsnmp import rfc1157
from libsnmp import role

class manager(asyncore.dispatcher):

    def __init__(self, (cb_fun, cb_ctx), dst=(None, 0), interface=('0.0.0.0', 0), timeout=0.25):
        if not callable(cb_fun):
            raise ValueError('Non-callable callback function')
        self.cb_fun = cb_fun
        self.cb_ctx = cb_ctx
        self.timeout = timeout
        asyncore.dispatcher.__init__(self)
        self.manager = role.manager(dst, interface)
        self.set_socket(self.manager.open())

    def send(self, req, dst=(None, 0)):
        self.manager.send(req, dst)

    def handle_read(self):
        (response, src) = self.manager.read()
        self.cb_fun(self, self.cb_ctx, (response, src), (None, None, None))
        return

    def writable(self):
        return 0

    def handle_connect(self):
        pass

    def handle_close(self):
        self.manager.close()

    def handle_error(self, exc_type=None, exc_value=None, exc_traceback=None):
        if exc_type is None or exc_value is None or exc_traceback is None:
            (exc_type, exc_value, exc_traceback) = sys.exc_info()
        if type(exc_type) == types.ClassType and issubclass(exc_type, ValueError):
            self.cb_fun(self, self.cb_ctx, (None, None), (exc_type, exc_value, exc_traceback))
        else:
            raise
        return

    def poll(self):
        asyncore.poll(self.timeout)