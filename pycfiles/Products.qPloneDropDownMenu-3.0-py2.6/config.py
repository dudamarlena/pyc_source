# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/qPloneDropDownMenu/config.py
# Compiled at: 2010-07-19 08:14:01
try:
    from Products.CMFCore import permissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions as permissions

MANAGE_PERMISSION = permissions.ManagePortal
PROJECT_NAME = 'qPloneDropDownMenu'
UNIQUE_ID = 'portal_dropdownmenu'
PROPERTY_SHEET = 'dropdownmenu_properties'
PROPERTY_FIELD = 'menu'