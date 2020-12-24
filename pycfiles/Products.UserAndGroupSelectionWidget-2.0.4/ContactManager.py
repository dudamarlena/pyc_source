# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/UpfrontContacts/ContactManager.py
# Compiled at: 2010-03-10 13:47:45
from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from Products.Archetypes.public import *
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
schema = BaseBTreeFolderSchema.copy()

class ContactManager(BrowserDefaultMixin, BaseBTreeFolder):
    """ Manage companies and people """
    __module__ = __name__
    security = ClassSecurityInfo()
    portal_type = meta_type = 'ContactManager'
    archetype_name = 'Contact Manager'
    schema = schema
    allowed_content_types = ()
    content_icon = 'contactmanager.png'
    immediate_view = 'contactmanager_view'
    default_view = 'contactmanager_view'
    global_allow = 1
    filter_content_types = 0
    _at_rename_after_creation = True
    __implements__ = BaseFolder.__implements__ + BrowserDefaultMixin.__implements__
    actions = ({'id': 'view', 'name': 'View', 'action': 'string:${object_url}/contactmanager_view', 'permissions': (permissions.View,)},)


registerType(ContactManager)