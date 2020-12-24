# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/djbetty/templatetags/betty.py
# Compiled at: 2016-10-10 15:46:42
# Size of source mod 2**32: 4986 bytes
from __future__ import absolute_import
import requests
from six.moves.urllib.parse import urlparse, urlunparse
from django import template
from django.core.cache import cache
from django.template.loader import select_template
from django.utils.safestring import mark_safe
from djbetty.conf import settings
from djbetty.fields import ImageFieldFile, default_storage
register = template.Library()

class AnonymousImageField(object):

    def __init__(self, id):
        self.id = id
        self.storage = default_storage

    def get_crop_url(self, ratio='original', width=600, format='jpg', fixed=False):
        return self.storage.url(self.id, ratio=ratio, width=width, format=format, fixed=fixed)

    def get_animated_url(self, format='gif', fixed=False):
        return self.storage.animated_url(self.id, format=format, fixed=fixed)


def coerce_image(image):
    """For right now, we need to be able to pass a string, or an int, or None
    into the template tags, and still have them return something meaningful"""
    if not image:
        if hasattr(settings, 'BETTY_DEFAULT_IMAGE') and settings.BETTY_DEFAULT_IMAGE is not None:
            return AnonymousImageField(settings.BETTY_DEFAULT_IMAGE)
        return
    if not isinstance(image, ImageFieldFile):
        try:
            image_id = int(image)
        except:
            if settings.BETTY_DEFAULT_IMAGE:
                image_id = settings.BETTY_DEFAULT_IMAGE
            else:
                return

        image = AnonymousImageField(image_id)
    return image


@register.simple_tag
def cropped_url(image, ratio='16x9', width=600, format='jpg', fixed=False):
    image = coerce_image(image)
    if image is None:
        return ''
    return image.get_crop_url(ratio=ratio, width=width, format=format, fixed=fixed)


@register.simple_tag(takes_context=True)
def cropped(context, image, ratio='16x9', width=600, format='jpg', fixed=False):
    image = coerce_image(image)
    if not image or not image.id:
        if hasattr(settings, 'BETTY_DEFAULT_IMAGE'):
            image = AnonymousImageField(settings.BETTY_DEFAULT_IMAGE)
    else:
        return ''
    context['image'] = image
    context['image_url'] = image.get_crop_url(ratio=ratio, width=width, format=format, fixed=fixed)
    context['ratio'] = ratio
    context['width'] = width
    context['format'] = format
    t = select_template(['betty/cropped.html', 'betty/cropped_default.html'])
    return t.render(context)


@register.simple_tag
def animated_url(image, format='gif', fixed=False):
    image = coerce_image(image)
    if image is None:
        return ''
    return image.get_animated_url(format=format, fixed=fixed)


@register.simple_tag
def betty_js_url():
    betty_image_url = settings.BETTY_IMAGE_URL
    url_parts = list(urlparse(betty_image_url))
    url_parts[0] = ''
    betty_image_url = urlunparse(url_parts)
    return '{}/image.js'.format(betty_image_url)


@register.simple_tag
def betty_image_url():
    url = settings.BETTY_IMAGE_URL
    url_parts = list(urlparse(url))
    url_parts[0] = ''
    url = urlunparse(url_parts)
    return url


@register.simple_tag
def betty_fixed_url():
    url = settings.BETTY_FIXED_URL
    url_parts = list(urlparse(url))
    url_parts[0] = ''
    url = urlunparse(url_parts)
    return url


def _javascript_tag(text):
    return '<script type="text/javascript">{}</script>'.format(text)


@register.simple_tag
def betty_js_header():
    if settings.BETTY_INLINE_JS:
        cache_key = 'betty-js-content'
        content = cache.get(cache_key)
        if not content:
            url_parts = list(urlparse(settings.BETTY_IMAGE_URL))
            if not url_parts[0]:
                url_parts[0] = 'http'
            url = urlunparse(url_parts)
            resp = requests.get('{}/image.js'.format(url))
            resp.raise_for_status()
            content = _javascript_tag(resp.text)
            cache.set(cache_key, content, 900)
        return mark_safe(content)
    else:
        return '<script src="{}"></script>'.format(betty_js_url())


@register.simple_tag
def betty_js_footer():
    return mark_safe(_javascript_tag('window.picturefill();'))