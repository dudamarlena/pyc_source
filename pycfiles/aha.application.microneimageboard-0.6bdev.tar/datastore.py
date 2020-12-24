# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/session/datastore.py
# Compiled at: 2010-10-22 05:19:30
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
import random, pickle, logging
from Cookie import SimpleCookie
from rfc822 import formatdate
from datetime import datetime, timedelta
from time import time
from google.appengine.ext import db
from aha import session
SESSION_DURATION = timedelta(hours=1)

class SessionStore(db.Model):
    id = db.StringProperty()
    value = db.BlobProperty()
    expires = db.DateTimeProperty()

    @classmethod
    def clear(cls):
        lst = cls.gql('WHERE expires < :1', datetime.now()).fetch(1000)
        for item in lst:
            item.delete()


class DatastoreSession(session.Session):
    """ session that uses the datastore """

    def __init__(self, hnd, name=session.COOKIE_NAME, timeout=0):
        super(DatastoreSession, self).__init__(hnd, name, timeout)
        SessionStore.clear()
        if not timeout:
            config = Config()
            timeout = config.get('session_timeout', 3600)
        elif timeout == -1:
            timeout = 1537920000
        if name in hnd.request.cookies:
            self._id = hnd.request.cookies[name]
            res = SessionStore.gql('WHERE id = :1', self._id).get()
            if res:
                self._store = res
                session_data = self._store.value
                if session_data:
                    self.update(pickle.loads(session_data))
            else:
                self._create_store(self._id)
        else:
            c = SimpleCookie()
            c[name] = self._id
            c[name]['path'] = '/'
            c[name]['expires'] = rfc822.formatdate(time() + timeout)
            cs = c.output().replace('Set-Cookie: ', '')
            hnd.response.headers.add_header('Set-Cookie', cs)
            self._create_store(self._id)

    def put(self):
        if not self._invalidated and self._store:
            self._store.value = pickle.dumps(self.copy())
            self._store.expires = datetime.now() + SESSION_DURATION
            self._store.put()

    def invalidate(self):
        """Invalidates the session data"""
        self._hnd.response.headers.add_header('Set-Cookie', '%s = ; expires = Thu, 1-Jan-1970 00:00:00 GMT;' % self._name)
        self._store.delete()
        self._store = None
        self.clear()
        self._invalidated = True
        return

    def _create_store(self, id):
        self._store = SessionStore(id=id, value=pickle.dumps(dict()), expires=datetime.now() + SESSION_DURATION)
        self._store.put()
        self._id = id