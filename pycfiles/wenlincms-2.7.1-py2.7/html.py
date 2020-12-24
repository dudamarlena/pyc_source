# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/utils/html.py
# Compiled at: 2016-05-20 23:41:38
from __future__ import absolute_import, unicode_literals
from future.builtins import chr, int, str
try:
    from html.parser import HTMLParser, HTMLParseError
    from html.entities import name2codepoint
except ImportError:
    from HTMLParser import HTMLParser, HTMLParseError
    from htmlentitydefs import name2codepoint

import re
SELF_CLOSING_TAGS = [
 b'br', b'img']
NON_SELF_CLOSING_TAGS = [b'script', b'iframe']

def decode_entities(html):
    """
    Remove HTML entities from a string.
    Adapted from http://effbot.org/zone/re-sub.htm#unescape-html
    """

    def decode(m):
        html = m.group(0)
        if html[:2] == b'&#':
            try:
                if html[:3] == b'&#x':
                    return chr(int(html[3:-1], 16))
                else:
                    return chr(int(html[2:-1]))

            except ValueError:
                pass

        else:
            try:
                html = chr(name2codepoint[html[1:-1]])
            except KeyError:
                pass

        return html

    return re.sub(b'&#?\\w+;', decode, html.replace(b'&amp;', b'&'))


def thumbnails(html):
    """
    Given a HTML string, converts paths in img tags to thumbnail
    paths, using wenlincms's ``thumbnail`` template tag. Used as
    one of the default values in the ``RICHTEXT_FILTERS`` setting.
    """
    from django.conf import settings
    from bs4 import BeautifulSoup
    from wenlincms.core.templatetags.wenlincms_tags import thumbnail
    if settings.MEDIA_URL.lower() not in html.lower():
        return html
    dom = BeautifulSoup(html, b'html.parser')
    for img in dom.findAll(b'img'):
        src = img.get(b'src', b'')
        src_in_media = src.lower().startswith(settings.MEDIA_URL.lower())
        width = img.get(b'width')
        height = img.get(b'height')
        if src_in_media and width and height:
            img[b'src'] = settings.MEDIA_URL + thumbnail(src, width, height)

    return str(dom)


class TagCloser(HTMLParser):
    """
    HTMLParser that closes open tags. Takes a HTML string as its first
    arg, and populate a ``html`` attribute on the parser with the
    original HTML arg and any required closing tags.
    """

    def __init__(self, html):
        HTMLParser.__init__(self)
        self.html = html
        self.tags = []
        try:
            self.feed(self.html)
        except HTMLParseError:
            pass
        else:
            self.html += (b'').join([ b'</%s>' % tag for tag in self.tags ])

    def handle_starttag(self, tag, attrs):
        if tag not in SELF_CLOSING_TAGS:
            self.tags.insert(0, tag)

    def handle_endtag(self, tag):
        try:
            self.tags.remove(tag)
        except ValueError:
            pass