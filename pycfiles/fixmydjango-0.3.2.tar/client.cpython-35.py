# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filipeximenes/Projects/fixmydjango-lib/fixmydjango/client.py
# Compiled at: 2017-09-13 09:06:32
# Size of source mod 2**32: 630 bytes
import requests
from django.conf import settings
base_url = getattr(settings, 'FIX_MY_DJANGO_API_BASE_URL', 'http://www.fixmydjango.com')

def search_exceptions(exception_type, raised_by, raised_by_line='', django_version='', base_url=base_url):
    search_path = '/api/search/'
    url = '{0}{1}'.format(base_url, search_path)
    return requests.get(url, params={'exception_type': exception_type, 
     'raised_by': raised_by, 
     'raised_by_line': raised_by_line, 
     'django_version': django_version}, headers={'Accept': 'application/json'}).json()