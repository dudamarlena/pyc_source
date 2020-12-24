# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pygnet/protocol.py
# Compiled at: 2007-07-24 04:55:08
import cerealizer as encoder
from twisted.protocols import basic

class GameProtocol(basic.Int32StringReceiver):

    def connectionMade(self):
        self.factory.new_connection(self)

    def connectionLost(self, reason):
        self.factory.lost_connection(self)

    def stringReceived(self, data):
        obj = encoder.loads(data)
        self.factory.receive_object(self, obj)

    def send_object(self, obj):
        data = encoder.dumps(obj)
        self.sendString(data)