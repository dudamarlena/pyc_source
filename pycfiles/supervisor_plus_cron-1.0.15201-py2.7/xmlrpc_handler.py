# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\medusa\xmlrpc_handler.py
# Compiled at: 2015-07-18 10:13:56
VERSION = '$Id: xmlrpc_handler.py,v 1.6 2004/04/21 14:09:24 akuchling Exp $'
import supervisor.medusa.http_server as http_server
try:
    import xmlrpclib
except:
    import xmlrpc.client as xmlrpclib

import sys

class xmlrpc_handler:

    def match(self, request):
        if request.uri[:5] == '/RPC2':
            return 1
        else:
            return 0

    def handle_request(self, request):
        if request.command == 'POST':
            request.collector = collector(self, request)
        else:
            request.error(400)

    def continue_request(self, data, request):
        params, method = xmlrpclib.loads(data)
        try:
            try:
                response = self.call(method, params)
                if type(response) != type(()):
                    response = (
                     response,)
            except:
                response = xmlrpclib.dumps(xmlrpclib.Fault(1, '%s:%s' % (sys.exc_info()[0], sys.exc_info()[1])))
            else:
                response = xmlrpclib.dumps(response, methodresponse=1)

        except:
            request.error(500)
        else:
            request['Content-Type'] = 'text/xml'
            request.push(response)
            request.done()

    def call(self, method, params):
        raise Exception('NotYetImplemented')


class collector:
    """gathers input for POST and PUT requests"""

    def __init__(self, handler, request):
        self.handler = handler
        self.request = request
        self.data = []
        cl = request.get_header('content-length')
        if not cl:
            request.error(411)
        else:
            cl = int(cl)
            self.request.channel.set_terminator(cl)

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        self.request.channel.set_terminator('\r\n\r\n')
        self.handler.continue_request(('').join(self.data), self.request)


if __name__ == '__main__':

    class rpc_demo(xmlrpc_handler):

        def call(self, method, params):
            print 'method="%s" params=%s' % (method, params)
            return 'Sure, that works'


    import supervisor.medusa.asyncore_25 as asyncore
    hs = http_server.http_server('', 8000)
    rpc = rpc_demo()
    hs.install_handler(rpc)
    asyncore.loop()