# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/jyu/portalview/content/portalviewcolumnfolder.py
# Compiled at: 2009-11-16 03:44:26
try:
    from Products.LinguaPlone.public import *
except ImportError:
    from Products.Archetypes.atapi import *

from jyu.portalview.interfaces import IPortalViewColumnFolder
from jyu.portalview import config
from jyu.portalview.content.schemata import PortalViewColumnFolderSchema
from zope.interface import implements
from zope.component import adapter

class PortalViewColumnFolder(OrderedBaseFolder):
    """ A simple folderish type containing actual portal views """
    __module__ = __name__
    implements(IPortalViewColumnFolder)
    portal_type = 'Portal View Column Folder'
    schema = PortalViewColumnFolderSchema
    _at_rename_after_creation = True
    title = ATFieldProperty('title')
    description = ATFieldProperty('description')
    width = ATFieldProperty('width')


registerType(PortalViewColumnFolder, config.PROJECTNAME)