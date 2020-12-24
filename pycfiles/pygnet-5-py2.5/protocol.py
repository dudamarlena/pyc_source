# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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