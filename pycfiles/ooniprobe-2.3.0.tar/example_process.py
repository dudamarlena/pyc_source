# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: example_process.py
# Compiled at: 2015-12-02 11:37:17
from twisted.internet import defer
from ooni.templates import process

class TestProcessExample(process.ProcessTest):

    @defer.inlineCallbacks
    def test_http_and_dns(self):
        yield self.run(['echo', 'Hello world!'])
        yield self.run(['sleep', '10'])


class TestProcessExample2(process.ProcessTest):

    @defer.inlineCallbacks
    def test_http_and_dns(self):
        yield self.run(['echo', 'Hello fool!'])
        yield self.run(['sleep', '10'])