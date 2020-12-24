# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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