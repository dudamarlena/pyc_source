# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/docs/source/../../ooni/nettests/examples/example_httpt.py
# Compiled at: 2016-03-17 16:00:08
from ooni.utils import log
from ooni.templates import httpt

class ExampleHTTP(httpt.HTTPTest):
    name = 'Example HTTP Test'
    author = 'Arturo Filastò'
    version = 0.1
    inputs = [
     'http://google.com/', 'http://wikileaks.org/',
     'http://torproject.org/']

    def test_http(self):
        if self.input:
            url = self.input
            return self.doRequest(url)
        raise Exception('No input specified')

    def processResponseBody(self, body):
        if 'blocked' in body:
            self.report['censored'] = True
        else:
            self.report['censored'] = False

    def processResponseHeaders(self, headers):
        pass