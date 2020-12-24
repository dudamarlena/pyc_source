# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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