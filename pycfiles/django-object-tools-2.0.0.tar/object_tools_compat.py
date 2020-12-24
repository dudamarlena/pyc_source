# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-object-tools/object_tools/templatetags/object_tools_compat.py
# Compiled at: 2018-12-21 02:57:07
"""Handle future url tag deprecation so we don't leave pre Django 1.8 in either
an unmaintained state or in a different branch."""
from django.template import Library
try:
    from django.templatetags.future import url as base_url
except ImportError:
    from django.template.defaulttags import url as base_url

register = Library()

@register.tag
def url(parser, token):
    return base_url(parser, token)