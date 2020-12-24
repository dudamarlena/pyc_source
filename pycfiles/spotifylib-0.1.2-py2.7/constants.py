# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/spotifylib/constants.py
# Compiled at: 2017-10-13 08:20:21
"""
defines constants

Static URL's and variables
"""
from urlparse import urlparse
SITE = 'https://accounts.spotify.com'
AUTH_API_URL = ('{SITE}/authorize').format(SITE=SITE)
API_LOGIN_URL = ('{SITE}/api/login').format(SITE=SITE)
LOGIN_WEB_URL = ('{SITE}/en/login').format(SITE=SITE)
AUTH_WEB_URL = ('{SITE}/en/authorize').format(SITE=SITE)
ACCEPT_URL = ('{AUTH_URL}/accept').format(AUTH_URL=AUTH_WEB_URL)
TOKEN_URL = ('{SITE}/api/token').format(SITE=SITE)
HEADERS = {'Host': urlparse(SITE).netloc, 'Accept': 'application/json, text/plain, */*', 
   'Content-Type': 'application/x-www-form-urlencoded'}
INVALID_TOKEN_MSG = {'error': {'status': 401, 'message': 'The access token expired'}}