# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aws\minisite\extendcontents\skinextension.py
# Compiled at: 2010-04-08 08:46:16
import zope.interface, zope.component
from archetypes.schemaextender.interfaces import ISchemaModifier, IBrowserLayerAwareExtender
from Products.ATContentTypes.content import folder
from aws.minisite.interfaces import IMiniSiteBrowserLayer

class IMiniSiteExtendable(zope.interface.Interface):
    """A Extendable content item.
    """
    __module__ = __name__


zope.interface.classImplements(folder.ATFolder, IMiniSiteExtendable)

class MiniSiteSchemaModifier(object):
    __module__ = __name__
    zope.interface.implements(ISchemaModifier, IBrowserLayerAwareExtender)
    zope.component.adapts(IMiniSiteExtendable)
    layer = IMiniSiteBrowserLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """change existent fields"""
        schema['local_phantasy_skin'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}