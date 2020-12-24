# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/csci/tweetsite/interfaces/onlinefeed.py
# Compiled at: 2009-11-18 05:17:02
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from csci.tweetsite import tweetsiteMessageFactory as _

class IonlineFeed(Interface):
    """Feed to manage"""
    __module__ = __name__
    categories = schema.List(title=_('Categories to post in'), required=True, description=_('select from list'))
    active_feed = schema.Bool(title=_('Active'), required=False, description=_('activate/deactivate feed'))
    feed_username = schema.TextLine(title=_('Feed Username'), required=True, description=_('enter the username of feed to manage'))