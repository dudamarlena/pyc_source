# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/slideshowfolder/tests/test_slideshow_enabling.py
# Compiled at: 2008-07-06 04:12:41
from base import SlideshowFolderTestCase
from Products.slideshowfolder.browser import FolderSlideShowView
from Products.slideshowfolder.config import PROJ
from Products.slideshowfolder.slideshowsetting import SlideShowSettings
from Products.slideshowfolder import HAS_PLONE30
try:
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    from zope.app.annotation.interfaces import IAnnotations

class TestSlideshowEnabling(SlideshowFolderTestCase):
    """Test the enabling and disabling of slideshows within folders"""
    __module__ = __name__

    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.folder.invokeFactory('Folder', id='test1', title='Test Slideshow')
        self.test1 = getattr(self.folder, 'test1')

    def testEnablingSlideshow(self):
        """Test that we can enable the slideshow functionality on a folder
        that doesn't yet have it"""
        view = FolderSlideShowView(self.test1, self.app.REQUEST)
        self.failUnless(not view.isSlideshow())
        action_id = 'makeSlideshow'
        actions = self.portal.portal_actions.listFilteredActionsFor(self.test1)
        action_ids = [ a['id'] for a in actions['object_buttons'] ]
        self.failUnless(action_id in action_ids, 'Uh oh! %s not found in %s' % (action_id, action_ids))
        view.makeSlideshow()
        self.failUnless(view.isSlideshow())
        if HAS_PLONE30:
            actions = self.portal.portal_actions.listFilteredActionsFor(self.test1)
            action_ids = [ a['id'] for a in actions['object'] ]
            action_id = 'slideshow_settings'
            self.failUnless(action_id in action_ids, 'Uh oh! %s not found in %s' % (action_id, action_ids))

    def testEnabledSlideshowIsEnabled(self):
        """Test that an enabled slideshow delivers what it promises."""
        view = FolderSlideShowView(self.test1, self.app.REQUEST)
        view.makeSlideshow()
        layout = getattr(self.test1, 'layout', '')
        self.failUnless(layout == 'folder_slideshow')
        action_id = 'unmakeSlideshow'
        actions = self.portal.portal_actions.listFilteredActionsFor(self.test1)
        action_ids = [ a['id'] for a in actions['object_buttons'] ]
        self.failUnless(action_id in action_ids, 'Uh oh! %s not found in %s' % (action_id, action_ids))
        action_id = 'slideshow_settings'
        actions = self.portal.portal_actions.listFilteredActionsFor(self.test1)
        if actions.has_key('object_tabs'):
            action_ids = [ a['id'] for a in actions['object_tabs'] ]
        else:
            action_ids = [ a['id'] for a in actions['object'] ]
        self.failUnless(action_id in action_ids, 'Uh oh! %s not found in %s' % (action_id, action_ids))
        self.failUnless(view.isSlideshow())

    def testDisablingSlideshow(self):
        """We want to make sure that we're thoroughly removing the cruft"""
        view = FolderSlideShowView(self.test1, self.app.REQUEST)
        view.makeSlideshow()
        metadata_setter = SlideShowSettings(self.test1)
        metadata_setter.slideDuration = 2
        view.unmakeSlideshow()
        self.failUnless(not view.isSlideshow())
        layout = getattr(self.test1, 'layout', '')
        self.failUnless(layout != 'folder_slideshow')
        action_id = 'makeSlideshow'
        actions = self.portal.portal_actions.listFilteredActionsFor(self.test1)
        action_ids = [ a['id'] for a in actions['object_buttons'] ]
        self.failUnless(action_id in action_ids, 'Uh oh! %s not found in %s' % (action_id, action_ids))
        if HAS_PLONE30:
            actions = self.portal.portal_actions.listFilteredActionsFor(self.test1)
            action_ids = [ a['id'] for a in actions['object'] ]
            action_id = 'slideshow_settings'
            self.failIf(action_id in action_ids, '%s still listed in available actions: %s' % (action_id, action_ids))
        annotations = IAnnotations(self.test1)
        self.failUnless(annotations.get(PROJ, None) is None, 'Annotations not deleted: %s' % annotations.get(PROJ))
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSlideshowEnabling))
    return suite