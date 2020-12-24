# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hgwebproxy/settings.py
# Compiled at: 2009-08-02 23:57:27
import os
from django.conf import settings
STATIC_URL = getattr(settings, 'HGPROXY_STATIC_URL', os.path.join(settings.MEDIA_URL, 'hg/'))
AUTH_REALM = getattr(settings, 'HGPROXY_AUTH_RELAM', 'Basic Auth')