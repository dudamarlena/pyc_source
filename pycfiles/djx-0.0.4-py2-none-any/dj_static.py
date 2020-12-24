# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/dj-static/dj_static.py
# Compiled at: 2019-02-14 00:35:17
import static
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.contrib.staticfiles.handlers import StaticFilesHandler as DebugHandler
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from django.contrib.staticfiles import utils
try:
    from django.core.handlers.wsgi import get_path_info
except ImportError:
    try:
        from django.core.handlers.base import get_path_info
    except ImportError:
        import sys
        py3 = sys.version_info[0] == 3

        def get_path_info(environ):
            """
            Returns the HTTP request's PATH_INFO as a unicode string.
            """
            path_info = environ.get('PATH_INFO', str('/'))
            if py3:
                path_info = path_info.encode('iso-8859-1')
            return path_info.decode('utf-8')


class Cling(WSGIHandler):
    """WSGI middleware that intercepts calls to the static files
    directory, as defined by the STATIC_URL setting, and serves those files.
    """

    def __init__(self, application, base_dir=None, ignore_debug=False):
        self.application = application
        self.ignore_debug = ignore_debug
        if not base_dir:
            base_dir = self.get_base_dir()
        self.base_url = urlparse(self.get_base_url())
        self.cling = static.Cling(base_dir)
        try:
            self.debug_cling = DebugHandler(application, base_dir=base_dir)
        except TypeError:
            self.debug_cling = DebugHandler(application)

        super(Cling, self).__init__()

    def get_base_dir(self):
        return settings.STATIC_ROOT

    def get_base_url(self):
        utils.check_settings()
        return settings.STATIC_URL

    @property
    def debug(self):
        return settings.DEBUG

    def _transpose_environ(self, environ):
        """Translates a given environ to static.Cling's expectations."""
        environ['PATH_INFO'] = environ['PATH_INFO'][len(self.base_url[2]) - 1:]
        return environ

    def _should_handle(self, path):
        """Checks if the path should be handled. Ignores the path if:

        * the host is provided as part of the base_url
        * the request's path isn't under the media path (or equal)
        """
        return path.startswith(self.base_url[2]) and not self.base_url[1]

    def __call__(self, environ, start_response):
        if not self._should_handle(get_path_info(environ)):
            return self.application(environ, start_response)
        else:
            if not self.debug or self.ignore_debug:
                environ = self._transpose_environ(environ)
                return self.cling(environ, start_response)
            return self.debug_cling(environ, start_response)


class MediaCling(Cling):

    def __init__(self, application, base_dir=None):
        super(MediaCling, self).__init__(application, base_dir=base_dir)
        self.debug_cling = self._debug_cling

    def _debug_cling(self, environ, start_response):
        environ = self._transpose_environ(environ)
        return self.cling(environ, start_response)

    def get_base_dir(self):
        return settings.MEDIA_ROOT

    def get_base_url(self):
        return settings.MEDIA_URL