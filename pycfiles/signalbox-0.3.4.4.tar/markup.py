# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/templatetags/markup.py
# Compiled at: 2014-08-27 19:26:12
import markdown as md
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    extensions = ['nl2br']
    return mark_safe(md.markdown(force_unicode(value), extensions, safe_mode=True, enable_attributes=False))