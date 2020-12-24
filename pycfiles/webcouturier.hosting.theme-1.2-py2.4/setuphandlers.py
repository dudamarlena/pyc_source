# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/webcouturier/hosting/theme/setuphandlers.py
# Compiled at: 2008-07-25 04:13:56
from zope.component import getMultiAdapter, getUtility
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

def setupVarious(context):
    if context.readDataFile('webcouturier.hosting.theme_various.txt') is None:
        return
    logger = context.getLogger('webcouturier.hosting.theme')
    portal = context.getSite()
    removeRightPortlets(logger, portal)
    return


def removeRightPortlets(logger, portal):
    logger.info('We need to un-assign portlets for the right column.')
    rightColumn = getUtility(IPortletManager, name='plone.rightcolumn', context=portal)
    right = getMultiAdapter((portal, rightColumn), IPortletAssignmentMapping, context=portal)
    for portlet in right:
        del right[portlet]
        logger.info('Un-assigned %s portlet.' % portlet)