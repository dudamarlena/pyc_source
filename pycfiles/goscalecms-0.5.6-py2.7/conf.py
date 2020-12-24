# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/conf.py
# Compiled at: 2013-02-15 05:53:31
import os
from django.conf import settings
gettext_noop = lambda s: s
DEFAULT_LANGUAGE = getattr(settings, 'DEFAULT_LANGUAGE', 'en')
GOSCALE_DEFAULT_POST_PLUGIN = getattr(settings, 'GOSCALE_DEFAULT_POST_PLUGIN', 'post.html')
GOSCALE_UPDATE_FROM_ADMIN = getattr(settings, 'GOSCALE_UPDATE_FROM_ADMIN', False)
CELERY_IMPORTS = getattr(settings, 'CELERY_IMPORTS', ())
GOSCALE_POSTS_UPDATE_FREQUENCY = getattr(settings, 'GOSCALE_POSTS_UPDATE_FREQUENCY', 1800)
GOSCALE_CACHE_DURATION = getattr(settings, 'GOSCALE_CACHE_DURATION', getattr(settings, 'CMS_CACHE_DURATIONS', {'content': 1})['content'])
GOSCALE_BROWSER_CACHE_MAX_AGE = getattr(settings, 'GOSCALE_CACHE_DURATION', GOSCALE_CACHE_DURATION)
GOSCALE_STANDARD_TZ_DELTA = getattr(settings, 'GOSCALE_STANDARD_TZ_DELTA', 0)
GOSCALE_POST_SUMMARY_LIMIT = getattr(settings, 'GOSCALE_POST_SUMMARY_LIMIT', 300)
GOSCALE_DEFAULT_PAGE_SIZE = getattr(settings, 'GOSCALE_DEFAULT_PAGE_SIZE', 10)
GOSCALE_DEFAULT_BLOG = getattr(settings, 'DEFAULT_BLOG', '')
GOSCALE_GOOGLE_ACCOUNT = getattr(settings, 'GOSCALE_GOOGLE_ACCOUNT', '')
GOSCALE_GOOGLE_ACCOUNT_PASSWORD = getattr(settings, 'GOSCALE_GOOGLE_ACCOUNT_PASSWORD', '')
GOSCALE_JSON_INDENT = getattr(settings, 'GOSCALE_JSON_INDENT', 4 if settings.DEBUG else 0)
GOSCALE_DEFAULT_CONTENT_ORDER = getattr(settings, 'GOSCALE_DEFAULT_CONTENT_ORDER', '-published')
GOSCALE_ROOT_TEMPLATE_DIR = 'goscale'
GOSCALE_ATOM_DATETIME_FORMAT = getattr(settings, 'GOSCALE_ATOM_DATETIME_FORMAT', '%Y-%m-%dT%H:%M:%S')
GOSCALE_RSS_DATETIME_FORMAT = getattr(settings, 'GOSCALE_RSS_DATETIME_FORMAT', '%a, %d %b %Y %H:%M:%S')
GOSCALE_SUPPORTED_OUTPUT_FORMATS = getattr(settings, 'GOSCALE_SUPPORTED_OUTPUT_FORMATS', ['html', 'rss', 'json', 'atom'])