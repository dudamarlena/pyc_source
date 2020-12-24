# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/context_processors.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 528 bytes
from django.conf import settings
from moneta import __version__ as version
__author__ = 'flanker'

def context_base(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    is_os_x = 'macintosh' in user_agent
    is_linux = 'linux' in user_agent
    absolute_url = settings.SERVER_BASE_URL[:-1]
    return {'absolute_url':absolute_url,  'use_https':absolute_url.startswith('https'),  'is_linux':is_linux, 
     'is_os_x':is_os_x,  'moneta_version':version,  'server_name':settings.SERVER_NAME}