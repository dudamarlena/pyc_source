# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/webcouturier/city/theme/setuphandlers.py
# Compiled at: 2008-06-29 10:06:06
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletManager
from webcouturier.city.theme.portlets import personaltools

def setupVarious(context):
    """Run the various non-Generic Setup profile import steps."""
    portal = context.getSite()
    configurePortlets(portal)


def configurePortlets(portal):
    leftColumn = getUtility(IPortletManager, name='plone.leftcolumn', context=portal)
    left = getMultiAdapter((portal, leftColumn), IPortletAssignmentMapping, context=portal)
    if 'personaltools' not in left:
        left['personaltools'] = personaltools.Assignment()