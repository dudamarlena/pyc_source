# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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