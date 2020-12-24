# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/docs/source/../../ooni/nettests/examples/example_scapyt_yield.py
# Compiled at: 2016-03-17 16:00:08
from twisted.python import usage
from twisted.internet import defer
from scapy.all import IP, ICMP
from ooni.templates import scapyt

class UsageOptions(usage.Options):
    optParameters = [
     [
      'target', 't', None, 'Specify the target to ping']]


class ExampleICMPPingScapyYield(scapyt.BaseScapyTest):
    name = 'Example ICMP Ping Test'
    usageOptions = UsageOptions

    @defer.inlineCallbacks
    def test_icmp_ping(self):
        packets = IP(dst=self.localOptions['target']) / ICMP()
        answered, unanswered = yield self.sr(packets)
        for snd, rcv in answered:
            rcv.show()