# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/linkedin/setuphandlers.py
# Compiled at: 2010-04-13 18:59:51
from zope.component import getSiteManager
from collective.linkedin.browser.interfaces import ICollectiveLinkedInManagement
from collective.linkedin.browser.config import LinkedInConfiguration
from collective.linkedin.browser.config import add_company_info_js

def setupVarious(context):
    if context.readDataFile('collective.linkedin_various.txt') is None:
        return
    portal = context.getSite()
    add_company_info_js(portal, overwrite=True)
    sm = getSiteManager()
    if 'linkedin_profile' not in portal.portal_memberdata.propertyIds():
        portal.portal_memberdata.portal_memberdata.manage_addProperty('linkedin_profile', '', 'string')
    if not sm.queryUtility(ICollectiveLinkedInManagement, name='linkedin_config'):
        sm.registerUtility(LinkedInConfiguration(), ICollectiveLinkedInManagement, 'linkedin_config')
    return