# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/session/memcache.py
# Compiled at: 2010-10-22 05:17:53
__doc__ = ' GAEO Session - memcache store '
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
import random, pickle, logging, Cookie
from rfc822 import formatdate
from datetime import datetime
from time import time
from google.appengine.api import memcache
from aha import session, Config

class MemcacheSession(session.Session):
    """ session that uses memcache """

    def __init__(self, hnd, name=session.COOKIE_NAME, timeout=0):
        """
        timeout = 0  : setting timeout based on config.
        timeout = -1 : setting timeout to the long future.
        other than above : everlasting.
        """
        if not timeout:
            config = Config()
            timeout = getattr(config, 'session_timeout', 3600)
        elif timeout == -1:
            timeout = 1537920000
        super(MemcacheSession, self).__init__(hnd, name, timeout)
        if name in hnd.request.cookies:
            self._id = hnd.request.cookies[name]
            session_data = memcache.get(self._id)
            if session_data:
                self.update(pickle.loads(session_data))
                memcache.set(self._id, session_data, timeout)
        else:
            c = Cookie.SimpleCookie()
            c[name] = self._id
            c[name]['path'] = '/'
            c[name]['expires'] = formatdate(time() + timeout)
            cs = c.output().replace('Set-Cookie: ', '')
            hnd.response.headers.add_header('Set-Cookie', cs)

    def put(self):
        if not self._invalidated:
            memcache.set(self._id, pickle.dumps(self.copy()), self._timeout)

    def invalidate(self):
        """Invalidates the session data"""
        self._hnd.response.headers.add_header('Set-Cookie', '%s = ; expires = Thu, 1-Jan-1970 00:00:00 GMT;' % self._name)
        memcache.delete(self._id)
        self.clear()
        self._invalidated = True