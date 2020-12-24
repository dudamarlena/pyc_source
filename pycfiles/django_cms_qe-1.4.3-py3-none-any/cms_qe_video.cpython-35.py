# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_video/templatetags/cms_qe_video.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 843 bytes
import typing
from urllib import parse
from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

@typing.no_type_check
@register.filter(name='cms_qe_video_url_to_embed')
@stringfilter
def cms_qe_video_url_to_embed(url: str) -> str:
    """
    Django template filter to change video URL to make it embed.
    A little hack for popular video hosting services.
    """
    url = parse.urlparse(url)
    if 'vimeo.com' in url.netloc:
        return parse.urlunparse((url.scheme, 'player.vimeo.com', '/video' + url.path, [], {}, ''))
    if 'youtube.com' in url.netloc or 'youtu.be' in url.netloc:
        video_id = parse.parse_qs(url.query)['v'][0]
        return parse.urlunparse((url.scheme, 'www.youtube.com', '/embed/' + video_id, [], {}, ''))
    return parse.urlunparse(url)