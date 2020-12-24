# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/gobry/src/canal/build/lib/canalweb/test_vod.py
# Compiled at: 2008-12-18 02:30:35
__doc__ = 'Tests for canalweb.vod.'
import os, shutil
from canalweb import vod
ROOT = os.path.dirname(__file__)

class TestDownloader(object):
    """Test the Downloader class."""

    def setup_method(self, _):
        """Setup a downloader."""
        self.cache = os.path.join(ROOT, 'test-cache')
        try:
            shutil.rmtree(self.cache)
        except OSError:
            pass

        os.mkdir(self.cache)
        self.dl = vod.Downloader(self.cache)

    def test_content_ids(self):
        """Check exraction of video IDs."""
        fd = open(os.path.join(ROOT, 'testdata', 'pid1830-c-zapping.html'))
        assert [ url for url in self.dl.extract_content_ids(fd) ] == [
         195190, 195164, 194541, 194196, 193817, 193423, 193128, 192859]

    def test_config(self):
        """Check parsing of the XML file."""
        data = open(os.path.join(ROOT, 'testdata', 'video-config.xml')).read()
        video = self.dl._video_url(data, 'guignoles', 1234)
        assert video.url == 'http://vod-flash.canalplus.fr/WWWPLUS/PROGRESSIF/0812/LES_GUIGNOLS_EMISSION_081214_AUTO_1138_169_video_H.flv'