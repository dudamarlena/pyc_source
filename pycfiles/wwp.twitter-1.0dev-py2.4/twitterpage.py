# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/twitter/interfaces/twitterpage.py
# Compiled at: 2009-08-07 07:53:08
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from wwp.twitter import twitterMessageFactory as _

class ITwitterPage(Interface):
    """Twitter Page"""
    __module__ = __name__
    numbertodisp = schema.Int(title=_('Number of posts to display'), required=False, description=_('Field description'))
    password = schema.TextLine(title=_('Password'), required=False, description=_('G'))
    username = schema.TextLine(title=_('Twitter Username'), required=False, description=_('Username of feed to display'))