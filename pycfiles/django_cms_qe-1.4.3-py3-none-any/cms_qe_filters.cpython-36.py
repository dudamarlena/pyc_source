# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/templatetags/cms_qe_filters.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 241 bytes
from django import template
register = template.Library()

@register.filter
def add_str(value, arg):
    """
    Same as :py:func:`django.template.defaultfilters.add` but always convert to ``str``.
    """
    return str(value) + str(arg)