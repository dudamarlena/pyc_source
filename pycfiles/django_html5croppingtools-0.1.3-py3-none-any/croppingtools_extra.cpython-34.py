# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/irakli/Documents/python/projects/test_d/html5croppingtools/templatetags/croppingtools_extra.py
# Compiled at: 2015-07-09 06:19:07
# Size of source mod 2**32: 440 bytes
from django import template
from django.db.models import ImageField
register = template.Library()

@register.simple_tag()
def html5crop(image_field, quality=None, dimensions=None):
    if image_field.url:
        _return = image_field.url + '?'
        _return += 'quality=' + str(quality) + '&' if quality else ''
        _return += 'dimensions=' + dimensions if dimensions else ''
        return _return
    else:
        return ''