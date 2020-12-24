# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/urlrelay.py
# Compiled at: 2009-01-14 21:23:25
"""RESTful WSGI URL dispatcher."""
import re, time, copy, random, threading
from fnmatch import translate
__author__ = 'L.C. Rees (lcrees@gmail.com)'
__revision__ = '0.7'
__all__ = ['URLRelay', 'url', 'register']

def synchronized(func):
    """Decorator to lock and unlock a method (Phillip J. Eby).

    @param func Method to decorate
    """

    def wrapper(self, *__args, **__kw):
        self._lock.acquire()
        try:
            return func(self, *__args, **__kw)
        finally:
            self._lock.release()

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper


def _handler(environ, start_response):
    start_response('404 Not Found', [('content-type', 'text/plain')])
    return ['Requested URL was not found on this server.']


def pattern_compile(pattern, pattern_type):
    """Compile pattern."""
    if pattern_type == 'glob':
        pattern = translate(pattern)
    return re.compile(pattern)


class _Registry(object):
    """Maintains order of URL preference while updating the central URL path
    registry."""
    _register = list()

    def __iter__(self):
        """Iterator for registry."""
        return iter(self._register)

    def add(self, pattern, mapping):
        """Add tuple to registry.

        @param pattern URL pattern
        @param mapping WSGI application mapping
        """
        self._register.append((pattern, mapping))

    def get(self):
        """Returns current registry."""
        return tuple(self._register)


_reg = _Registry()

def register(pattern, application, method=None):
    """Registers a pattern, application, and optional HTTP method.

    @param pattern URL pattern
    @param application WSGI application
    @param method HTTP method (default: None)
    """
    if method is None:
        _reg.add(pattern, application)
    else:
        for entry in _reg:
            if entry[0] == pattern:
                entry[1][method] = application
                return

        _reg.add(pattern, {method: application})
    return


def url(pattern, method=None):
    """Decorator for registering a path pattern /application pair.

    @param pattern Regex pattern for path
    @param method HTTP method (default: None)
    """

    def decorator(application):
        register(pattern, application, method)
        return application

    return decorator


class lazy(object):
    """Lazily assign attributes on an instance upon first use."""

    def __init__(self, method):
        self.method = method
        self.name = method.__name__

    def __get__(self, instance, cls):
        if instance is None:
            return self
        value = self.method(instance)
        setattr(instance, self.name, value)
        return value


class MemoryCache(object):
    """Base Cache class."""

    def __init__(self, **kw):
        timeout = kw.get('timeout', 300)
        try:
            timeout = int(timeout)
        except (ValueError, TypeError):
            timeout = 300

        self.timeout = timeout
        random.seed()
        self._cache = dict()
        max_entries = kw.get('max_entries', 300)
        try:
            self._max_entries = int(max_entries)
        except (ValueError, TypeError):
            self._max_entries = 300

        self._maxcull = kw.get('maxcull', 10)
        self._lock = threading.Condition()

    def __getitem__(self, key):
        """Fetch a given key from the cache."""
        return self.get(key)

    def __setitem__(self, key, value):
        """Set a value in the cache. """
        self.set(key, value)

    def __delitem__(self, key):
        """Delete a key from the cache."""
        self.delete(key)

    def __contains__(self, key):
        """Tell if a given key is in the cache."""
        return self.get(key) is not None

    def get(self, key, default=None):
        """Fetch a given key from the cache.  If the key does not exist, return
        default, which itself defaults to None.

        @param key Keyword of item in cache.
        @param default Default value (default: None)
        """
        values = self._cache.get(key)
        if values is None:
            value = default
        elif values[0] < time.time():
            self.delete(key)
            value = default
        else:
            value = values[1]
        return copy.deepcopy(value)

    def set(self, key, value):
        """Set a value in the cache.

        @param key Keyword of item in cache.
        @param value Value to be inserted in cache.
        """
        if len(self._cache) >= self._max_entries:
            self._cull()
        self._cache[key] = (
         time.time() + self.timeout, value)

    def delete(self, key):
        """Delete a key from the cache, failing silently.

        @param key Keyword of item in cache.
        """
        try:
            del self._cache[key]
        except KeyError:
            pass

    def keys(self):
        """Returns a list of keys in the cache."""
        return self._cache.keys()

    def _cull(self):
        """Remove items in cache to make room."""
        num, maxcull = 0, self._maxcull
        for key in self.keys():
            if num <= maxcull:
                if self.get(key) is None:
                    num += 1
            else:
                break

        while len(self.keys()) >= self._max_entries and num <= maxcull:
            self.delete(random.choice(self.keys()))
            num += 1

        return


class URLRelay(object):
    """Passes HTTP requests to a WSGI callable based on URL path component and
    HTTP request method.
    """

    def __init__(self, **kw):
        pattern_type = kw.get('pattern_type', 'regex')
        self._paths = tuple(((pattern_compile(u, pattern_type), v) for (u, v) in kw.get('paths', _reg.get())))
        self._modpath = kw.get('modpath', '')
        self._response = kw.get('handler', _handler)
        self._default = kw.get('default')
        self._maxcull = kw.get('maxcull', 10)
        self._max_entries = kw.get('max_entries', 300)
        self._timeout = kw.get('timeout', 300)

    def __call__(self, env, start_response):
        try:
            (app, arg, kw) = self.resolve(env['PATH_INFO'], env['REQUEST_METHOD'])
            env['wsgiorg.routing_args'] = (
             arg, kw)
        except (ImportError, AttributeError):
            return self._response(env, start_response)

        return app(env, start_response)

    @lazy
    def _cache(self):
        """URL <-> callable mapping Cache."""
        return MemoryCache(timeout=self._timeout, maxcull=self._maxcull, max_entries=self._max_entries)

    def _getapp(self, app):
        """Loads a callable based on its name
    
        @param app An WSGI application"""
        if isinstance(app, basestring):
            try:
                dot = app.rindex('.')
                return getattr(__import__(app[:dot], '', '', ['']), app[dot + 1:])
            except ValueError:
                return __import__(app, '', '', [''])

        return app

    def _loadapp(self, app):
        """Loads an application based on its name.

        @param app Web application name"""
        if self._modpath != '' and isinstance(app, basestring):
            app = ('.').join([self._modpath, app])
        newapp = self._getapp(app)
        return newapp

    def resolve(self, path, method):
        """Fetches a WSGI app based on URL path component and method.

        @param path URL path component
        @param method HTTP method
        """
        key = (':').join([path, method])
        app = self._cache.get(key)
        if app is not None:
            return app
        for (pattern, app) in self._paths:
            search = pattern.search(path)
            if not search:
                continue
            if isinstance(app, dict):
                app = app.get(method)
                if app is None:
                    continue
            app = self._loadapp(app)
            assert hasattr(app, '__call__')
            kw = search.groupdict()
            args = tuple((i for i in search.groups() if i not in kw))
            self._cache[key] = (
             app, args, kw)
            return (app, args, kw)

        if self._default is not None:
            default = self._loadapp(self._default)
            return (default, (), {})
        raise ImportError()
        return