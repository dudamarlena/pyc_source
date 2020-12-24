# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vinny.ly/workspace/cloud-metrics/blueflood-carbon-forwarder/tests/http_server_mock.py
# Compiled at: 2016-05-31 16:44:01
import sys, time
from twisted.web import resource, server
from twisted.internet import reactor, endpoints

class MockServerHandler(resource.Resource):
    isLeaf = True

    def __init__(self, cv=None):
        resource.Resource.__init__(self)
        self.cv = cv
        self.data = []
        self.reply = []
        self.default_reply = (200, '', {})

    def should_reply_once(self, status, response, headers):
        self.reply.append((status, response, headers))

    def should_reply_forever(self, status, response, headers):
        self.default_reply = (
         status, response, headers)

    def reset_to_default_reply(self):
        self.reply = []

    def _get_next_reply(self):
        code, response, headers = self.reply[0] if self.reply else self.default_reply
        try:
            del self.reply[0]
        except IndexError:
            pass

        return (code, response, headers)

    def render_POST(self, request):
        data = request.content.read()
        self.data += [
         (time.time(),
          dict([ (k.lower(), v) for k, (v,) in request.requestHeaders.getAllRawHeaders()
          ]), request.path, data)]
        print self.data[(-1)]
        print ''
        if self.cv:
            with self.cv:
                self.cv.notify()
        code, response, headers = self._get_next_reply()
        request.setResponseCode(code)
        for key, value in headers.items():
            request.setHeader(key, value)

        return response


if __name__ == '__main__':
    b_handler = MockServerHandler()
    a_handler = MockServerHandler()
    response = '{"access":{"token":{"id":"eb5e1d9287054898a55439137ea68675","expires":"2014-12-14T22:54:49.574Z","tenant":{"id":"836986","name":"836986"}}}}'
    endpoints.serverFromString(reactor, 'tcp:8000').listen(server.Site(b_handler))
    endpoints.serverFromString(reactor, 'tcp:8001').listen(server.Site(a_handler))
    a_handler.should_reply_forever(200, response, {})
    reactor.run()