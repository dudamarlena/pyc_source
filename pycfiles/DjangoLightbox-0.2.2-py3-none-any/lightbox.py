# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geert/dev/ccnet17/lib/python2.7/site-packages/lightbox/templatetags/lightbox.py
# Compiled at: 2014-04-18 11:13:54
from django import template
import base64
register = template.Library()

@register.simple_tag
def decode(value):
    return base64.b64decode(value)


from django.core.serializers import serialize
from django.db.models.query import QuerySet
try:
    from django.utils import simplejson as json
except:
    import json

from django.utils.safestring import mark_safe

def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(json.dumps(object))


register.filter('jsonify', jsonify)
jsonify.is_safe = True