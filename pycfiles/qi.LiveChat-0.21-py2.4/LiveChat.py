# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/LiveChat/content/LiveChat.py
# Compiled at: 2008-07-25 11:17:40
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from qi.LiveChat.interfaces import ILiveChat
from Products.ATContentTypes.content.schemata import finalizeATCTSchema, ATContentTypeSchema
from Products.ATContentTypes.content.base import ATCTContent
from qi.LiveChat.config import PROJECTNAME
schema = Schema(())
LiveChat_schema = ATContentTypeSchema.copy() + schema.copy()

class LiveChat(ATCTContent):
    """
    """
    __module__ = __name__
    implements(ILiveChat)
    security = ClassSecurityInfo()
    schema = LiveChat_schema

    def __init__(self, *args, **kwargs):
        """
        """
        ATCTContent.__init__(self, *args, **kwargs)


registerType(LiveChat, PROJECTNAME)