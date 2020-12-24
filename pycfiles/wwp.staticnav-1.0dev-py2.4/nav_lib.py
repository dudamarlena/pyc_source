# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/portlet/staticnav/nav_lib.py
# Compiled at: 2009-07-10 11:04:28
from Products.CMFCore.utils import getToolByName
from plone.browserlayer import utils
import string
from AccessControl import getSecurityManager
from Acquisition import aq_parent

def nav_init(context, basePath=None, update_titles=False):
    urltool = getToolByName(context, 'portal_url')
    catalog = getToolByName(context, 'portal_catalog')
    levels = 1
    types = None
    nav_dir = {}
    nav_list = []
    nav_status = 'Started...\n'
    print basePath
    if basePath is None:
        basePath = urltool.getPortalPath()
        print '----this works----'
    elif basePath == 'None':
        basePath = urltool.getPortalPath()
    elif basePath == '':
        basePath = urltool.getPortalPath()
    print basePath
    nav_list.append(basePath)
    nav_status = nav_status + 'Update from: ' + basePath
    for nav_item in nav_list:
        basePath = nav_item
        query = {}
        query['sort_on'] = 'getObjPositionInParent'
        if levels is not None and levels > 0:
            query['path'] = {'query': basePath, 'depth': levels}
        else:
            query['path'] = basePath
        if types:
            query['portal_type'] = types
        results = catalog.searchResults(query)
        nav_dir[basePath] = []
        app = context.restrictedTraverse(basePath)
        if '/' + str(app.virtual_url_path()) == urltool.getPortalPath():
            pass
        else:
            parent = aq_parent(app)
            nav_dir[str(basePath)].append(['- Back -', app.Title, app.Type, parent.absolute_url()])
        for r in results:
            link_name = r.getPath()
            link_name = link_name.split('/')
            link_name = link_name[(-1)]
            link_name = link_name.split('.')
            link_name = link_name[0]
            link_name = link_name.split('-')
            i = 0
            for word in link_name:
                word = word.capitalize()
                link_name[i] = word
                i += 1

            link_name = string.join(link_name)
            app = context.restrictedTraverse(r.getPath())
            obj_viewed = [ x for x in app.permissionsOfRole('Anonymous') if x['name'] == 'View' ]
            if obj_viewed[0]['selected'] == 'SELECTED':
                nav_dir[str(basePath)].append([link_name, r.Title, r.Type, r.getURL()])
            if update_titles:
                app.setTitle(link_name)
                app.reindexObject()
            if r.Type == 'Folder' or r.Type == 'Large Folder':
                nav_list.append(r.getPath())
                basePath

    nav_status = nav_status + 'Re-Indexing and Renaming Complete'
    return (nav_status, nav_dir)