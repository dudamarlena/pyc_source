# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kpages/web.py
# Compiled at: 2018-09-26 02:47:45
"""
    MinxiHandler for kpages
    author comger@gmail.com
    1. auth
    
"""
import json, tornado
from utility import mongo_conv
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

AUTH_KEY = 'authed_user'

class AuthMinix(object):
    uid = property(lambda self: self.current_user['_id'])

    def get_current_user(self):
        user_json = self.get_secure_cookie(AUTH_KEY)
        if not user_json:
            return None
        else:
            return json.loads(user_json)

    def prepare(self):
        if not self.current_user:
            url = __conf__.login_url
            if '?' not in url:
                if urlparse.urlsplit(url).scheme:
                    next_url = self.request.full_url()
                else:
                    next_url = self.request.uri
                url += '?' + urlencode(dict(next=next_url))
            self.redirect(url)
            return

    def login(self, user):
        user = mongo_conv(user)
        self.set_secure_cookie(AUTH_KEY, json.dumps(user))