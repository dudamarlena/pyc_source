# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/modifier.py
# Compiled at: 2008-10-23 05:55:17
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.interfaces.IModifier import ISaveRetrieveModifier
from Products.CMFEditions.interfaces.IArchivist import ArchivistUnregisteredError
from Products.CMFEditions.Modifiers import ConditionalTalesModifier
from iw.fss.FileSystemStorage import FileSystemStorage
MODIFIER_ID = 'FSSModifier'
modifierAddForm = PageTemplateFile('zmi/modifier_add_form.zpt', globals(), __name__='modifier_add_form')

def manage_addModifier(self, REQUEST=None):
    """Add a modifier for saving versions in FileSystemStorage.
    """
    modifier = Modifier()
    id = MODIFIER_ID
    title = 'A modifier for saving FileSystemStorage versions'
    wrapped = ConditionalTalesModifier(id, modifier, title)
    wrapped.edit(enabled=True, condition='python:True', title=title)
    self.register(id, wrapped)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url() + '/manage_main')
    return


class Modifier(object):
    """
   Save each version of an FSS file into a different file so past versions of
   files are available
    """
    __module__ = __name__
    __implements__ = (
     ISaveRetrieveModifier,)

    def beforeSaveModifier(self, obj, clone):
        for field in obj.Schema().fields():
            if not hasattr(field, 'getStorage'):
                continue
            storage = field.getStorage()
            if not isinstance(storage, FileSystemStorage):
                continue
            rtool = getToolByName(obj, 'portal_repository')
            history = rtool.getHistory(obj)
            version = len(history)
            storage.set(field.getName(), clone.__of__(obj.aq_parent), field.getAccessor(obj)(), mimetype=field.getContentType(obj), field=field, filename=field.getFilename(obj), version=version)

        return ({}, [], [])

    def afterRetrieveModifier(self, obj, repo_clone, preserve=()):
        return ([], [], {})