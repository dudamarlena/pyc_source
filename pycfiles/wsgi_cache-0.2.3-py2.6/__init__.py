# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wsgi_cache/__init__.py
# Compiled at: 2011-07-27 11:37:00
import fcntl, os, cPickle as pickle

class CacheMiddleware(object):
    """A WSGI Middleware class that blindly caches the results of requests
    to the disk."""

    def __init__(self, app, global_conf, cache_dir, content_type='text/html', cache_paths=None, directory_index='__index.html'):
        self.app = app
        self.conf = global_conf
        self.content_type = content_type
        self.directory_index = directory_index
        self.cache_dir = os.path.join(global_conf.get('here'), os.path.normpath(cache_dir))
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        if cache_paths is None:
            self.cache_paths = None
        else:
            self.cache_paths = [ p.strip() for p in cache_paths.split(',') ]
            for path in self.cache_paths:
                assert path[0] == '/'

            return

    def resource_name(self, environ):
        """Return the resource name for the request in the provided environ."""
        return environ['PATH_INFO'][1:]

    def resource_cache_name(self, resource):
        """Return the path name to the specified resource in the cache."""
        cache_name = os.path.join(self.cache_dir, resource)
        if resource.endswith('/'):
            cache_name = os.path.join(cache_name, self.directory_index)
        return cache_name

    def cached(self, resource):
        """Return True if the specified resource is cached; the resource is
        the cache identifier."""
        cache_name = self.resource_cache_name(resource)
        return os.path.exists(cache_name) and not os.path.getsize(cache_name) == 0 and not os.path.isdir(cache_name)

    def store(self, resource, contents):
        """Store the resource contents in the cache."""
        cache_filename = self.resource_cache_name(resource)
        if not os.path.exists(os.path.dirname(cache_filename)):
            os.makedirs(os.path.dirname(cache_filename))
        try:
            try:
                cache = file(cache_filename, 'w')
                fcntl.lockf(cache, fcntl.LOCK_EX | fcntl.LOCK_NB)
                for line in contents:
                    cache.write(line)

                fcntl.lockf(cache, fcntl.LOCK_UN)
            except IOError:
                return

        finally:
            cache.close()

    __setitem__ = store

    def load(self, resource):
        """Load the resource from the cache."""
        return iter(file(self.resource_cache_name(resource), 'r'))

    __getitem__ = load

    def __serve_cached(self, environ, start_response):
        identifier = self.resource_name(environ)
        response = dict(status='200 OK', headers=[
         (
          'Content-type', self.content_type)])

        def sr(status, headers):
            response['status'] = status
            response['headers'] = headers

        if self.cached(identifier):
            response['contents'] = self.load(identifier)
        else:
            response['contents'] = self.app(environ, sr)
            if response['status'] == '200 OK' and ('Cache-Control', 'no-cache') not in response['headers']:
                self.store(identifier, response['contents'])
        start_response(response['status'], response['headers'])
        return response['contents']

    def __call__(self, environ, start_response):
        if environ['QUERY_STRING']:
            return self.app(environ, start_response)
        if self.cache_paths:
            for cp in self.cache_paths:
                if environ['PATH_INFO'].startswith(cp):
                    return self.__serve_cached(environ, start_response)

            return self.app(environ, start_response)
        return self.__serve_cached(environ, start_response)