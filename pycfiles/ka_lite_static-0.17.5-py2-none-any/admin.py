# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/admin.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
from django.conf import settings
from django.contrib import admin
if b'django.contrib.auth' in settings.INSTALLED_APPS:
    from tastypie.models import ApiKey

    class ApiKeyInline(admin.StackedInline):
        model = ApiKey
        extra = 0


    ABSTRACT_APIKEY = getattr(settings, b'TASTYPIE_ABSTRACT_APIKEY', False)
    if ABSTRACT_APIKEY and not isinstance(ABSTRACT_APIKEY, bool):
        raise TypeError(b"'TASTYPIE_ABSTRACT_APIKEY' must be either 'True' or 'False'.")
    if not ABSTRACT_APIKEY:
        admin.site.register(ApiKey)