# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/CSSManager/config.py
# Compiled at: 2008-09-18 15:18:08
from Products.CMFCore.permissions import AddPortalContent, View, ManagePortal
from Products.Archetypes.public import DisplayList
ADD_CONTENT_PERMISSION = AddPortalContent
PROJECTNAME = 'CSSManager'
SKINS_DIR = 'skins'
view_permission = View
man_perm = ManagePortal
GLOBALS = globals()
DEPENDENCIES = []
cssmanager_configlet = {'id': 'css_manager', 'appId': 'CSSManager', 'name': 'Theme Configuration Manager', 'action': 'string:$portal_url/prefs_cssmanager_form', 'category': 'Products', 'permission': (ManagePortal,), 'imageUrl': 'css_manager_logo.gif'}