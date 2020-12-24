# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/noors/PycharmProjects/django_2gis_maps/django_2gis_maps/templatetags/doublegis.py
# Compiled at: 2018-09-05 10:55:41
# Size of source mod 2**32: 573 bytes
from __future__ import unicode_literals
from math import floor
from django import template
from django.contrib.messages import constants as message_constants
from django.template import Context
from django.utils import six
from django.utils.safestring import mark_safe
register = template.Library()

@register.inclusion_tag('django_2gis_maps/map/map.html')
def render_map(instance, **kwargs):
    context = {'instance':instance, 
     'geolocation':instance.get_location}
    if kwargs:
        context.update(kwargs)
    return context