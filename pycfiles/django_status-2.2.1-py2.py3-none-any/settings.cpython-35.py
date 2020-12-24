# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/perdy/Development/django-status/status/settings.py
# Compiled at: 2016-09-28 11:10:01
# Size of source mod 2**32: 1224 bytes
"""
Settings.
"""
from django.conf import settings
DEBUG = getattr(settings, 'DEBUG', False)
INSTALLED_APPS = settings.INSTALLED_APPS
CACHES = settings.CACHES
BASE_DIR = getattr(settings, 'BASE_DIR', None)
CELERY_WORKERS = getattr(settings, 'STATUS_CELERY_WORKERS', ())
PROVIDERS = getattr(settings, 'STATUS_PROVIDERS', {'health': (('ping', 'status.providers.health.ping', None, None), ('databases', 'status.providers.health.databases', None, None),
 ('caches', 'status.providers.health.caches', None, None)), 
 
 'stats': (('databases', 'status.providers.stats.databases', None, None), ('code', 'status.providers.stats.code', None, None))})
if CELERY_WORKERS:
    PROVIDERS['health'] += (
     (
      'celery', 'status.providers.health.celery', None, {'workers': CELERY_WORKERS}),)
    PROVIDERS['stats'] += (
     (
      'celery', 'status.providers.stats.celery', None, {'workers': CELERY_WORKERS}),)