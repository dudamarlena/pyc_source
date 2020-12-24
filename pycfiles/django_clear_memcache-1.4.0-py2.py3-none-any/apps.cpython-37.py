# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enrico/pyenv/uvena_de/django_clear_memcache/apps.py
# Compiled at: 2014-12-09 17:05:32
# Size of source mod 2**32: 365 bytes
try:
    from django.apps import AppConfig
    import django.utils.translation as _
except ImportError:
    pass
else:

    class ClearMemcacheConfig(AppConfig):
        name = 'django_clear_memcache'
        verbose_name = _('Clear Memcache')