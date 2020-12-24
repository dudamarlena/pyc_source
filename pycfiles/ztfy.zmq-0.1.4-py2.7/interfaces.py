# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/zmq/interfaces.py
# Compiled at: 2012-10-16 12:05:26
from zope.interface import Interface, Attribute
from ztfy.zmq import _

class IZMQProcess(Interface):
    """ZeroMQ process interface"""
    socket_type = Attribute(_('Socket type'))

    def setup(self):
        """Initialize process context and events loop and initialize stream"""
        pass

    def stream(self, sock_type, addr, bind, callback=None, subscribe=''):
        """Create ZMQStream"""
        pass

    def initStream(self):
        """initialize response stream"""
        pass

    def start(self):
        """Start the process"""
        pass

    def stop(self):
        """Stop the process"""
        pass


class IZMQMessageHandler(Interface):
    """ZeroMQ message handler"""
    handler = Attribute(_('Concrete message handler'))