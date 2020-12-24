# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/badgr/settings.py
# Compiled at: 2012-09-15 13:37:21
"""
These Flickr settings should not be edited directly.
Instead, overwrite them in the main project's setting file.
"""
from django.conf import settings
from django.core.cache import cache
FLICKR_APIKEY = getattr(settings, 'FLICKR_APIKEY', None)
FLICKR_USERID = getattr(settings, 'FLICKR_USERID', None)
FLICKR_NUMPHOTOS = getattr(settings, 'FLICKR_NUMPHOTOS', 12)
FLICKR_TIMEOUT = getattr(settings, 'FLICKR_TIMEOUT', cache.default_timeout)
FLICKR_IMAGESIZE = getattr(settings, 'FLICKR_IMAGESIZE', '')