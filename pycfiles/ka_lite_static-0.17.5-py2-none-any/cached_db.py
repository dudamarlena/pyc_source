# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/sessions/backends/cached_db.py
# Compiled at: 2018-07-11 18:15:30
"""
Cached, database-backed sessions.
"""
from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.core.cache import cache
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
KEY_PREFIX = 'django.contrib.sessions.cached_db'

class SessionStore(DBStore):
    """
    Implements cached, database backed sessions.
    """

    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    @property
    def cache_key(self):
        return KEY_PREFIX + self._get_or_create_session_key()

    def load(self):
        try:
            data = cache.get(self.cache_key, None)
        except Exception:
            data = None

        if data is None:
            try:
                s = Session.objects.get(session_key=self.session_key, expire_date__gt=timezone.now())
                data = self.decode(s.session_data)
                cache.set(self.cache_key, data, self.get_expiry_age(expiry=s.expire_date))
            except (Session.DoesNotExist, SuspiciousOperation):
                self.create()
                data = {}

        return data

    def exists(self, session_key):
        if KEY_PREFIX + session_key in cache:
            return True
        return super(SessionStore, self).exists(session_key)

    def save(self, must_create=False):
        super(SessionStore, self).save(must_create)
        cache.set(self.cache_key, self._session, self.get_expiry_age())

    def delete(self, session_key=None):
        super(SessionStore, self).delete(session_key)
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        cache.delete(KEY_PREFIX + session_key)
        return

    def flush(self):
        """
        Removes the current session data from the database and regenerates the
        key.
        """
        self.clear()
        self.delete(self.session_key)
        self.create()


from django.contrib.sessions.models import Session