# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/djbetty/conf/defaults.py
# Compiled at: 2016-10-10 15:46:48
# Size of source mod 2**32: 363 bytes
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from django.conf import settings as _settings
BETTY_ADMIN_URL = urljoin(_settings.MEDIA_URL, 'images/')
BETTY_IMAGE_URL = urljoin(_settings.MEDIA_URL, 'images/')
BETTY_PUBLIC_TOKEN = None
BETTY_PRIVATE_TOKEN = None
BETTY_DEFAULT_IMAGE = None
BETTY_INLINE_JS = True