# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\FlashVideo\tests\test_FlashVideoFolder.py
# Compiled at: 2009-03-02 16:14:25
"""
Unit tests for FlashVideoFolder class
"""
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.FlashVideo.config import *
from Products.FlashVideo.tests.utils import getRequest
from BaseTest import PloneFunctionalTestCase
from BaseTest import PloneIntegrationTestCase
from BaseTest import PloneUnitTestCase
VIDEO_FOLDER_ID = 'videofolder'

class FlashVideoFolderUnitTests(PloneUnitTestCase):
    """
    Test class for FlashVideoFolder class.  
    """
    __module__ = __name__
    portal_type = FLASHVIDEOFOLDER_PORTALTYPE
    object_id = VIDEO_FOLDER_ID


class FlashVideoFolderIntegrationTestCase(PloneIntegrationTestCase):
    """
    Functional tests checking that all configuation works
    """
    __module__ = __name__
    portal_type = FLASHVIDEOFOLDER_PORTALTYPE
    object_id = VIDEO_FOLDER_ID
    type_properties = (('immediate_view', 'flashvideofolder_view'), ('default_view', 'flashvideofolder_view'), ('content_icon', 'flashvideofolder_icon.gif'), ('allowed_content_types', (FLASHVIDEO_PORTALTYPE, FLASHVIDEOPLAYLIST_PORTALTYPE)), ('global_allow', True), ('filter_content_types', True))
    skin_files = ('flashvideofolder_icon.gif', 'flashvideofolder_view')
    object_actions = [
     'view', 'edit', 'metadata', 'local_roles', 'folderContents']


class FlashVideoFolderFunctionalTestCase(PloneFunctionalTestCase):
    """
    Functional tests for view and edit templates
    """
    __module__ = __name__
    portal_type = FLASHVIDEOFOLDER_PORTALTYPE
    object_id = VIDEO_FOLDER_ID


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(FlashVideoFolderUnitTests))
    suite.addTest(makeSuite(FlashVideoFolderFunctionalTestCase))
    suite.addTest(makeSuite(FlashVideoFolderIntegrationTestCase))
    return suite


if __name__ == '__main__':
    framework()