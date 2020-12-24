# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Pycharm\PycharmProjects\locationfield\mapbox_location_field\templatetags\mapbox_location_field_tags.py
# Compiled at: 2019-07-08 05:46:20
# Size of source mod 2**32: 991 bytes
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def location_field_includes():
    html = "<meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no'/><script src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.js'></script><link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.css' rel='stylesheet'/><script src='https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.4.0/mapbox-gl-geocoder.min.js'></script><link rel='stylesheet' href='https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.4.0/mapbox-gl-geocoder.css' type='text/css'/>"
    return mark_safe(html)


@register.simple_tag
def include_jquery():
    return mark_safe("<script src='https://code.jquery.com/jquery-3.3.1.min.js' integrity='sha384-tsQFqpEReu7ZLhBV2VZlAu7zcOV+rXbYlF2cqB8txI/8aZajjp4Bqd+V6D5IgvKT' crossorigin='anonymous' ></script>")