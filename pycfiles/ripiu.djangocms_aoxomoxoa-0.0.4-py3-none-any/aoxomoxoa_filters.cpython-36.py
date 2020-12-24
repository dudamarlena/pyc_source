# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/github/djangocms_aoxomoxoa/ripiu/djangocms_aoxomoxoa/templatetags/aoxomoxoa_filters.py
# Compiled at: 2018-04-03 09:24:46
# Size of source mod 2**32: 953 bytes
from django.template import Library
register = Library()

@register.filter(name='get_size')
def get_size(thumb_opt):
    return (thumb_opt.width, thumb_opt.height)


@register.filter(name='get_alt')
def get_alt(instance):
    if hasattr(instance, 'image'):
        return instance.alt_text or instance.image.default_alt_text
    else:
        if hasattr(instance, 'picture'):
            if 'alt' in instance.attributes:
                if instance.attributes['alt']:
                    return instance.attributes['alt']
            return instance.picture.default_alt_text
        return 'PUPPA!'


@register.filter(name='get_caption')
def get_caption(instance):
    if hasattr(instance, 'image'):
        return instance.caption_text or instance.image.default_caption
    if hasattr(instance, 'picture'):
        return instance.caption_text or instance.picture.default_caption