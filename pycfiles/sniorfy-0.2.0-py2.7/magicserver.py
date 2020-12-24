# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sniorfy/magicserver.py
# Compiled at: 2012-06-29 04:53:57
import sniorfy.rpc, sniorfy.ioloop

class Application(sniorfy.rpc.Application):

    def __init__(self, server, request_callback):
        self.server = server
        sniorfy.rpc.Application.__init__(self, MagicHandler)


class MagicHandler(sniorfy.rpc.RequestHandler):

    def deal(self):
        argv = self.request.argv
        try:
            fn = getattr(self.request.connection.application.server, argv[0])
        except AttributeError:
            fn = None

        if fn is not None:
            self.appendarg('OK')
            fn(self, argv[1:])
        else:
            self.appendarg('ERR')
            self.appendarg('No such method on server')
        return


class MagicServer(object):

    def __init__(self, port, address=''):
        self.app = Application(self, MagicHandler)
        self.app.listen(port)

    def start(self):
        sniorfy.ioloop.IOLoop.instance().start()