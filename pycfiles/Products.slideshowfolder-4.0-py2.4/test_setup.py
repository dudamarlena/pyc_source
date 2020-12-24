# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/slideshowfolder/tests/test_setup.py
# Compiled at: 2008-07-09 00:45:53
from base import SlideshowFolderTestCase

class TestSlideshowFolderProductInstall(SlideshowFolderTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.skins = self.portal.portal_skins
        self.css = self.portal.portal_css
        self.types = self.portal.portal_types
        self.product_skin_layers = ('slideshowfolder', 'slideshowjavascript')
        self.action_ids = ('makeSlideshow', 'unmakeSlideshow', 'slideshow_settings')

    def testSkinLayersRegistered(self):
        """Make sure the desired skin layers with templates,
           javascript, and CSS are registered with the skins tool.
        """
        registered_skin_layers = self.skins.objectIds()
        for layer in self.product_skin_layers:
            self.failUnless(layer in registered_skin_layers, 'The layer %s is not                 registered with the skin tool' % layer)

    def testSkinLayersAppearInAllThemes(self):
        """We need our product's skin directories to show up below custom as one of the called
           upon layers of our skin's properties
        """
        for (selection, layers) in self.skins.getSkinPaths():
            for specific_layer in self.product_skin_layers:
                self.failUnless(specific_layer in layers, "The %s layer                     does not appear in the layers of Plone's %s skin" % (specific_layer, selection))

    def testPortalActionsHasOurActions(self):
        """We register three actions
        """
        all_action_ids = [ a.id for a in self.portal.portal_actions.listActions() ]
        for id in self.action_ids:
            self.failUnless(id in all_action_ids, '%s missing from portal_actions' % id)

    def testSlideshowPermissionInstalled(self):
        """ We add a permission called "Slideshowfolder: Manage slideshow settings"
        """
        from Products.CMFCore.utils import _checkPermission as checkPerm
        self.setRoles(['Manager'])
        self.failUnless(checkPerm('Slideshowfolder: Manage slideshow settings', self.portal))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSlideshowFolderProductInstall))
    return suite