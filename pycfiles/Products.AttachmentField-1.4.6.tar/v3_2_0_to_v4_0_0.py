# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/Plone-4.3.7-was-4.2.1/zeocluster/src/Products.ATSuccessStory/Products/ATSuccessStory/upgrades/v3_2_0_to_v4_0_0.py
# Compiled at: 2015-12-17 03:22:24
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.component.hooks import getSite
from Products.ATSuccessStory.browser.portlets.successstory import ISuccessStoryPortlet
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignable
from zLOG import LOG, INFO, WARNING
from Products.ATSuccessStory.config import PROJECTNAME
from plone.portlets.constants import USER_CATEGORY
from plone.portlets.constants import GROUP_CATEGORY
from plone.portlets.constants import CONTENT_TYPE_CATEGORY
from plone.portlets.constants import CONTEXT_CATEGORY
import transaction

def fix_search_path(assignement, site, location):
    ss_portlets = [ i for i in assignement.values() if ISuccessStoryPortlet.providedBy(i) ]
    try:
        location = ('/').join(location.getPhysicalPath())
    except:
        pass

    for portlet in ss_portlets:
        if hasattr(portlet.data, 'global_portlet'):
            msg = 'Fixing portlet "%s" for %s' % (portlet.header, location)
            LOG(PROJECTNAME, INFO, msg)
            if not portlet.data.global_portlet:
                search_path = portlet.searchpath
                msg = 'This is not a global portlet, old search path: %s' % search_path
                LOG(PROJECTNAME, INFO, msg)
                if search_path.startswith('/'):
                    search_path = search_path[1:]
                try:
                    ss_folder = site.unrestrictedTraverse(search_path)
                except:
                    break

            else:
                msg = 'This is a global portlet'
                LOG(PROJECTNAME, INFO, msg)
                ss_folder = site
            search_path = ('/').join(ss_folder.getPhysicalPath())
            msg = 'New search path %s' % search_path
            LOG(PROJECTNAME, INFO, msg)
            portlet.data.searchpath = search_path
            del portlet.data.global_portlet
        else:
            msg = 'Portlet "%s" for %s is already updated' % (portlet.header, location)
            LOG(PROJECTNAME, INFO, msg)


def updatePortlets(portal_setup):
    """
    This migration step will search all existing portlets and make the proper
    changes so they keep working
    """
    msg = 'Starting to update portlets'
    LOG(PROJECTNAME, INFO, msg)
    site = getSite()
    pc = getToolByName(site, 'portal_catalog')
    sm = getSiteManager(site)
    registrations = [ r.name for r in sm.registeredUtilities() if IPortletManager == r.provided
                    ]
    locations = pc.searchResults(object_provides=ILocalPortletAssignable.__identifier__)
    for name in registrations:
        column = getUtility(IPortletManager, name=name, context=site)
        for location in locations:
            place = location.getObject()
            assignement = getMultiAdapter((place, column), IPortletAssignmentMapping)
            fix_search_path(assignement, site, place)

        for category in (USER_CATEGORY, GROUP_CATEGORY, CONTENT_TYPE_CATEGORY, CONTEXT_CATEGORY):
            for name, assignement in column.get(category, {}).items():
                fix_search_path(assignement, site, category)

        assignement = getMultiAdapter((site, column), IPortletAssignmentMapping)
        fix_search_path(assignement, site, site)

    transaction.savepoint()