# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/google/youtube/tests/test_youtube_tool.py
# Compiled at: 2020-01-08 12:53:55
# Size of source mod 2**32: 1534 bytes
import logging, re
from functools import lru_cache
from unittest import TestCase
from foxylib.tools.google.youtube.youtube_tool import YoutubeTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import MatchTool

class TestYoutubeTool(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        url = 'https://www.youtube.com/watch?v=4VYAaLh3XZg&t=33s'
        hyp = YoutubeTool.url2video_id(url)
        ref = '4VYAaLh3XZg'
        self.assertEqual(hyp, ref)

    def test_02(self):
        video_id = '4VYAaLh3XZg'
        hyp = YoutubeTool.video_id2url(video_id)
        ref = 'https://www.youtube.com/watch?v=4VYAaLh3XZg'
        self.assertEqual(hyp, ref)

    def test_03(self):
        url = 'https://www.youtube.com/watch?v=4VYAaLh3XZg'
        hyp = YoutubeTool.url2is_accessible(url)
        self.assertTrue(hyp)

    def test_04(self):
        p = YoutubeTool.pattern_url()
        url1 = 'http://youtu.be/5Y6HSHwhVlY'
        self.assertTrue(p.match(url1))
        self.assertEqual(YoutubeTool.url2video_id(url1), '5Y6HSHwhVlY')
        url2 = 'http://www.youtube.com/embed/5Y6HSHwhVlY?rel=0'
        self.assertTrue(p.match(url2))
        self.assertEqual(YoutubeTool.url2video_id(url2), '5Y6HSHwhVlY')
        url3 = 'http://www.youtube.com/watch?v=ZFqlHhCNBOI'
        self.assertTrue(p.match(url3))
        self.assertEqual(YoutubeTool.url2video_id(url3), 'ZFqlHhCNBOI')