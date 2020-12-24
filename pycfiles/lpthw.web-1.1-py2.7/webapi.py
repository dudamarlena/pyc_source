# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/web/webapi.py
# Compiled at: 2011-06-21 16:54:55
"""
Web API (wrapper around WSGI)
(from web.py)
"""
__all__ = [
 'config',
 'header', 'debug',
 'input', 'data',
 'setcookie', 'cookies',
 'ctx',
 'HTTPError',
 'OK', 'Created', 'Accepted',
 'ok', 'created', 'accepted',
 'Redirect', 'Found', 'SeeOther', 'NotModified', 'TempRedirect',
 'redirect', 'found', 'seeother', 'notmodified', 'tempredirect',
 'BadRequest', 'Unauthorized', 'Forbidden', 'NotFound', 'NoMethod', 'NotAcceptable', 'Conflict', 'Gone', 'PreconditionFailed',
 'badrequest', 'unauthorized', 'forbidden', 'notfound', 'nomethod', 'notacceptable', 'conflict', 'gone', 'preconditionfailed',
 'InternalError',
 'internalerror']
import sys, cgi, Cookie, pprint, urlparse, urllib
from utils import storage, storify, threadeddict, dictadd, intget, safestr
config = storage()
config.__doc__ = '\nA configuration object for various aspects of web.py.\n\n`debug`\n   : when True, enables reloading, disabled template caching and sets internalerror to debugerror.\n'

class HTTPError(Exception):

    def __init__(self, status, headers={}, data=''):
        ctx.status = status
        for k, v in headers.items():
            header(k, v)

        self.data = data
        Exception.__init__(self, status)


def _status_code(status, data=None, classname=None, docstring=None):
    if data is None:
        data = status.split(' ', 1)[1]
    classname = status.split(' ', 1)[1].replace(' ', '')
    docstring = docstring or '`%s` status' % status

    def __init__(self, data=data, headers={}):
        HTTPError.__init__(self, status, headers, data)

    return type(classname, (HTTPError, object), {'__doc__': docstring, 
       '__init__': __init__})


ok = OK = _status_code('200 OK', data='')
created = Created = _status_code('201 Created')
accepted = Accepted = _status_code('202 Accepted')

class Redirect(HTTPError):
    """A `301 Moved Permanently` redirect."""

    def __init__(self, url, status='301 Moved Permanently', absolute=False):
        """
        Returns a `status` redirect to the new URL. 
        `url` is joined with the base URL so that things like 
        `redirect("about") will work properly.
        """
        newloc = urlparse.urljoin(ctx.path, url)
        if newloc.startswith('/'):
            if absolute:
                home = ctx.realhome
            else:
                home = ctx.home
            newloc = home + newloc
        headers = {'Content-Type': 'text/html', 
           'Location': newloc}
        HTTPError.__init__(self, status, headers, '')


redirect = Redirect

class Found(Redirect):
    """A `302 Found` redirect."""

    def __init__(self, url, absolute=False):
        Redirect.__init__(self, url, '302 Found', absolute=absolute)


found = Found

class SeeOther(Redirect):
    """A `303 See Other` redirect."""

    def __init__(self, url, absolute=False):
        Redirect.__init__(self, url, '303 See Other', absolute=absolute)


seeother = SeeOther

class NotModified(HTTPError):
    """A `304 Not Modified` status."""

    def __init__(self):
        HTTPError.__init__(self, '304 Not Modified')


notmodified = NotModified

class TempRedirect(Redirect):
    """A `307 Temporary Redirect` redirect."""

    def __init__(self, url, absolute=False):
        Redirect.__init__(self, url, '307 Temporary Redirect', absolute=absolute)


tempredirect = TempRedirect

class BadRequest(HTTPError):
    """`400 Bad Request` error."""
    message = 'bad request'

    def __init__(self):
        status = '400 Bad Request'
        headers = {'Content-Type': 'text/html'}
        HTTPError.__init__(self, status, headers, self.message)


badrequest = BadRequest

class _NotFound(HTTPError):
    """`404 Not Found` error."""
    message = 'not found'

    def __init__(self, message=None):
        status = '404 Not Found'
        headers = {'Content-Type': 'text/html'}
        HTTPError.__init__(self, status, headers, message or self.message)


def NotFound(message=None):
    """Returns HTTPError with '404 Not Found' error from the active application.
    """
    if message:
        return _NotFound(message)
    else:
        if ctx.get('app_stack'):
            return ctx.app_stack[(-1)].notfound()
        return _NotFound()


notfound = NotFound
unauthorized = Unauthorized = _status_code('401 Unauthorized')
forbidden = Forbidden = _status_code('403 Forbidden')
notacceptable = NotAcceptable = _status_code('406 Not Acceptable')
conflict = Conflict = _status_code('409 Conflict')
preconditionfailed = PreconditionFailed = _status_code('412 Precondition Failed')

class NoMethod(HTTPError):
    """A `405 Method Not Allowed` error."""

    def __init__(self, cls=None):
        status = '405 Method Not Allowed'
        headers = {}
        headers['Content-Type'] = 'text/html'
        methods = [
         'GET', 'HEAD', 'POST', 'PUT', 'DELETE']
        if cls:
            methods = [ method for method in methods if hasattr(cls, method) ]
        headers['Allow'] = (', ').join(methods)
        data = None
        HTTPError.__init__(self, status, headers, data)
        return


nomethod = NoMethod

class Gone(HTTPError):
    """`410 Gone` error."""
    message = 'gone'

    def __init__(self):
        status = '410 Gone'
        headers = {'Content-Type': 'text/html'}
        HTTPError.__init__(self, status, headers, self.message)


