# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\zope\qotd.py
# Compiled at: 2019-08-29 22:24:39
# Size of source mod 2**32: 586 bytes
"""
A simple Quote of the Day server
"""
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class QOTD(Protocol):

    def connectionMade(self):
        self.transport.write(b'An apple a day keeps the doctor away\r\n')
        self.transport.loseConnection()


factory = Factory()
factory.protocol = QOTD
portNum = 8007
reactor.listenTCP(portNum, factory)
print('Listening on port', portNum)
reactor.run()