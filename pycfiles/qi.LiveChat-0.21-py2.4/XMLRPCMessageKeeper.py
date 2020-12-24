# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/LiveChat/XMLRPCMessageKeeper.py
# Compiled at: 2008-07-25 11:17:40
from zope.interface import implements
from zope.component import getUtility
from zope.app.component.hooks import getSite
from qi.LiveChat.interfaces import IMessageKeeper
from xmlrpclib import Server

class XMLRPCMessageKeeper(object):
    """
        """
    __module__ = __name__
    implements(IMessageKeeper)

    def __init__(self):
        """
                """
        self.rpcserver = Server('http://localhost:8000')

    def login(self, chatUID, userID):
        """
                """
        return self.rpcserver.login(chatUID, userID)

    def logout(self, chatUID, userID):
        """
                """
        self.rpcserver.logout(chatUID, userID)

    def sendMessage(self, chatUID, userID, message):
        """
                """
        return self.rpcserver.sendMessage(chatUID, userID, message)

    def update(self, chatUID, userID):
        """
                """
        return self.rpcserver.update(chatUID, userID)