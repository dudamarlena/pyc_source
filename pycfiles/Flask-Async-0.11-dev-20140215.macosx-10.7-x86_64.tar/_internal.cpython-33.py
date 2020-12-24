# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/werkzeug/_internal.py
# Compiled at: 2014-01-20 15:46:16
# Size of source mod 2**32: 13713 bytes
"""
    werkzeug._internal
    ~~~~~~~~~~~~~~~~~~

    This module provides internally used helpers and constants.

    :copyright: (c) 2013 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
import re, string, inspect
from weakref import WeakKeyDictionary
from datetime import datetime, date
from itertools import chain
from werkzeug._compat import iter_bytes, text_type, BytesIO, int_to_byte, range_type, to_native
_logger = None
_empty_stream = BytesIO()
_signature_cache = WeakKeyDictionary()
_epoch_ord = date(1970, 1, 1).toordinal()
_cookie_params = set((b'expires', b'path', b'comment', b'max-age', b'secure', b'httponly',
                      b'version'))
_legal_cookie_chars = (string.ascii_letters + string.digits + "!#$%&'*+-.^_`|~:").encode('ascii')
_cookie_quoting_map = {b',': b'\\054', 
 b';': b'\\073', 
 b'"': b'\\"', 
 b'\\': b'\\\\'}
for _i in chain(range_type(32), range_type(127, 256)):
    _cookie_quoting_map[int_to_byte(_i)] = ('\\%03o' % _i).encode('latin1')

_octal_re = re.compile(b'\\\\[0-3][0-7][0-7]')
_quote_re = re.compile(b'[\\\\].')
_legal_cookie_chars_re = b"[\\w\\d!#%&'~_`><@,:/\\$\\*\\+\\-\\.\\^\\|\\)\\(\\?\\}\\{\\=]"
_cookie_re = re.compile(b'(?x)\n    (?P<key>[^=]+)\n    \\s*=\\s*\n    (?P<val>\n        "(?:[^\\\\"]|\\\\.)*" |\n         (?:.*?)\n    )\n    \\s*;\n')

class _Missing(object):

    def __repr__(self):
        return 'no value'

    def __reduce__(self):
        return '_missing'


_missing = _Missing()

def _get_environ(obj):
    env = getattr(obj, 'environ', obj)
    assert isinstance(env, dict), '%r is not a WSGI environment (has to be a dict)' % type(obj).__name__
    return env


def _log(type, message, *args, **kwargs):
    """Log into the internal werkzeug logger."""
    global _logger
    if _logger is None:
        import logging
        _logger = logging.getLogger('werkzeug')
        if not logging.root.handlers:
            if _logger.level == logging.NOTSET:
                _logger.setLevel(logging.INFO)
                handler = logging.StreamHandler()
                _logger.addHandler(handler)
    getattr(_logger, type)(message.rstrip(), *args, **kwargs)
    return


def _parse_signature(func):
    """Return a signature object for the function."""
    if hasattr(func, 'im_func'):
        func = func.im_func
    parse = _signature_cache.get(func)
    if parse is not None:
        return parse
    else:
        positional, vararg_var, kwarg_var, defaults = inspect.getargspec(func)
        defaults = defaults or ()
        arg_count = len(positional)
        arguments = []
        for idx, name in enumerate(positional):
            if isinstance(name, list):
                raise TypeError('cannot parse functions that unpack tuples in the function signature')
            try:
                default = defaults[(idx - arg_count)]
            except IndexError:
                param = (
                 name, False, None)
            else:
                param = (
                 name, True, default)
            arguments.append(param)

        arguments = tuple(arguments)

        def parse(args, kwargs):
            new_args = []
            missing = []
            extra = {}
            for idx, (name, has_default, default) in enumerate(arguments):
                try:
                    new_args.append(args[idx])
                except IndexError:
                    try:
                        new_args.append(kwargs.pop(name))
                    except KeyError:
                        if has_default:
                            new_args.append(default)
                        else:
                            missing.append(name)

                else:
                    if name in kwargs:
                        extra[name] = kwargs.pop(name)
                        continue

            extra_positional = args[arg_count:]
            if vararg_var is not None:
                new_args.extend(extra_positional)
                extra_positional = ()
            if kwargs:
                if kwarg_var is None:
                    extra.update(kwargs)
                    kwargs = {}
            return (
             new_args, kwargs, missing, extra, extra_positional,
             arguments, vararg_var, kwarg_var)

        _signature_cache[func] = parse
        return parse


def _date_to_unix(arg):
    """Converts a timetuple, integer or datetime object into the seconds from
    epoch in utc.
    """
    if isinstance(arg, datetime):
        arg = arg.utctimetuple()
    elif isinstance(arg, (int, long, float)):
        return int(arg)
    year, month, day, hour, minute, second = arg[:6]
    days = date(year, month, 1).toordinal() - _epoch_ord + day - 1
    hours = days * 24 + hour
    minutes = hours * 60 + minute
    seconds = minutes * 60 + second
    return seconds


class _DictAccessorProperty(object):
    __doc__ = 'Baseclass for `environ_property` and `header_property`.'
    read_only = False

    def __init__(self, name, default=None, load_func=None, dump_func=None, read_only=None, doc=None):
        self.name = name
        self.default = default
        self.load_func = load_func
        self.dump_func = dump_func
        if read_only is not None:
            self.read_only = read_only
        self.__doc__ = doc
        return

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        else:
            storage = self.lookup(obj)
            if self.name not in storage:
                return self.default
            rv = storage[self.name]
            if self.load_func is not None:
                try:
                    rv = self.load_func(rv)
                except (ValueError, TypeError):
                    rv = self.default

            return rv

    def __set__(self, obj, value):
        if self.read_only:
            raise AttributeError('read only property')
        if self.dump_func is not None:
            value = self.dump_func(value)
        self.lookup(obj)[self.name] = value
        return

    def __delete__(self, obj):
        if self.read_only:
            raise AttributeError('read only property')
        self.lookup(obj).pop(self.name, None)
        return

    def __repr__(self):
        return '<%s %s>' % (
         self.__class__.__name__,
         self.name)


def _cookie_quote(b):
    buf = bytearray()
    all_legal = True
    _lookup = _cookie_quoting_map.get
    _push = buf.extend
    for char in iter_bytes(b):
        if char not in _legal_cookie_chars:
            all_legal = False
            char = _lookup(char, char)
        _push(char)

    if all_legal:
        return bytes(buf)
    return bytes(b'"' + buf + b'"')


def _cookie_unquote(b):
    if len(b) < 2:
        return b
    if b[:1] != b'"' or b[-1:] != b'"':
        return b
    b = b[1:-1]
    i = 0
    n = len(b)
    rv = bytearray()
    _push = rv.extend
    while 0 <= i < n:
        o_match = _octal_re.search(b, i)
        q_match = _quote_re.search(b, i)
        if not o_match:
            if not q_match:
                rv.extend(b[i:])
                break
        j = k = -1
        if o_match:
            j = o_match.start(0)
        if q_match:
            k = q_match.start(0)
        if q_match and (not o_match or k < j):
            _push(b[i:k])
            _push(b[k + 1:k + 2])
            i = k + 2
        else:
            _push(b[i:j])
            rv.append(int(b[j + 1:j + 4], 8))
            i = j + 4

    return bytes(rv)


def _cookie_parse_impl(b):
    """Lowlevel cookie parsing facility that operates on bytes."""
    i = 0
    n = len(b)
    while i < n:
        match = _cookie_re.search(b + b';', i)
        if not match:
            break
        key = match.group('key').strip()
        value = match.group('val')
        i = match.end(0)
        if key.lower() not in _cookie_params:
            yield (
             _cookie_unquote(key), _cookie_unquote(value))
            continue


def _encode_idna(domain):
    if not isinstance(domain, text_type):
        domain.decode('ascii')
        return domain
    try:
        return domain.encode('ascii')
    except UnicodeError:
        pass

    parts = domain.split('.')
    for idx, part in enumerate(parts):
        parts[idx] = part.encode('idna')

    return (b'.').join(parts)


def _decode_idna(domain):
    if isinstance(domain, text_type):
        try:
            domain = domain.encode('ascii')
        except UnicodeError:
            return domain

    parts = domain.split(b'.')
    for idx, part in enumerate(parts):
        try:
            parts[idx] = part.decode('idna')
        except UnicodeError:
            parts[idx] = part.decode('ascii', 'ignore')

    return '.'.join(parts)


def _make_cookie_domain(domain):
    if domain is None:
        return
    else:
        domain = _encode_idna(domain)
        if b':' in domain:
            domain = domain.split(b':', 1)[0]
        if b'.' in domain:
            return domain
        raise ValueError("Setting 'domain' for a cookie on a server running localy (ex: localhost) is not supportted by complying browsers. You should have something like: '127.0.0.1 localhost dev.localhost' on your hosts file and then point your server to run on 'dev.localhost' and also set 'domain' for 'dev.localhost'")
        return


def _easteregg(app=None):
    """Like the name says.  But who knows how it works?"""

    def bzzzzzzz(gyver):
        import base64, zlib
        return zlib.decompress(base64.b64decode(gyver)).decode('ascii')

    gyver = '\n'.join([x + (77 - len(x)) * ' ' for x in bzzzzzzz(b'\n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\n7f2zLkGNv8b191cD/3vs9Q833z8t').splitlines()])

    def easteregged(environ, start_response):

        def injecting_start_response(status, headers, exc_info=None):
            headers.append(('X-Powered-By', 'Werkzeug'))
            return start_response(status, headers, exc_info)

        if app is not None and environ.get('QUERY_STRING') != 'macgybarchakku':
            return app(environ, injecting_start_response)
        else:
            injecting_start_response('200 OK', [('Content-Type', 'text/html')])
            return [
             ('\n<!DOCTYPE html>\n<html>\n<head>\n<title>About Werkzeug</title>\n<style type="text/css">\n  body { font: 15px Georgia, serif; text-align: center; }\n  a { color: #333; text-decoration: none; }\n  h1 { font-size: 30px; margin: 20px 0 10px 0; }\n  p { margin: 0 0 30px 0; }\n  pre { font: 11px \'Consolas\', \'Monaco\', monospace; line-height: 0.95; }\n</style>\n</head>\n<body>\n<h1><a href="http://werkzeug.pocoo.org/">Werkzeug</a></h1>\n<p>the Swiss Army knife of Python web development.</p>\n<pre>%s\n\n\n</pre>\n</body>\n</html>' % gyver).encode('latin1')]

    return easteregged