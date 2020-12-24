# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ialbert/web/pyblue-central/docs/templatetags/demotags.py
# Compiled at: 2019-04-02 09:06:58
# Size of source mod 2**32: 466 bytes
__doc__ = '\nThis library demonstrates the use of custom demo tags\n'
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