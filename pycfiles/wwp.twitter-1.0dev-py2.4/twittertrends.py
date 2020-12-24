# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/twitter/interfaces/twittertrends.py
# Compiled at: 2009-08-10 06:22:18
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from wwp.twitter import twitterMessageFactory as _

class Itwittertrends(Interface):
    """Display top words from twitter"""
    __module__ = __name__
    password = schema.TextLine(title=_('Password'), required=False, description=_('of twitter feed (Optional)'))
    username = schema.TextLine(title=_('Username'), required=False, description=_('Enter username to post tweets in (Optional)'))
    postresults = schema.Bool(title=_('Post results to feed?'), required=False, description=_('enter feed username'))
    trendtype = schema.TextLine(title=_('Type of Twitter Trend'), required=True, description=_('Make your selection'))