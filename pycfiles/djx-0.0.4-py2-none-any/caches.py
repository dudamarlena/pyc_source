# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/checks/caches.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS
from . import Error, Tags, register
E001 = Error(b"You must define a '%s' cache in your CACHES setting." % DEFAULT_CACHE_ALIAS, id=b'caches.E001')

@register(Tags.caches)
def check_default_cache_is_configured(app_configs, **kwargs):
    if DEFAULT_CACHE_ALIAS not in settings.CACHES:
        return [E001]
    return []