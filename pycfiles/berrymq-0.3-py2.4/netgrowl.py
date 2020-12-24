# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/berrymq/adapter/growl/netgrowl.py
# Compiled at: 2009-10-02 07:17:32
"""Growl 0.6 Network Protocol Client for Python

modified by SHIBUKAWA Yoshiki to follow PEP-8 and remove deprecate warning.
"""
__version__ = '0.6'
__author__ = 'Rui Carmo (http://the.taoofmac.com)'
__copyright__ = '(C) 2004 Rui Carmo. Code under BSD License.'
__contributors__ = 'Ingmar J Stein (Growl Team)'
import struct
try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5

from socket import AF_INET, SOCK_DGRAM, socket
GROWL_UDP_PORT = 9887
GROWL_PROTOCOL_VERSION = 1
GROWL_TYPE_REGISTRATION = 0
GROWL_TYPE_NOTIFICATION = 1

class GrowlRegistrationPacket:
    """Builds a Growl Network Registration packet.
       Defaults to emulating the command-line growlnotify utility."""
    __module__ = __name__

    def __init__(self, application='growlnotify', password=None):
        self.notifications = []
        self.defaults = []
        self.application = application.encode('utf-8')
        self.password = password

    def addNotification(self, notification='Command-Line Growl Notification', enabled=True):
        """Adds a notification type and sets whether it is enabled on the GUI"""
        self.notifications.append(notification)
        if enabled:
            self.defaults.append(len(self.notifications) - 1)

    def payload(self):
        """Returns the packet payload."""
        self.data = struct.pack('!BBH', GROWL_PROTOCOL_VERSION, GROWL_TYPE_REGISTRATION, len(self.application))
        self.data += struct.pack('BB', len(self.notifications), len(self.defaults))
        self.data += self.application
        for notification in self.notifications:
            encoded = notification.encode('utf-8')
            self.data += struct.pack('!H', len(encoded))
            self.data += encoded

        for default in self.defaults:
            self.data += struct.pack('B', default)

        self.checksum = md5()
        self.checksum.update(self.data)
        if self.password:
            self.checksum.update(self.password)
        self.data += self.checksum.digest()
        return self.data


class GrowlNotificationPacket:
    """Builds a Growl Network Notification packet.
    Defaults to emulating the command-line growlnotify utility."""
    __module__ = __name__

    def __init__(self, application='growlnotify', notification='Command-Line Growl Notification', title='Title', description='Description', priority=0, sticky=False, password=None):
        self.application = application.encode('utf-8')
        self.notification = notification.encode('utf-8')
        self.title = title.encode('utf-8')
        self.description = description.encode('utf-8')
        flags = (priority & 7) * 2
        if priority < 0:
            flags |= 8
        if sticky:
            flags = flags | 1
        self.data = struct.pack('!BBHHHHH', GROWL_PROTOCOL_VERSION, GROWL_TYPE_NOTIFICATION, flags, len(self.notification), len(self.title), len(self.description), len(self.application))
        self.data += self.notification
        self.data += self.title
        self.data += self.description
        self.data += self.application
        self.checksum = md5()
        self.checksum.update(self.data)
        if password:
            self.checksum.update(password)
        self.data += self.checksum.digest()

    def payload(self):
        """Returns the packet payload."""
        return self.data


if __name__ == '__main__':
    print 'Starting Unit Test'
    print ' - please make sure Growl is listening for network notifications'
    addr = ('localhost', GROWL_UDP_PORT)
    s = socket(AF_INET, SOCK_DGRAM)
    print "Assembling registration packet like growlnotify's (no password)"
    p = GrowlRegistrationPacket()
    p.addNotification()
    print 'Sending registration packet'
    s.sendto(p.payload(), addr)
    import time
    time.sleep(3)
    print 'Assembling standard notification packet'
    p = GrowlNotificationPacket()
    print 'Sending standard notification packet'
    s.sendto(p.payload(), addr)
    print 'Assembling priority -2 (Very Low) notification packet'
    p = GrowlNotificationPacket(priority=-2)
    print 'Sending priority -2 notification packet'
    s.sendto(p.payload(), addr)
    print 'Assembling priority 2 (Very High) sticky notification packet'
    p = GrowlNotificationPacket(priority=2, sticky=True)
    print 'Sending priority 2 (Very High) sticky notification packet'
    s.sendto(p.payload(), addr)
    s.close()
    print 'Done.'