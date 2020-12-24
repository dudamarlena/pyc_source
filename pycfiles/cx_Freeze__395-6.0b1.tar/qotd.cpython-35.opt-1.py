# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\samples\zope\qotd.py
# Compiled at: 2019-08-29 22:24:39
# Size of source mod 2**32: 586 bytes
__doc__ = '\nA simple Quote of the Day server\n'
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class QOTD(Protocol):

    def connectionMade(self):
        self.transport.write('An apple a day keeps the doctor away\r\n')
        self.transport.loseConnection()


factory = Factory()
factory.protocol = QOTD
portNum = 8007
reactor.listenTCP(portNum, factory)
print('Listening on port', portNum)
reactor.run()