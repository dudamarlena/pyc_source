# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tornado_extensions/sessions/backends/cache.py
# Compiled at: 2013-09-03 05:36:04
from tornado_extensions.cache import cache
from tornado_extensions.sessions.backends.base import SessionBase, CreateError
from tornado import gen

class SessionStore(SessionBase):
    """
    A cache-based session store.
    """
    prefix = 'p:'

    def __init__(self, *args, **kwargs):
        self._cache = cache
        super(SessionStore, self).__init__(*args, **kwargs)

    @property
    def cache_key(self):
        return self.prefix + self._get_or_create_session_key()

    @gen.engine
    def load(self, callback=None):
        self.loaded = True
        try:
            session_data = yield gen.Task(self._cache.get, self.cache_key, None)
            print session_data, 'session data'
        except Exception:
            session_data = None

        if session_data is not None:
            self._session_cache = session_data
            if callback:
                callback(session_data)
            raise StopIteration
        self.create()
        if callback:
            self._session_cache = {}
            callback(self._session)
        return

    def create(self):
        for i in xrange(10000):
            self._session_key = self._get_new_session_key()
            try:
                yield gen.Task(self.save, must_create=True)
            except CreateError:
                continue

            self.modified = True
            return

        raise RuntimeError('Unable to create a new session key.')

    @gen.engine
    def save(self, must_create=False, callback=None):
        if must_create:
            func = self._cache.add
        else:
            func = self._cache.set
        result = yield gen.Task(func, self.cache_key, self._get_session(), self.get_expiry_age())
        if must_create and not result:
            raise CreateError
        if callback:
            callback(None)
        return

    @gen.engine
    def exists(self, session_key, callback=None):
        result = yield gen.Task(self._cache.has_key, self.prefix + session_key)
        if callback:
            callback(result)

    @gen.engine
    def delete(self, session_key=None, callback=None):
        if session_key is None:
            if self.session_key is None:
                if callback:
                    callback(None)
                raise StopIteration
            session_key = self.session_key
        yield gen.Task(self._cache.delete, self.prefix + session_key)
        if callback:
            callback(None)
        return