# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pb/Code/django-sirtrevor/sirtrevor/templatetags/sirtrevor.py
# Compiled at: 2014-02-18 06:05:37
import markdown2
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def markdown2_filter(value):
    return mark_safe(markdown2.markdown(force_text(value)))


register.filter('markdown', markdown2_filter)