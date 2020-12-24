# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dodi/envs/isdc/isdc_modules/isdc_dashboard/dashboard/templatetags/app_filters.py
# Compiled at: 2018-11-05 22:35:30
from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet, ValuesListQuerySet
from geonode.utils import JSONEncoderCustom
import json, urllib
register = template.Library()

@register.simple_tag
def readable(val):
    if val >= 1000 and val < 1000000:
        c = ('%.1f' % round(val / 1000, 2)).rstrip('0').rstrip('.')
        return ('{} K').format(c)
    else:
        if val >= 1000000 and val < 1000000000:
            b = ('%.1f' % round(val / 1000000, 2)).rstrip('0').rstrip('.')
            return ('{} M').format(b)
        return ('%.1f' % round(val or 0)).rstrip('0').rstrip('.')


@register.filter(is_safe=True)
def jsonify(object):
    return json.dumps(object, cls=JSONEncoderCustom)