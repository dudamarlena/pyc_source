# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neteasy/plone/subnavbar/navbar_contents.py
# Compiled at: 2009-01-16 14:41:17
""" neteasy.plone.subnavbar
    Copyright (C) 2008-9, Jim Nelson <jim.nelson@neteasyinc.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from Products.CMFCore.utils import getToolByName
from AccessControl import ModuleSecurityInfo
modulesecurity = ModuleSecurityInfo()
modulesecurity.declarePublic('getSecondLevelList')

def getSecondLevelList(context):
    context = context.aq_inner
    plone_utils = getToolByName(context, 'plone_utils')
    if context.meta_type == 'Plone Site':
        return {'selected': None, 'contents': []}
    if not plone_utils.isStructuralFolder(context) and context.aq_parent.meta_type == 'Plone Site':
        return {'selected': None, 'contents': []}
    selectedChild = context
    item = context
    itemparent = context.aq_parent
    while itemparent.meta_type != 'Plone Site':
        selectedChild = item
        item = itemparent
        itemparent = item.aq_parent

    basePath = ('/').join(item.getPhysicalPath())
    catalog = getToolByName(context, 'portal_catalog')
    query = {}
    query['sort_on'] = 'getObjPositionInParent'
    query['path'] = {'query': basePath, 'depth': 1}
    searchresults = catalog.searchResults(query)
    results = []
    for searchitem in searchresults:
        obj = searchitem.getObject()
        if not obj.exclude_from_nav() and obj.id != item.defaultView():
            results.append(obj)

    return {'selected': selectedChild, 'contents': results}


modulesecurity.apply(globals())