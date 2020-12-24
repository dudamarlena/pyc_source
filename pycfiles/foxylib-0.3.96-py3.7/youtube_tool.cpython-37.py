# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/google/youtube/youtube_tool.py
# Compiled at: 2020-01-29 00:30:01
# Size of source mod 2**32: 3408 bytes
import logging, re
from functools import lru_cache
import requests
from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.string.string_tool import format_str
from foxylib.tools.url.url_tool import URLTool

class YoutubeTool:

    @classmethod
    def video_id2url(cls, video_id):
        url_base = 'https://www.youtube.com/watch'
        h = {'v': video_id}
        url = URLTool.append_query2url(url_base, h)
        return url

    @classmethod
    def url2is_accessible(cls, url):
        httpr = requests.head(url)
        return httpr.ok

    @classmethod
    def rstr_video_id(cls):
        return '[A-Za-z0-9\\-=_]{11}'

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_video_id(cls):
        return re.compile(cls.rstr_video_id())

    @classmethod
    def rstr_url_prefix(cls):
        return '(?:https?://)?(?:www\\.)?(?:youtube|youtu|youtube-nocookie)\\.(?:com|be)/(?:watch\\?v=|embed/|v/|.+\\?v=)?'

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_url_prefix(cls):
        return re.compile(cls.rstr_url_prefix())

    @classmethod
    def rstr_url(cls):
        logger = FoxylibLogger.func_level2logger(cls.rstr_url, logging.DEBUG)
        rstr_prefix = cls.rstr_url_prefix()
        rstr_video_id = cls.rstr_video_id()
        rstr = RegexTool.join('', [rstr_prefix, rstr_video_id])
        logger.debug({'rstr': rstr})
        return rstr

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_url(cls):
        return re.compile(cls.rstr_url())

    @classmethod
    def _url2match_video_id(cls, url):
        m_prefix = cls.pattern_url_prefix().match(url)
        if not m_prefix:
            return
        else:
            m_video_id = cls.pattern_video_id().match(url[m_prefix.end():])
            return m_video_id or None
        return m_video_id

    @classmethod
    def url2video_id(cls, url):
        m_video_id = cls._url2match_video_id(url)
        if not m_video_id:
            return
        return m_video_id.group()

    @classmethod
    def video_id2thumbnail_url_hqdefault(cls, video_id):
        return 'https://img.youtube.com/vi/{}/hqdefault.jpg'.format(video_id)