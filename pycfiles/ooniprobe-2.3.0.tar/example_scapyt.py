# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/docs/source/../../ooni/nettests/examples/example_scapyt.py
# Compiled at: 2016-03-17 16:00:08
from twisted.python import usage
from scapy.all import IP, ICMP
from ooni.templates import scapyt

class UsageOptions(usage.Options):
    optParameters = [
     [
      'target', 't', '8.8.8.8', 'Specify the target to ping']]


class ExampleICMPPingScapy(scapyt.BaseScapyTest):
    name = 'Example ICMP Ping Test'
    usageOptions = UsageOptions

    def test_icmp_ping(self):

        def finished(packets):
            print packets
            answered, unanswered = packets
            for snd, rcv in answered:
                rcv.show()

        packets = IP(dst=self.localOptions['target']) / ICMP()
        d = self.sr(packets)
        d.addCallback(finished)
        return d