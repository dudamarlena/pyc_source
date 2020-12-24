# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Zpydoc/ZpydocRenderer.py
# Compiled at: 2011-09-28 02:31:46
__doc__ = '$id$'
import AccessControl, Products, inspect
from AccessControl.Permissions import change_configuration, view_management_screens, manage_properties, change_permissions, undo_changes, access_contents_information
try:
    from Products.OrderedFolder.OrderedFolder import OrderedFolder
    Folder = OrderedFolder
except:
    from OFS.Folder import Folder

from zope.interface import classImplements
from interfaces.IRenderer import IZpydocRenderer

class RendererFolder(Folder):
    """ """
    meta_type = 'RendererFolder'
    id = 'renderers'
    title = ''
    manage_options = (
     Folder.manage_options[0],) + Folder.manage_options[2:]
    index_html = None

    def all_meta_types(self):
        possibles = filter(lambda x: x['name'] in ('pydocRenderer', 'PythonRenderer', 'ZopeRenderer'), Products.meta_types)
        definites = map(lambda x: x.meta_type, self.objectValues())
        return filter(lambda x, y=definites: x['name'] not in y, possibles)


AccessControl.class_init.InitializeClass(RendererFolder)