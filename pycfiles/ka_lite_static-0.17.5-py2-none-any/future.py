# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/templatetags/future.py
# Compiled at: 2018-07-11 18:15:30
from django.template import Library
from django.template.defaulttags import url as default_url, ssi as default_ssi
register = Library()

@register.tag
def ssi(parser, token):
    return default_ssi(parser, token)


@register.tag
def url(parser, token):
    return default_url(parser, token)