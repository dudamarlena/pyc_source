# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\zope\qotd.py
# Compiled at: 2016-04-18 03:12:47
# Size of source mod 2**32: 531 bytes
"""
A simple Quote of the Day server
"""
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class QOTD(Protocol):

    def connectionMade(self):
        self.transport.write('An apple a day keeps the doctor away\r\n')
        self.transport.loseConnection()


factory = Factory()
factory.protocol = QOTD
reactor.listenTCP(8007, factory)
reactor.run()