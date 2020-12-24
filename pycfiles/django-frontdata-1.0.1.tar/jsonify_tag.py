# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/projects/vk-board/src/jsonify/templatetags/jsonify_tag.py
# Compiled at: 2015-06-20 19:04:37
from django import template
from django.utils.safestring import mark_safe
from jsonify import compat
register = template.Library()

@register.filter
def jsonify(data):
    return mark_safe(compat.serialize_data(data))