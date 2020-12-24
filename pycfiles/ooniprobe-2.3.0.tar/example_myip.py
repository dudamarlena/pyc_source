# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/docs/source/../../ooni/nettests/examples/example_myip.py
# Compiled at: 2016-03-17 16:00:08
from ooni.templates import httpt

class MyIP(httpt.HTTPTest):
    inputs = [
     'https://check.torproject.org']

    def test_lookup(self):
        return self.doRequest(self.input)

    def processResponseBody(self, body):
        import re
        regexp = 'Your IP address appears to be: <b>(.+?)<\\/b>'
        match = re.search(regexp, body)
        try:
            self.report['myip'] = match.group(1)
        except:
            self.report['myip'] = None

        return