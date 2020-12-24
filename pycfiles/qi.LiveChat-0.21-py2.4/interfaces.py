# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/LiveChat/interfaces.py
# Compiled at: 2008-07-25 11:17:40
from zope.interface import Interface

class ILiveChat(Interface):
    """
    Marker interface for LiveChat
    """
    __module__ = __name__


class IMessageKeeper(Interface):
    """
        Message keeper utility interface
        """
    __module__ = __name__

    def login(chatroom, user):
        """
                """
        pass

    def logout(chatroom, user):
        """
                """
        pass

    def sendMessage(chatroom, user, message):
        """
                """
        pass

    def update(chatroom, user):
        """
                """
        pass