# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/qPloneDropDownMenu/setuphandlers.py
# Compiled at: 2010-07-19 08:14:01
from Products.CMFCore.utils import getToolByName
from utils import updateMenu
from config import PROPERTY_SHEET, PROPERTY_FIELD

def installMenu(context):
    if context.readDataFile('qplonedropdownmenu_various.txt') is None:
        return
    else:
        site = context.getSite()
        portal_props = getToolByName(site, 'portal_properties')
        prop_sheet = getattr(portal_props.aq_base, PROPERTY_SHEET, None)
        if prop_sheet is not None:
            prop_field = getattr(prop_sheet.aq_base, PROPERTY_FIELD, None)
            if prop_field is not None:
                return
        updateMenu(site)
        return