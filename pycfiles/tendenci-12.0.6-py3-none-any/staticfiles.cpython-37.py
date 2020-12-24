# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/theme/templatetags/staticfiles.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 533 bytes
from warnings import warn
from django import template
from .static import do_static as _do_static
register = template.Library()

@register.tag('static')
def do_static(parser, token):
    template = parser.origin.name
    theme = getattr(parser.origin, 'theme', None)
    theme_str = 'theme "%s"' % theme if theme else 'an installed Django app'
    warn('{%% load staticfiles %%} in template "%s" in %s is deprecated, use {%% load static %%} instead' % (template, theme_str), DeprecationWarning)
    return _do_static(parser, token)