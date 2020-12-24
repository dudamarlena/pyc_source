# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sniorfy/rpc.py
# Compiled at: 2012-06-29 04:53:39
from sniorfy.stpserver import STPServer

class Application(object):

    def __init__(self, request_handler=None):
        self.request_handler = request_handler

    def listen(self, port, address='', **kwargs):
        server = STPServer(self, application=self, **kwargs)
        server.listen(port, address)

    def __call__(self, request):
        if self.request_handler is not None:
            handler = self.request_handler(self, request)
            handler.deal()
            handler.finish()
        return


class RequestHandler(object):

    def __init__(self, application, request, **kwargs):
        self.application = application
        self.request = request

    def _encode(self, value):
        """Return a bytestring representation of the value"""
        if isinstance(value, unicode):
            return value.encode('utf-8', 'strict')
        return str(value)

    def appendarg(self, arg):
        arg = self._encode(arg)
        self.request.connection.stream.write('%d\r\n%s\r\n' % (len(arg), arg))

    def finish(self):
        self.request.connection.stream.write('\r\n')