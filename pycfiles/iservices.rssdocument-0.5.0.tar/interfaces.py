# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erik/Develop/amlo/src/iservices.rssdocument/iservices/rssdocument/interfaces.py
# Compiled at: 2012-05-03 22:31:07
from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface
from zope import schema
from iservices.rssdocument import RSSDocumentMessageFactory as _

class IRSSDocumentLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 Layer for this product
    """
    pass


class IRSSDocument(Interface):
    """
    A Plone document that embedds a RSS feed with JQuery
    """
    title = schema.TextLine(title=_('RSS Feed Name'), description=_('A descriptive name for the RSS Feed such as "My brand new Blog"'), required=True)
    rsslink = schema.TextLine(title=_('RSS URL'), description=_('The URL of the RSS Feed'), required=True)
    max_entries = schema.Int(title=_('Max Entries'), description=_('Maximum Number of entries to show'), required=True)