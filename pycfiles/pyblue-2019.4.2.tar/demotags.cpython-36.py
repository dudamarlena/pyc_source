# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ialbert/web/pyblue-central/docs/templatetags/demotags.py
# Compiled at: 2019-04-02 09:06:58
# Size of source mod 2**32: 466 bytes
"""
This library demonstrates the use of custom demo tags
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import logging
from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
logger = logging.getLogger(__name__)
register = template.Library()

@register.simple_tag()
def boom(text):
    html = 'BOOM! BOOM! POW! <b>{}</b>!'.format(text)
    return mark_safe(html)