# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\FlashVideo\tests\test_FlashVideoPlaylist.py
# Compiled at: 2009-03-02 16:14:25
__doc__ = '\nUnit tests for FlashVideoPlaylist class\n'
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.FlashVideo.config import *
from Products.FlashVideo.tests.utils import getRequest
from BaseTest import PloneFunctionalTestCase
from BaseTest import PloneIntegrationTestCase
from BaseTest import PloneUnitTestCase
VIDEO_PLAYLIST_ID = 'videoplaylist'
VIDEO_ID1 = 'video1'

class FlashVideoPlaylistUnitTests(PloneUnitTestCase):
    """
    Test class for FlashVideoPlaylist class.  
    """
    __module__ = __name__
    portal_type = FLASHVIDEOPLAYLIST_PORTALTYPE
    object_id = VIDEO_PLAYLIST_ID

    def createInstance(self):
        """
        Create object instance of defined portal_type
        """
        image = self.getImageFile()
        movie = self.getMovieFile()
        self.folder.invokeFactory(FLASHVIDEO_PORTALTYPE, id=VIDEO_ID1)
        video = self.folder._getOb(VIDEO_ID1)
        video.setScreenshot(image)
        video.setFile(movie)
        self.folder.invokeFactory(self.portal_type, id=self.object_id)
        playlist = self.folder._getOb(self.object_id)
        playlist.setVideos(video.UID())
        return playlist

    def test_createInstance(self):
        """
        Check if createInstance creates playlist with one 
        video file inside
        """
        playlist = self.createInstance()
        self.assertEqual(playlist.portal_type, self.portal_type)
        uids = playlist.getRawVideos()
        self.assertEqual(len(uids), 1)
        video = self.folder._getOb(VIDEO_ID1)
        self.assertEqual(uids[0], video.UID())

    def test_getVideosList(self):
        """
        Get list of videos
        """
        playlist = self.createInstance()
        vl = playlist.getVideosList()
        self.assertEqual(len(vl), 1)
        self.assertEqual(vl[0].getId(), VIDEO_ID1)

    def test_getPlaylistWidth(self):
        """
        Test if playlist width (resolution) is the same as width of first movie
        """
        playlist = self.createInstance()
        self.assertEqual(playlist.getPlaylistWidth(), 130)

    def test_getPlaylistHeight(self):
        """
        Test if playlist height (resolution) is the same as height of first movie
        """
        playlist = self.createInstance()
        self.assertEqual(playlist.getPlaylistHeight(), 70)

    def test_getPlaylistUrls(self):
        """
        Get absolute urls of all movies in list
        """
        playlist = self.createInstance()
        urls = playlist.getPlaylistUrls()
        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0].endswith(VIDEO_ID1), True)

    def test_getPlaylistString(self):
        """
        Check generated string for javascript if contains one
        video url
        """
        playlist = self.createInstance()
        url = self.folder._getOb(VIDEO_ID1).absolute_url()
        self.assertEqual(playlist.getPlaylistString(), "{url: '%s', type: 'flv'}," % url)

    def test_getPlaylistScreenshot(self):
        """
        Check if playlist screenshot url is the same as video url
        """
        playlist = self.createInstance()
        screenshot = playlist.getPlaylistScreenshot()
        url = self.folder._getOb(VIDEO_ID1).absolute_url()
        self.assertEqual(screenshot, '%s/screenshot' % url)

    def test_screenshot_mini(self):
        """
        Check method for displaying screenshot_mini. Check with REQUEST
        and without.
        """
        playlist = self.createInstance()
        mini = playlist.screenshot_mini()
        self.assertNotEqual(mini, None)
        self.assertEqual(len(mini), 3159)
        response = getRequest().RESPONSE
        content_type = response.getHeader('content-type')
        self.assertEqual(content_type, None)
        mini2 = playlist.screenshot_mini(RESPONSE=response)
        self.assertNotEqual(mini, None)
        self.assertEqual(len(mini), 3159)
        content_type = response.getHeader('content-type')
        self.assertEqual(content_type, 'image/jpeg')
        return


class FlashVideoPlaylistIntegrationTestCase(PloneIntegrationTestCase):
    """
    Functional tests checking that all configuation works
    """
    __module__ = __name__
    portal_type = FLASHVIDEOPLAYLIST_PORTALTYPE
    object_id = VIDEO_PLAYLIST_ID
    type_properties = (('immediate_view', 'flashvideoplaylist_view'), ('default_view', 'flashvideoplaylist_view'), ('content_icon', 'flashvideoplaylist_icon.gif'), ('allowed_content_types', ()), ('global_allow', True), ('filter_content_types', False))
    skin_files = ('flashvideoplaylist_icon.gif', 'flashvideoplaylist_view')
    object_actions = [
     'view', 'edit', 'metadata', 'local_roles', 'play']
    type_actions = ['view', 'edit', 'metadata', 'local_roles', 'play']


class FlashVideoPlaylistFunctionalTestCase(PloneFunctionalTestCase):
    """
    Functional tests for view and edit templates
    """
    __module__ = __name__
    portal_type = FLASHVIDEOPLAYLIST_PORTALTYPE
    object_id = VIDEO_PLAYLIST_ID


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(FlashVideoPlaylistUnitTests))
    suite.addTest(makeSuite(FlashVideoPlaylistFunctionalTestCase))
    suite.addTest(makeSuite(FlashVideoPlaylistIntegrationTestCase))
    return suite


if __name__ == '__main__':
    framework()