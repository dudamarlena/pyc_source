# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.0-STABLE-i386/egg/infrae/plone/relations/form/tests.py
# Compiled at: 2008-06-13 09:07:00
__author__ = 'sylvain@infrae.com'
__format__ = 'plaintext'
__version__ = '$Id: tests.py 29203 2008-06-13 13:07:10Z sylvain $'
import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.PloneTestCase import ptc
from Products.PloneTestCase.setup import portal_owner, default_password
from Products.Five.testbrowser import Browser
from five.intid.site import add_intids
from plone.app.relations.utils import add_relations
from five.intid.lsm import USE_LSM
from Products.Five import zcml

class TestCase(ptc.FunctionalTestCase):
    __module__ = __name__

    def afterSetUp(self):
        from infrae.plone.relations import form
        zcml.load_config('configure.zcml', form)
        if not USE_LSM:
            from Products.Five.site.metaconfigure import classSiteHook
            from Products.Five.site.localsite import FiveSite
            from zope.interface import classImplements
            from zope.app.component.interfaces import IPossibleSite
            klass = self.portal.__class__
            classSiteHook(klass, FiveSite)
            classImplements(klass, IPossibleSite)
        add_intids(self.portal)
        add_relations(self.portal)

    def createFolder(self, root, title, published=False):
        self.loginAsPortalOwner()
        fid = self.portal.plone_utils.normalizeString(title)
        root.invokeFactory('Folder', fid)
        folder = getattr(root, fid)
        folder.setTitle(title)
        folder.setDescription('Description for %s' % title)
        folder.reindexObject()
        if published:
            self.portal.portal_workflow.doActionFor(folder, 'publish')
        self.logout()

    def createDocument(self, root, title, content):
        self.loginAsPortalOwner()
        did = self.portal.plone_utils.normalizeString(title)
        root.invokeFactory('Document', did)
        document = getattr(root, did)
        document.setTitle(title)
        document.setDescription('Description for %s' % title)
        document.setContentType('text/plain')
        document.setText(content)
        document.reindexObject()
        self.logout()

    def getAuthenticatedBrowser(self):
        browser = Browser()
        browser.open('http://nohost/plone')
        browser.getControl(name='__ac_name').value = portal_owner
        browser.getControl(name='__ac_password').value = default_password
        browser.getControl(name='submit').click()
        return browser


OPTIONS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

def test_suite():
    (
     ptc.setupPloneSite(),)
    return unittest.TestSuite((FunctionalDocFileSuite('README.txt', test_class=TestCase, optionflags=OPTIONS), FunctionalDocFileSuite('README.EXT.txt', test_class=TestCase, optionflags=OPTIONS)))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')