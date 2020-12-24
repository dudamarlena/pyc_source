# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\QuillsRemoteBlogging\tests\base.py
# Compiled at: 2008-06-04 06:25:04
"""Base class for integration tests, based on ZopeTestCase and PloneTestCase.
Note that importing this module has various side-effects: it registers a set of
products with Zope, and it sets up a sandbox Plone site with the appropriate
products installed.
"""
from Testing import ZopeTestCase
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite
from Products.CMFCore.utils import getToolByName
from quills.remoteblogging.interfaces import IUIDManager
ZopeTestCase.installProduct('Quills')
ZopeTestCase.installProduct('QuillsRemoteBlogging')
ZopeTestCase.installProduct('MetaWeblogPASPlugin')
setupPloneSite(products=['Quills', 'MetaWeblogPASPlugin', 'QuillsRemoteBlogging'])

class QuillsRemoteBloggingDocTestCase(PloneTestCase):
    """Base class for integration tests for the 'QuillsRemoteBlogging' product.
    This may provide specific set-up and tear-down operations, or provide
    convenience methods.
    """
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory('Weblog', id='weblog')
        self.mwenabled = self.portal.weblog
        self.appkey = IUIDManager(self.mwenabled).getUID()
        self.blogid = self.appkey
        mtool = getToolByName(self.portal, 'portal_membership')
        self.bloguserid = mtool.getAuthenticatedMember().getId()