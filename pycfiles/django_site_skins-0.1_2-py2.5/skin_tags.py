# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skins/templatetags/skin_tags.py
# Compiled at: 2010-03-20 20:08:48
"""Provides secure-aware skinned media url tags.

:Authors:
    - Bruce Kroeze
"""
__docformat__ = 'restructuredtext'
from django import template
from django.utils import translation
from skins.utils import url_join
from skins import skin
import logging
log = logging.getLogger('skin_tags')
register = template.Library()

def _skin_media_url():
    return skin.active_skin().media_url


class SkinMediaURLNode(template.Node):

    def __init__(self, url):
        self.url = url

    def render(self, context):
        if self.url:
            return url_join(_skin_media_url(), self.url)
        else:
            return _skin_media_url()


@register.tag
def skin_media_url(parser, token):
    parts = token.contents.split(None)
    if len(parts) > 1:
        url = parts[1:]
    else:
        url = None
    return SkinMediaURLNode(url)


@register.filter
def skin_media(val):
    return url_join(_skin_media_url(), val)


class SkinMediaLocaleURLNode(template.Node):

    def __init__(self, url):
        self.url = url

    def render(self, context):
        prefix = skin_media_url()
        language = translation.get_language()
        if self.url:
            return url_join(prefix, self.url, language)
        else:
            return url_join(prefix, language)


@register.tag
def skin_media_locale_url(parser, token):
    parts = token.contents.split(None)
    if len(parts) > 1:
        url = parts[1:]
    else:
        url = None
    return SkinMediaLocaleURLNode(url)