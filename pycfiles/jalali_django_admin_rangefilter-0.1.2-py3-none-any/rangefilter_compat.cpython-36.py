# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nima/Projects/Python/jalali-django-admin-rangefilter/rangefilter/templatetags/rangefilter_compat.py
# Compiled at: 2020-02-10 05:04:20
# Size of source mod 2**32: 390 bytes
from __future__ import unicode_literals
import django
from django.template import Library
if django.VERSION[:2] >= (1, 10):
    from django.templatetags.static import static as _static
else:
    from django.contrib.admin.templatetags.admin_static import static as _static
register = Library()

@register.simple_tag()
def static(path):
    return _static(path)