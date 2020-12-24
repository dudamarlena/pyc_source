# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/checks/compatibility/django_1_10.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.conf import global_settings, settings
from .. import Tags, Warning, register

@register(Tags.compatibility)
def check_duplicate_middleware_settings(app_configs, **kwargs):
    if settings.MIDDLEWARE is not None and settings.MIDDLEWARE_CLASSES != global_settings.MIDDLEWARE_CLASSES:
        return [
         Warning(b"The MIDDLEWARE_CLASSES setting is deprecated in Django 1.10 and the MIDDLEWARE setting takes precedence. Since you've set MIDDLEWARE, the value of MIDDLEWARE_CLASSES is ignored.", id=b'1_10.W001')]
    else:
        return []