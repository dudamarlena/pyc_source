# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/xmpp/client/pingpong.py
# Compiled at: 2008-08-01 13:19:37
from twisted.words.xish.domish import Element
from twisted.words.protocols.jabber.client import IQ
import qi.xmpp.client.xmppComm as xmppComm

class PingPong(object):
    """
        XEP 0199: xmpp ping
        http://www.xmpp.org/extensions/xep-0199.html
        Does NOT support pinging, only ponging.
        """
    __module__ = __name__

    def __init__(self, client):
        self.client = client

    def onPing(self, el):
        fr = el['from']
        pid = el['id']
        pong = Element(('jabber:client', 'iq'))
        pong['from'] = self.client.jabberID.full()
        pong['to'] = fr
        pong['id'] = pid
        pong['type'] = result
        xmppComm.sendIq(self.client, pong)
        print 'KAKAKAKAKAKA'