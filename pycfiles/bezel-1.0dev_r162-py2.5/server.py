# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bezel/networking/server.py
# Compiled at: 2009-02-25 04:20:27
import logging
USE_AVAHI = False
USE_BONJOUR = False
try:
    import avahi, dbus
except ImportError:
    logging.warn('Avahi could not be imported.')
else:
    USE_AVAHI = True

try:
    import pybonjour
except ImportError:
    logging.warn('PyBonjour could not be imported.')
else:
    USE_BONJOUR = True

import SocketServer

class TCPServer(SocketServer.TCPServer, object):
    __doc__ = SocketServer.TCPServer.__doc__


class UDPServer(SocketServer.UDPServer, object):
    __doc__ = SocketServer.UDPServer.__doc__


class GameServer(SocketServer.ThreadingMixIn, object):

    def __init__(self, engine, *args, **kwargs):
        self.engine = engine
        super(GameServer, self).__init__(*args, **kwargs)


class BaseZeroconfMixin(object):

    def __init__(self, name, stype, *args, **kwargs):
        self.name = name
        self.stype = stype
        self.domain = kwargs.pop('domain', '')
        self.text = kwargs.pop('text', '')
        super(BaseZeroconfMixin, self).__init__(*args, **kwargs)


if USE_AVAHI:

    class AvahiMixin(BaseZeroconfMixin):
        """
        A mixin which adds Avahi publishing to a TCP server.
        """

        def server_bind(self):
            host = ''
            port = self.server_address[1]
            super(AvahiMixin, self).server_bind()
            bus = dbus.SystemBus()
            server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER), avahi.DBUS_INTERFACE_SERVER)
            group = dbus.Interface(bus.get_object(avahi.DBUS_NAME, server.EntryGroupNew()), avahi.DBUS_INTERFACE_ENTRY_GROUP)
            group.AddService(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC, dbus.UInt32(0), self.name, self.stype, self.domain, host, dbus.UInt16(port), self.text)
            group.Commit()
            self.group = group

        def server_close(self):
            super(AvahiMixin, self).server_close()
            self.group.Reset()


if USE_BONJOUR:

    class BonjourMixin(BaseZeroconfMixin):

        def server_bind(self):
            super(BonjourMixin, self).server_bind()
            self.service = pybonjour.DNSServiceRegister(name=self.name, regtype=self.stype, port=self.server_address[1])

        def server_close(self):
            super(BonjourMixin, self).server_close()
            self.service.close()
            self.service = None
            return


if USE_AVAHI:
    ServiceMixin = AvahiMixin
elif USE_BONJOUR:
    ServiceMixin = BonjourMixin