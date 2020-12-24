# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\fresh\ven\sirtest\sirtrevor\templatetags\sirtrevor.py
# Compiled at: 2014-07-21 06:19:49
# Size of source mod 2**32: 486 bytes
import markdown2
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.conf import settings
register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def markdown2_filter(value):
    return mark_safe(markdown2.markdown(force_text(value), extras=settings.SIRTREVOR_MARKDOWN_EXTENSIONS))


register.filter('markdown', markdown2_filter)