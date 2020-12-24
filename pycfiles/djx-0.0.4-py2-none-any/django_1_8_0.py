# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/checks/compatibility/django_1_8_0.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.conf import settings
from .. import Tags, Warning, register

@register(Tags.compatibility)
def check_duplicate_template_settings(app_configs, **kwargs):
    if settings.TEMPLATES:
        values = [b'TEMPLATE_DIRS',
         b'TEMPLATE_CONTEXT_PROCESSORS',
         b'TEMPLATE_DEBUG',
         b'TEMPLATE_LOADERS',
         b'TEMPLATE_STRING_IF_INVALID']
        defined = [ value for value in values if getattr(settings, value, None) ]
        if defined:
            return [
             Warning(b'The standalone TEMPLATE_* settings were deprecated in Django 1.8 and the TEMPLATES dictionary takes precedence. You must put the values of the following settings into your default TEMPLATES dict: %s.' % (b', ').join(defined), id=b'1_8.W001')]
    return []