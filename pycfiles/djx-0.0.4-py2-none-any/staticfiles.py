# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/staticfiles/templatetags/staticfiles.py
# Compiled at: 2019-02-14 00:35:17
from django import template
from django.templatetags.static import do_static as _do_static, static as _static
register = template.Library()

def static(path):
    return _static(path)


@register.tag('static')
def do_static(parser, token):
    return _do_static(parser, token)