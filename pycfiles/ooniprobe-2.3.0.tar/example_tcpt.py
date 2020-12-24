# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/docs/source/../../ooni/nettests/examples/example_tcpt.py
# Compiled at: 2016-03-17 16:00:08
from twisted.internet.error import ConnectionRefusedError
from ooni.utils import log
from ooni.templates import tcpt

class ExampleTCPT(tcpt.TCPTest):

    def test_hello_world(self):

        def got_response(response):
            print 'Got this data %s' % response

        def connection_failed(failure):
            failure.trap(ConnectionRefusedError)
            print 'Connection Refused'

        self.address = '127.0.0.1'
        self.port = 57002
        payload = 'Hello World!\n\r'
        d = self.sendPayload(payload)
        d.addErrback(connection_failed)
        d.addCallback(got_response)
        return d