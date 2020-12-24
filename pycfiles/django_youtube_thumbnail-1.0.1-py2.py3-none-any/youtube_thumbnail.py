# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsenkbeil/Projects/gs/django-youtube-thumbnail/youtube_thumbnail/templatetags/youtube_thumbnail.py
# Compiled at: 2015-08-25 16:56:42
from classytags.core import Tag, Options
from classytags.arguments import Argument
from django import template
from ..api import get_thumbnail_url
register = template.Library()

class YoutubeThumbnailURL(Tag):
    name = 'youtube_thumbnail_url'
    options = Options(Argument('url'))

    def render_tag(self, context, url):
        return get_thumbnail_url(url)


register.tag(YoutubeThumbnailURL)