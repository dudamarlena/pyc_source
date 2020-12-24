# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nima/Projects/Python/jalali-django-admin-rangefilter/rangefilter/apps.py
# Compiled at: 2020-02-10 05:04:20
# Size of source mod 2**32: 374 bytes
from __future__ import unicode_literals
import django
from django.apps import AppConfig
if django.VERSION >= (2, 0, 0):
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _

class RangeFilterConfig(AppConfig):
    name = 'rangefilter'
    verbose_name = _('Range Filter')