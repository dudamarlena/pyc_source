# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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