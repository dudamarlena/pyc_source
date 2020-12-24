# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/slideshowfolder/tests/test_uninstallation.py
# Compiled at: 2008-07-09 00:41:15
from base import SlideshowFolderTestCase
from Products.slideshowfolder.browser import FolderSlideShowView

class TestSlideshowFolderProductUninstall(SlideshowFolderTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.folder.invokeFactory('Folder', id='test1', title='Test Slideshow')
        self.test1 = getattr(self.folder, 'test1')
        view = FolderSlideShowView(self.test1, self.app.REQUEST)
        view.makeSlideshow()

    def testFoldersAreNoLongerSlideshows(self):
        """Uninstall should unslideshow-ify all existing slideshows"""
        view = FolderSlideShowView(self.test1, self.app.REQUEST)
        self.failUnless(view.isSlideshow())
        qi = self.portal.portal_quickinstaller
        if qi.isProductInstalled('slideshowfolder'):
            qi.uninstallProducts(products=['slideshowfolder'])
        self.failUnless(not view.isSlideshow())

    def testObjectActionsGoneAfterUninstall(self):
        """Uninstall shouldn't leave any traces in portal_actions"""
        qi = self.portal.portal_quickinstaller
        if qi.isProductInstalled('slideshowfolder'):
            qi.uninstallProducts(products=['slideshowfolder'])
        action_ids = [ a.id for a in self.portal.portal_actions.listActions() ]
        self.failIf('makeSlideshow' in action_ids)
        self.failIf('unmakeSlideshow' in action_ids)
        self.failIf('slideshow_settings' in action_ids)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSlideshowFolderProductUninstall))
    return suite