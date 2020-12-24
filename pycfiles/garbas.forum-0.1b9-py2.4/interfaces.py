# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/garbas/forum/interfaces.py
# Compiled at: 2008-08-15 09:29:25
from zope.interface import Interface

class IForum(Interface):
    """forum content"""
    __module__ = __name__


class IForumTopic(Interface):
    """forum topic content"""
    __module__ = __name__


class IForumPost(Interface):
    """forum post content"""
    __module__ = __name__


class IForumNotifiable(Interface):
    """ forum notifiable """
    __module__ = __name__


class IForumNotification(Interface):
    """ forim notification """
    __module__ = __name__