gone = Gone

class _InternalError(HTTPError):
    """500 Internal Server Error`."""
    message = 'internal server error'

    def __init__(self, message=None):
        status = '500 Internal Server Error'
        headers = {'Content-Type': 'text/html'}
        HTTPError.__init__(self, status, headers, message or self.message)


def InternalError(message=None):
    """Returns HTTPError with '500 internal error' error from the active application.
    """
    if message:
        return _InternalError(message)
    else:
        if ctx.get('app_stack'):
            return ctx.app_stack[(-1)].internalerror()
        return _InternalError()


internalerror = InternalError

def header(hdr, value, unique=False):
    """
    Adds the header `hdr: value` with the response.
    
    If `unique` is True and a header with that name already exists,
    it doesn't add a new one. 
    """
    hdr, value = safestr(hdr), safestr(value)
    if '\n' in hdr or '\r' in hdr or '\n' in value or '\r' in value:
        raise ValueError, 'invalid characters in header'
    if unique is True:
        for h, v in ctx.headers:
            if h.lower() == hdr.lower():
                return

    ctx.headers.append((hdr, value))


def rawinput(method=None):
    """Returns storage object with GET or POST arguments.
    """
    method = method or 'both'
    from cStringIO import StringIO

    def dictify(fs):
        if fs.list is None:
            fs.list = []
        return dict([ (k, fs[k]) for k in fs.keys() ])

    e = ctx.env.copy()
    a = b = {}
    if method.lower() in ('both', 'post', 'put'):
        if e['REQUEST_METHOD'] in ('POST', 'PUT'):
            if e.get('CONTENT_TYPE', '').lower().startswith('multipart/'):
                a = ctx.get('_fieldstorage')
                if not a:
                    fp = e['wsgi.input']
                    a = cgi.FieldStorage(fp=fp, environ=e, keep_blank_values=1)
                    ctx._fieldstorage = a
            else:
                fp = StringIO(data())
                a = cgi.FieldStorage(fp=fp, environ=e, keep_blank_values=1)
            a = dictify(a)
    if method.lower() in ('both', 'get'):
        e['REQUEST_METHOD'] = 'GET'
        b = dictify(cgi.FieldStorage(environ=e, keep_blank_values=1))

    def process_fieldstorage(fs):
        if isinstance(fs, list):
            return [ process_fieldstorage(x) for x in fs ]
        else:
            if fs.filename is None:
                return fs.value
            else:
                return fs

            return

    return storage([ (k, process_fieldstorage(v)) for k, v in dictadd(b, a).items() ])


def input(*requireds, **defaults):
    """
    Returns a `storage` object with the GET and POST arguments. 
    See `storify` for how `requireds` and `defaults` work.
    """
    _method = defaults.pop('_method', 'both')
    out = rawinput(_method)
    try:
        defaults.setdefault('_unicode', True)
        return storify(out, *requireds, **defaults)
    except KeyError:
        raise badrequest()


def data():
    """Returns the data sent with the request."""
    if 'data' not in ctx:
        cl = intget(ctx.env.get('CONTENT_LENGTH'), 0)
        ctx.data = ctx.env['wsgi.input'].read(cl)
    return ctx.data


def setcookie(name, value, expires='', domain=None, secure=False, httponly=False):
    """Sets a cookie."""
    if expires < 0:
        expires = -1000000000
    kargs = {'expires': expires, 'path': '/'}
    if domain:
        kargs['domain'] = domain
    if secure:
        kargs['secure'] = secure
    cookie = Cookie.SimpleCookie()
    cookie[name] = urllib.quote(safestr(value))
    for key, val in kargs.iteritems():
        cookie[name][key] = val

    value = cookie.items()[0][1].OutputString()
    if httponly:
        value += '; httponly'
    header('Set-Cookie', value)


def cookies(*requireds, **defaults):
    """
    Returns a `storage` object with all the cookies in it.
    See `storify` for how `requireds` and `defaults` work.
    """
    cookie = Cookie.SimpleCookie()
    cookie.load(ctx.env.get('HTTP_COOKIE', ''))
    try:
        d = storify(cookie, *requireds, **defaults)
        for k, v in d.items():
            d[k] = v and urllib.unquote(v)

        return d
    except KeyError:
        badrequest()
        raise StopIteration


def debug(*args):
    """
    Prints a prettyprinted version of `args` to stderr.
    """
    try:
        out = ctx.environ['wsgi.errors']
    except:
        out = sys.stderr

    for arg in args:
        print >> out, pprint.pformat(arg)

    return ''


def _debugwrite(x):
    try:
        out = ctx.environ['wsgi.errors']
    except:
        out = sys.stderr

    out.write(x)


debug.write = _debugwrite
ctx = context = threadeddict()
ctx.__doc__ = '\nA `storage` object containing various information about the request:\n  \n`environ` (aka `env`)\n   : A dictionary containing the standard WSGI environment variables.\n\n`host`\n   : The domain (`Host` header) requested by the user.\n\n`home`\n   : The base path for the application.\n\n`ip`\n   : The IP address of the requester.\n\n`method`\n   : The HTTP method used.\n\n`path`\n   : The path request.\n   \n`query`\n   : If there are no query arguments, the empty string. Otherwise, a `?` followed\n     by the query string.\n\n`fullpath`\n   : The full path requested, including query arguments (`== path + query`).\n\n### Response Data\n\n`status` (default: "200 OK")\n   : The status code to be used in the response.\n\n`headers`\n   : A list of 2-tuples to be used in the response.\n\n`output`\n   : A string to be used as the response.\n'