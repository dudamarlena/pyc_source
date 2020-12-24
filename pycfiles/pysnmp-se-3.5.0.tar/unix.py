# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/carrier/twisted/dgram/unix.py
# Compiled at: 2019-08-18 17:24:05
import sys
from twisted.internet import reactor
from pysnmp.carrier.base import AbstractTransportAddress
from pysnmp.carrier.twisted.dgram.base import DgramTwistedTransport
from pysnmp.carrier import error
domainName = snmpLocalDomain = (1, 3, 6, 1, 2, 1, 100, 1, 13)

class UnixTransportAddress(str, AbstractTransportAddress):
    __module__ = __name__


class UnixTwistedTransport(DgramTwistedTransport):
    __module__ = __name__
    addressType = UnixTransportAddress
    _lport = None

    def openClientMode(self, iface=''):
        try:
            self._lport = reactor.connectUNIXDatagram(iface, self)
        except Exception:
            raise error.CarrierError(sys.exc_info()[1])

        return self

    def openServerMode(self, iface):
        try:
            self._lport = reactor.listenUNIXDatagram(iface, self)
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


UnixTransport = UnixTwistedTransport