# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/cascade.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = '\nCascades through several applications, so long as applications\nreturn ``404 Not Found``.\n'
from paste import httpexceptions
from paste.util import converters
import tempfile
from cStringIO import StringIO
__all__ = [
 'Cascade']

def make_cascade(loader, global_conf, catch='404', **local_conf):
    """
    Entry point for Paste Deploy configuration
    
    Expects configuration like::

        [composit:cascade]
        use = egg:Paste#cascade
        # all start with 'app' and are sorted alphabetically
        app1 = foo
        app2 = bar
        ...
        catch = 404 500 ...
    """
    catch = map(int, converters.aslist(catch))
    apps = []
    for (name, value) in local_conf.items():
        if not name.startswith('app'):
            raise ValueError("Bad configuration key %r (=%r); all configuration keys must start with 'app'" % (
             name, value))
        app = loader.get_app(value, global_conf=global_conf)
        apps.append((name, app))

    apps.sort()
    apps = [ app for (name, app) in apps ]
    return Cascade(apps, catch=catch)


class Cascade(object):
    """
    Passed a list of applications, ``Cascade`` will try each of them
    in turn.  If one returns a status code listed in ``catch`` (by
    default just ``404 Not Found``) then the next application is
    tried.

    If all applications fail, then the last application's failure
    response is used.

    Instances of this class are WSGI applications.
    """

    def __init__(self, applications, catch=(404, )):
        self.apps = applications
        self.catch_codes = {}
        self.catch_exceptions = []
        for error in catch:
            if isinstance(error, str):
                error = int(error.split(None, 1)[0])
            if isinstance(error, httpexceptions.HTTPException):
                exc = error
                code = error.code
            else:
                exc = httpexceptions.get_exception(error)
                code = error
            self.catch_codes[code] = exc
            self.catch_exceptions.append(exc)

        self.catch_exceptions = tuple(self.catch_exceptions)
        return

    def __call__(self, environ, start_response):
        """
        WSGI application interface
        """
        failed = []

        def repl_start_response(status, headers, exc_info=None):
            code = int(status.split(None, 1)[0])
            if code in self.catch_codes:
                failed.append(None)
                return _consuming_writer
            else:
                return start_response(status, headers, exc_info)

        try:
            length = int(environ.get('CONTENT_LENGTH', 0) or 0)
        except ValueError:
            length = 0

        if length > 0:
            copy_wsgi_input = True
            if length > 4096 or length < 0:
                f = tempfile.TemporaryFile()
                if length < 0:
                    f.write(environ['wsgi.input'].read())
                copy_len = length
                while copy_len > 0:
                    chunk = environ['wsgi.input'].read(min(copy_len, 4096))
                    if not chunk:
                        raise IOError('Request body truncated')
                    f.write(chunk)
                    copy_len -= len(chunk)

                f.seek(0)
            else:
                f = StringIO(environ['wsgi.input'].read(length))
            environ['wsgi.input'] = f
        else:
            copy_wsgi_input = False
        for app in self.apps[:-1]:
            environ_copy = environ.copy()
            if copy_wsgi_input:
                environ_copy['wsgi.input'].seek(0)
            failed = []
            try:
                v = app(environ_copy, repl_start_response)
                if not failed:
                    return v
                if hasattr(v, 'close'):
                    list(v)
                    v.close()
            except self.catch_exceptions, e:
                pass

        if copy_wsgi_input:
            environ['wsgi.input'].seek(0)
        return self.apps[(-1)](environ, start_response)


def _consuming_writer(s):
    pass