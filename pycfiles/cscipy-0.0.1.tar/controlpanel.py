# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/csci/tweetsite/interfaces/controlpanel.py
# Compiled at: 2009-11-17 10:42:23
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from csci.tweetsite import tweetsiteMessageFactory as _

class IcontrolPanel(Interface):
    """create and manage user accounts"""
    __module__ = __name__
    lastpost = schema.TextLine(title=_('Last update'), required=False, description=_('Time of last update'))
    premiumlist = schema.List(title=_('Premium Feeds'), required=False, description=_('Select Premium feeds'))