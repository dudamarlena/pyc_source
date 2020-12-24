# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\QuillsRemoteBlogging\tests\base.py
# Compiled at: 2008-06-04 06:25:04
__doc__ = 'Base class for integration tests, based on ZopeTestCase and PloneTestCase.\nNote that importing this module has various side-effects: it registers a set of\nproducts with Zope, and it sets up a sandbox Plone site with the appropriate\nproducts installed.\n'
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