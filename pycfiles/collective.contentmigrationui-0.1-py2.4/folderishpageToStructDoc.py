# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentmigrationui/allmigrations/folderishpageToStructDoc.py
# Compiled at: 2010-08-19 03:37:24
from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import ATFolderMigrator, ATItemMigrator
from collective.contentmigrationui.interfaces import IContentMigrator
from zope.interface import implements
from collective.contentmigrationui.utils import BASE_AT_PROPERTIES
from Products.CMFCore.utils import getToolByName
from zExceptions import BadRequest
from OFS.interfaces import IOrderedContainer

class FolderishPageToStructuredDocument(object, ATFolderMigrator, ATItemMigrator):
    """Migrate the old item type to the new item type
    """
    __module__ = __name__
    implements(IContentMigrator)
    walker = CustomQueryWalker
    src_meta_type = 'FolderishPage'
    src_portal_type = 'FolderishPage'
    dst_meta_type = 'Structured Document'
    dst_portal_type = 'Structured Document'
    description = 'FolderishPage to Structured Document'
    safeMigration = True

    def __init__(self, *args, **kwargs):
        ATFolderMigrator.__init__(self, *args, **kwargs)
        ATItemMigrator.__init__(self, *args, **kwargs)
        self.fields_map = BASE_AT_PROPERTIES

    def migrate_children(self):
        """Copy childish objects from the old folder to the new one
        """
        subobjs = self.subobjs
        pc = getToolByName(self.new, 'portal_catalog')
        for (id, obj) in subobjs.items():
            __traceback_info__ = __traceback_info__ = (
             'migrate_children', self.old, self.orig_id, 'Migrating subobject %s' % id)
            try:
                if obj.portal_type == 'Link':
                    if not getattr(self.new, 'links', None):
                        self.new.invokeFactory(type_name='Folder Deepening', id='links', title='Links')
                    linksFolder = getattr(self.new, 'links', None)
                    linksFolder._setObject(id, obj, set_owner=0)
                elif obj.portal_type == 'File':
                    if not getattr(self.new, 'files', None):
                        self.new.invokeFactory(type_name='Folder Deepening', id='files', title='Files')
                    filesFolder = getattr(self.new, 'files', None)
                    filesFolder._setObject(id, obj, set_owner=0)
                else:
                    self.new._setObject(id, obj, set_owner=0)
                if obj.portal_type == 'Link' or obj.portal_type == 'File':
                    completePath = ('/').join(self.new.getPhysicalPath()) + '/' + ('/').join(obj.getPhysicalPath())
                    results = pc(path=completePath)
                    if len(results) > 0:
                        pc.uncatalog_object(results[0].getPath())
            except BadRequest:
                print '\nEXCEPTION\n'
                if id in self.new.objectIds():
                    self.new._delOb(id)
                    if getattr(self.new, '_objects', None) is not None:
                        self.new._objects = tuple([ o for o in self.new._objects if o['id'] != id ])
                    self.new._setObject(id, obj, set_owner=0)
                else:
                    raise

        return


FolderishPageToStructDocMigrator = FolderishPageToStructuredDocument