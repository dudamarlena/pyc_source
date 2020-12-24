# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cspace/hgsite/util.py
# Compiled at: 2012-11-20 19:18:50
"""Utilities
Copyright (C) 2012 Remy Blank
"""
import mimetypes, os, re, stat, time
from urllib import quote, quote_plus
from mercurial.node import hex

class Namespace(object):
    """An object serving as a namespace."""
    pass


def get_ext(path):
    """Return the extension of the given path.

    For paths without extensions, the basename is returned."""
    return path.rsplit('/', 1)[(-1)].rsplit('.', 1)[(-1)]


def guess_mimetype(mimetype, path, default):
    """Return the given mime type if already set, or guess it from the file
    extension, or return the default if guessing fails."""
    if mimetype:
        return mimetype
    mimetype, encoding = mimetypes.guess_type(path, False)
    if mimetype:
        return mimetype
    return default


_weekdays = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
_months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov',
           'Dec')

def http_date(t=None):
    """Return the given timesamp formatted as an HTTP date."""
    tm = time.gmtime(t)
    return '%s, %02d %s %04d %02d:%02d:%02d GMT' % (
     _weekdays[tm.tm_wday], tm.tm_mday, _months[(tm.tm_mon - 1)], tm.tm_year,
     tm.tm_hour, tm.tm_min, tm.tm_sec)


def unicode_quote(value, safe='/'):
    """Unicode-aware version of `quote()`."""
    return quote(value.encode('utf-8') if isinstance(value, unicode) else str(value), safe)


def unicode_quote_plus(value, safe=''):
    """Unicode-aware version of `quote_plus()`."""
    return quote_plus(value.encode('utf-8') if isinstance(value, unicode) else str(value), safe)


def unicode_urlencode(params, safe=''):
    """Encode URL query parameters."""
    return ('&').join(unicode_quote_plus(param[0], safe) + '=' + unicode_quote_plus(param[1], safe) for param in params)


_eol = re.compile('\r\n|\n|\r')

def find_line_no(pattern, text, occurrence=1, flags=0):
    """Find the given pattern in `text` and return the line number of the
    start of the first capturing group, or the line number of the start of the
    nth match if there are no capturing groups."""
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern, re.M | re.S | flags)
    group = 1 if pattern.groups > 0 else 0
    for match in pattern.finditer(text):
        occurrence -= 1
        if occurrence <= 0:
            return 1 + sum(1 for m in _eol.finditer(text, 0, match.start(group)))


_digits = re.compile('(\\d+)')

def natural_sort_key(s):
    """Return a natural sort key for the given string."""
    parts = _digits.split(s)
    parts[1::2] = map(int, parts[1::2])
    return parts


_url_safe = "/!~*'()"

def href_builder(base):
    """Return a URL builder with the given base."""
    base = base.rstrip('/')

    def build_href(*args, **kwargs):
        """Build URLs for a given base."""
        if args:
            href = base + '/' + ('/').join(unicode_quote(unicode(arg).strip('/'), _url_safe) for arg in args if arg)
        else:
            href = base or '/'
        if kwargs:
            href += '?' + unicode_urlencode((kv for kv in kwargs.iteritems() if kv[1] is not None), _url_safe)
        return href

    return build_href


def hex_node(ctx):
    """Return the hex representation of the node of the given context, or an
    empty string if this is a `workingctx`."""
    return hex(ctx.node() or '')


def exists_in_wc(repo, path):
    """Return True iff the given path exists in the working copy."""
    try:
        st = os.lstat(repo.wjoin(path))
    except OSError:
        return False

    return stat.S_IFMT(st.st_mode) in (stat.S_IFREG, stat.S_IFLNK)


def file_exists(ctx, path):
    """Return `True` iff the path exists in the given context."""
    if ctx.node() is None:
        return exists_in_wc(ctx._repo, path)
    else:
        return path in ctx


def exec_file(ctx, path, symbols=None):
    """Execute a repository file as Python code in a namespace object."""
    namespace = Namespace()
    if symbols:
        namespace.__dict__.update(symbols)
    exec ctx[path].data() in namespace.__dict__
    return namespace