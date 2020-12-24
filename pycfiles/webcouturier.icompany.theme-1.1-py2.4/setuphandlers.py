# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/webcouturier/icompany/theme/setuphandlers.py
# Compiled at: 2008-04-30 11:18:21
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager

def setupVarious(context):
    """Run the various non-Generic Setup profile import steps."""
    portal = context.getSite()
    configurePortlets(portal)


def configurePortlets(portal):
    leftColumn = getUtility(IPortletManager, name='plone.leftcolumn', context=portal)
    left = getMultiAdapter((portal, leftColumn), IPortletAssignmentMapping, context=portal)
    if 'navigation' in left:
        navigation = left['navigation']
        navigation.topLevel = 2