# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/docs/source/../../ooni/nettests/examples/example_dnst.py
# Compiled at: 2016-03-17 16:00:08
from ooni.templates import dnst

class ExampleDNSTest(dnst.DNSTest):
    inputFile = [
     'file', 'f', None, 'foobar']

    def test_a_lookup(self):

        def gotResult(result):
            print result

        d = self.performALookup('torproject.org', ('8.8.8.8', 53))
        d.addCallback(gotResult)
        return d