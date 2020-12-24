# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentmigrationui/allmigrations/documentToStructuredDocument.py
# Compiled at: 2010-08-19 03:37:16
from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import ATItemMigrator
from collective.contentmigrationui.interfaces import IContentMigrator
from zope.interface import implements
from collective.contentmigrationui.utils import BASE_AT_PROPERTIES

class DocumentToStructuredDocument(object, ATItemMigrator):
    """Migrate the old item type to the new item type
    """
    __module__ = __name__
    implements(IContentMigrator)
    walker = CustomQueryWalker
    src_meta_type = 'ATDocument'
    src_portal_type = 'Document'
    dst_meta_type = 'Structured Document'
    dst_portal_type = 'Structured Document'
    description = 'Document to Structured Document'
    safeMigration = True

    def __init__(self, *args, **kwargs):
        ATItemMigrator.__init__(self, *args, **kwargs)
        self.fields_map = BASE_AT_PROPERTIES


DocToStructDocMigrator = DocumentToStructuredDocument