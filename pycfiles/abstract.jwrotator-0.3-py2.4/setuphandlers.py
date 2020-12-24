# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/abstract/jwrotator/setuphandlers.py
# Compiled at: 2008-07-09 06:34:27
from Products.CMFPlone.utils import getToolByName

def addViewMethod(context):
    site = context.getSite()
    type_tool = getToolByName(site, 'portal_types')
    view_types = ['Folder', 'Topic', 'Large Plone Folder']
    for view_type in view_types:
        folder_view_methods = list(type_tool[view_type].view_methods)
        if 'jwrotator_view' not in folder_view_methods:
            folder_view_methods.append('jwrotator_view')
            type_tool[view_type].view_methods = tuple(folder_view_methods)