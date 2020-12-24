# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jsonfield2/templatetags/jsonify.py
# Compiled at: 2015-06-04 10:41:05
# Size of source mod 2**32: 378 bytes
import json
from django import template
from django.utils.safestring import mark_safe
from jsonfield2.utils import JSONEncoder
register = template.Library()

@register.filter
def jsonify(value):
    if getattr(value, 'all', False):
        value = list(value)
    return mark_safe(json.dumps(value, cls=JSONEncoder))