# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/age/.virtualenvs/twine/lib/python3.6/site-packages/joom/settings.py
# Compiled at: 2017-12-13 07:39:22
# Size of source mod 2**32: 365 bytes
from urllib.parse import urljoin
BASE_URL = 'https://api-merchant.joom.com/'
BASE_ENDPOINT = 'api/v2/'
FULL_BASE_URL = urljoin(BASE_URL, BASE_ENDPOINT)
BASE_AUTHORIZATION_URL = urljoin(FULL_BASE_URL, 'oauth/authorize')
BASE_ACCESS_TOKEN_URL = urljoin(FULL_BASE_URL, 'oauth/access_token')
BASE_REFRESH_TOKEN_URL = urljoin(FULL_BASE_URL, 'oauth/refresh_token')