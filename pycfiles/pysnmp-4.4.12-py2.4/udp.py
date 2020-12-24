# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/carrier/twisted/dgram/udp.py
# Compiled at: 2019-08-18 17:24:05
import sys
from twisted.internet import reactor
from pysnmp.carrier.base import AbstractTransportAddress
from pysnmp.carrier.twisted.dgram.base import DgramTwistedTransport
from pysnmp.carrier import error
domainName = snmpUDPDomain = (1, 3, 6, 1, 6, 1, 1)

class UdpTransportAddress(tuple, AbstractTransportAddress):
    __module__ = __name__


class UdpTwistedTransport(DgramTwistedTransport):
    __module__ = __name__
    addressType = UdpTransportAddress
    _lport = None

    def openClientMode(self, iface=None):
        if iface is None:
            iface = ('', 0)
        try:
            self._lport = reactor.listenUDP(iface[1], self, iface[0])
        except Exception:
            raise error.CarrierError(sys.exc_info()[1])

        return self

    def openServerMode(self, iface):
        try:
            self._lport = reactor.listenUDP(iface[1], self, iface[0])
        except Exception:
            raise error.CarrierError(sys.exc_info()[1])

        return self

    def closeTransport(self):
        if self._lport is not None:
            d = self._lport.stopListening()
            if d:
                d.addCallback(lambda x: None)
            DgramTwistedTransport.closeTransport(self)
        return


UdpTransport = UdpTwistedTransport