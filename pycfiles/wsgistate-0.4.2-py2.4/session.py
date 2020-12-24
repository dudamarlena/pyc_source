# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wsgistate/session.py
# Compiled at: 2007-10-22 20:26:07
import os, string, weakref, atexit, cgi, urllib, sha, random, sys
from Cookie import SimpleCookie
from urllib import quote
try:
    import threading
except ImportError:
    import dummy_threading as threading

from wsgistate import synchronized
__all__ = [
 'SessionCache', 'SessionManager', 'CookieSession', 'URLSession', 'session', 'urlsession']

def _shutdown(ref):
    cache = ref()
    if cache is not None:
        cache.shutdown()
    return


def session(cache, **kw):
    """Decorator for sessions."""

    def decorator(application):
        return CookieSession(application, cache, **kw)

    return decorator


def urlsession(cache, **kw):
    """Decorator for URL encoded sessions."""

    def decorator(application):
        return URLSession(application, cache, **kw)

    return decorator


class SessionCache(object):
    """Base class for session cache. You first acquire a session by
    calling create() or checkout(). After using the session, you must call
    checkin(). You must not keep references to sessions outside of a check
    in/check out block. Always obtain a fresh reference.
    """
    __module__ = __name__
    idchars = ('-_').join([string.digits, string.ascii_letters])
    length = 64

    def __init__(self, cache, **kw):
        self._lock = threading.Condition()
        self.checkedout, self._closed, self.cache = dict(), False, cache
        self._random = kw.get('random', False)
        self._secret = ('').join((self.idchars[(ord(c) % len(self.idchars))] for c in os.urandom(self.length)))
        atexit.register(_shutdown, weakref.ref(self))

    def __del__(self):
        self.shutdown()

    @synchronized
    def create(self):
        """Create a new session with a unique identifier.

        The newly-created session should eventually be released by
        a call to checkin().
        """
        sid, sess = self.newid(), dict()
        self.cache.set(sid, sess)
        self.checkedout[sid] = sess
        return (sid, sess)

    @synchronized
    def checkout(self, sid):
        """Checks out a session for use. Returns the session if it exists,
        otherwise returns None. If this call succeeds, the session
        will be touch()'ed and locked from use by other processes.
        Therefore, it should eventually be released by a call to
        checkin().

        @param sid Session id
        """
        while sid in self.checkedout:
            self._lock.wait()

        sess = self.cache.get(sid)
        if sess is not None:
            if self._random:
                self.cache.delete(sid)
                sid = self.newid()
            self.checkedout[sid] = sess
            return (sid, sess)
        return (None, None)

    @synchronized
    def checkin(self, sid, sess):
        """Returns the session for use by other threads/processes.

        @param sid Session id
        @param session Session dictionary
        """
        del self.checkedout[sid]
        self.cache.set(sid, sess)
        self._lock.notify()

    @synchronized
    def shutdown(self):
        """Clean up outstanding sessions."""
        if not self._closed:
            for (sid, sess) in self.checkedout.iteritems():
                self.cache.set(sid, sess)

            self.checkedout.clear()
            self.cache._cull()
            self._closed = True

    def newid(self):
        """Returns session key that is not being used."""
        sid = None
        for num in xrange(10000):
            sid = sha.new(str(random.randint(0, sys.maxint - 1)) + str(random.randint(0, sys.maxint - 1)) + self._secret).hexdigest()
            if sid not in self.cache:
                break

        return sid


class SessionManager(object):
    """Session Manager."""
    __module__ = __name__

    def __init__(self, cache, environ, **kw):
        self._cache = cache
        self._fieldname = kw.get('fieldname', '_SID_')
        self._path = kw.get('path', '/')
        self.session = self._sid = self._csid = None
        self.expired = self.current = self.new = self.inurl = False
        self._get(environ)
        return

    def _fromcookie(self, environ):
        """Attempt to load the associated session using the identifier from
        the cookie.
        """
        cookie = SimpleCookie(environ.get('HTTP_COOKIE'))
        morsel = cookie.get(self._fieldname, None)
        if morsel is not None:
            (self._sid, self.session) = self._cache.checkout(morsel.value)
            self._csid = morsel.value
            if self._csid != self._sid:
                self.new = True
        return

    def _fromquery(self, environ):
        """Attempt to load the associated session using the identifier from
        the query string.
        """
        self._qdict = dict(cgi.parse_qsl(environ.get('QUERY_STRING', '')))
        value = self._qdict.get(self._fieldname)
        if value is not None:
            (self._sid, self.session) = self._cache.checkout(value)
            if self._sid is not None:
                self._csid, self.inurl = value, True
                if self._csid != self._sid:
                    self.current = self.new = True
        return

    def _get(self, environ):
        """Attempt to associate with an existing Session."""
        self._fromcookie(environ)
        if self.session is None:
            self._fromquery(environ)
        if self.session is None:
            (self._sid, self.session) = self._cache.create()
            self.new = True
        return

    def close(self):
        """Checks session back into session cache."""
        self._cache.checkin(self._sid, self.session)
        self.session = None
        return

    def setcookie(self, headers):
        """Sets a cookie header if needed."""
        cookie, name = SimpleCookie(), self._fieldname
        cookie[name], cookie[name]['path'] = self._sid, self._path
        headers.append(('Set-Cookie', cookie[name].OutputString()))

    def seturl(self, environ):
        """Encodes session ID in URL, if necessary."""
        path = ('').join([quote(environ.get('SCRIPT_NAME', '')), quote(environ.get('PATH_INFO', ''))])
        if self._qdict:
            self._qdict[self._fieldname] = self._sid
        else:
            self._qdict = {self._fieldname: self._sid}
        return ('?').join([path, urllib.urlencode(self._qdict)])


class _Session(object):
    """WSGI middleware that adds a session service."""
    __module__ = __name__

    def __init__(self, application, cache, **kw):
        self.application, self.cache, self.kw = application, cache, kw
        self.key = kw.get('key', 'com.saddi.service.session')

    def __call__(self, environ, start_response):
        sess = SessionManager(self.cache, environ, **self.kw)
        environ[self.key] = sess
        try:
            if sess.new:
                return self._initial(environ, start_response)
            return self.application(environ, start_response)
        finally:
            sess.close()


class CookieSession(_Session):
    """WSGI middleware that adds a session service in a cookie."""
    __module__ = __name__

    def _initial(self, environ, start_response):
        """Initial response to a cookie session."""

        def session_response(status, headers, exc_info=None):
            environ[self.key].setcookie(headers)
            return start_response(status, headers, exc_info)

        return self.application(environ, session_response)


class URLSession(_Session):
    """WSGI middleware that adds a session service in a URL query string."""
    __module__ = __name__

    def _initial(self, environ, start_response):
        """Initial response to a query encoded session."""
        url = environ[self.key].seturl(environ)
        start_response('302 Found', [('location', url)])
        return ['The browser is being redirected to %s' % url]