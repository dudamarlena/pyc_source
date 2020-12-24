# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/postfeeds/interfaces/postfeed.py
# Compiled at: 2009-10-14 10:31:38
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from csci.postfeeds import postfeedsMessageFactory as _

class Ipostfeed(Interface):
    """Post feeds from here"""
    __module__ = __name__
    news_onoff = schema.Bool(title=_('Post a news item for posts?'), required=False, description=_('check box to keep a site record of posts'))
    lastpost = schema.Text(title=_('Last post captured'), required=False, description=_('This is the last post captured from the feed'))
    t_pass = schema.TextLine(title=_('Twitter Password'), required=False, description=_('password to twitter'))
    t_uname = schema.TextLine(title=_('Twitter Username'), required=False, description=_('enter username here'))
    t_onoff = schema.Bool(title=_('Post to Twitter'), required=False, description=_('Post to twitter'))
    feedurl = schema.TextLine(title=_('Feed URL'), required=True, description=_('http://.......'))