# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/qPloneDropDownMenu/DropDownMenuTool.py
# Compiled at: 2010-07-19 08:14:01
from App.class_init import InitializeClass
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import UniqueObject, getToolByName
from utils import updateMenu
from config import MANAGE_PERMISSION, PROJECT_NAME, UNIQUE_ID

class DropDownMenuTool(UniqueObject, SimpleItem):
    meta_type = 'DropDownMenu Tool'
    id = UNIQUE_ID
    title = 'DropDown Menu Tool'
    security = ClassSecurityInfo()
    security.declareProtected(MANAGE_PERMISSION, 'regenerateMenu')

    def regenerateMenu(self):
        portal = getToolByName(self, 'portal_url').getPortalObject()
        updateMenu(portal)


InitializeClass(DropDownMenuTool)