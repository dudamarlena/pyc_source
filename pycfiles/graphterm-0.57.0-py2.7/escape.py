# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/tornado/escape.py
# Compiled at: 2012-01-23 23:44:33
"""Escaping/unescaping methods for HTML, JSON, URLs, and others.

Also includes a few other miscellaneous string manipulation functions that
have crept in over time.
"""
import htmlentitydefs, re, sys, urllib
try:
    bytes
except Exception:
    bytes = str

try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

try:
    import json
    assert hasattr(json, 'loads') and hasattr(json, 'dumps')
    _json_decode = json.loads
    _json_encode = json.dumps
except Exception:
    try:
        import simplejson
        _json_decode = lambda s: simplejson.loads(_unicode(s))
        _json_encode = lambda v: simplejson.dumps(v)
    except ImportError:
        try:
            from django.utils import simplejson
            _json_decode = lambda s: simplejson.loads(_unicode(s))
            _json_encode = lambda v: simplejson.dumps(v)
        except ImportError:

            def _json_decode(s):
                raise NotImplementedError('A JSON parser is required, e.g., simplejson at http://pypi.python.org/pypi/simplejson/')


            _json_encode = _json_decode

_XHTML_ESCAPE_RE = re.compile('[&<>"]')
_XHTML_ESCAPE_DICT = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}

def xhtml_escape(value):
    """Escapes a string so it is valid within XML or XHTML."""
    return _XHTML_ESCAPE_RE.sub(lambda match: _XHTML_ESCAPE_DICT[match.group(0)], to_basestring(value))


def xhtml_unescape(value):
    """Un-escapes an XML-escaped string."""
    return re.sub('&(#?)(\\w+?);', _convert_entity, _unicode(value))


def json_encode(value):
    """JSON-encodes the given Python object."""
    return _json_encode(recursive_unicode(value)).replace('</', '<\\/')


def json_decode(value):
    """Returns Python objects for the given JSON string."""
    return _json_decode(to_basestring(value))


def squeeze(value):
    """Replace all sequences of whitespace chars with a single space."""
    return re.sub('[\\x00-\\x20]+', ' ', value).strip()


def url_escape(value):
    """Returns a valid URL-encoded version of the given value."""
    return urllib.quote_plus(utf8(value))


if sys.version_info[0] < 3:

    def url_unescape(value, encoding='utf-8'):
        """Decodes the given value from a URL.

        The argument may be either a byte or unicode string.

        If encoding is None, the result will be a byte string.  Otherwise,
        the result is a unicode string in the specified encoding.
        """
        if encoding is None:
            return urllib.unquote_plus(utf8(value))
        else:
            return unicode(urllib.unquote_plus(utf8(value)), encoding)
            return


    parse_qs_bytes = parse_qs
else:

    def url_unescape(value, encoding='utf-8'):
        """Decodes the given value from a URL.

        The argument may be either a byte or unicode string.

        If encoding is None, the result will be a byte string.  Otherwise,
        the result is a unicode string in the specified encoding.
        """
        if encoding is None:
            return urllib.parse.unquote_to_bytes(value)
        else:
            return urllib.unquote_plus(to_basestring(value), encoding=encoding)
            return


    def parse_qs_bytes(qs, keep_blank_values=False, strict_parsing=False):
        """Parses a query string like urlparse.parse_qs, but returns the
        values as byte strings.

        Keys still become type str (interpreted as latin1 in python3!)
        because it's too painful to keep them as byte strings in
        python3 and in practice they're nearly always ascii anyway.
        """
        result = parse_qs(qs, keep_blank_values, strict_parsing, encoding='latin1', errors='strict')
        encoded = {}
        for k, v in result.iteritems():
            encoded[k] = [ i.encode('latin1') for i in v ]

        return encoded


_UTF8_TYPES = (
 bytes, type(None))

def utf8(value):
    """Converts a string argument to a byte string.

    If the argument is already a byte string or None, it is returned unchanged.
    Otherwise it must be a unicode string and is encoded as utf8.
    """
    if isinstance(value, _UTF8_TYPES):
        return value
    assert isinstance(value, unicode)
    return value.encode('utf-8')


_TO_UNICODE_TYPES = (
 unicode, type(None))

def to_unicode(value):
    """Converts a string argument to a unicode string.

    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    assert isinstance(value, bytes)
    return value.decode('utf-8')


_unicode = to_unicode
if str is unicode:
    native_str = to_unicode
else:
    native_str = utf8
_BASESTRING_TYPES = (basestring, type(None))

def to_basestring(value):
    """Converts a string argument to a subclass of basestring.

    In python2, byte and unicode strings are mostly interchangeable,
    so functions that deal with a user-supplied argument in combination
    with ascii string constants can use either and should return the type
    the user supplied.  In python3, the two types are not interchangeable,
    so this method is needed to convert byte strings to unicode.
    """
    if isinstance(value, _BASESTRING_TYPES):
        return value
    assert isinstance(value, bytes)
    return value.decode('utf-8')


def recursive_unicode(obj):
    """Walks a simple data structure, converting byte strings to unicode.

    Supports lists, tuples, and dictionaries.
    """
    if isinstance(obj, dict):
        return dict((recursive_unicode(k), recursive_unicode(v)) for k, v in obj.iteritems())
    else:
        if isinstance(obj, list):
            return list(recursive_unicode(i) for i in obj)
        if isinstance(obj, tuple):
            return tuple(recursive_unicode(i) for i in obj)
        if isinstance(obj, bytes):
            return to_unicode(obj)
        return obj


_URL_RE = re.compile('\\b((?:([\\w-]+):(/{1,3})|www[.])(?:(?:(?:[^\\s&()]|&amp;|&quot;)*(?:[^!"#$%&\'()*+,.:;<=>?@\\[\\]^`{|}~\\s]))|(?:\\((?:[^\\s&()]|&amp;|&quot;)*\\)))+)')

def linkify(text, shorten=False, extra_params='', require_protocol=False, permitted_protocols=['http', 'https']):
    """Converts plain text into HTML with links.

    For example: ``linkify("Hello http://tornadoweb.org!")`` would return
    ``Hello <a href="http://tornadoweb.org">http://tornadoweb.org</a>!``

    Parameters:

    shorten: Long urls will be shortened for display.

    extra_params: Extra text to include in the link tag,
        e.g. linkify(text, extra_params='rel="nofollow" class="external"')

    require_protocol: Only linkify urls which include a protocol. If this is
        False, urls such as www.facebook.com will also be linkified.

    permitted_protocols: List (or set) of protocols which should be linkified,
        e.g. linkify(text, permitted_protocols=["http", "ftp", "mailto"]).
        It is very unsafe to include protocols such as "javascript".
    """
    if extra_params:
        extra_params = ' ' + extra_params.strip()

    def make_link(m):
        url = m.group(1)
        proto = m.group(2)
        if require_protocol and not proto:
            return url
        if proto and proto not in permitted_protocols:
            return url
        href = m.group(1)
        if not proto:
            href = 'http://' + href
        params = extra_params
        max_len = 30
        if shorten and len(url) > max_len:
            before_clip = url
            if proto:
                proto_len = len(proto) + 1 + len(m.group(3) or '')
            else:
                proto_len = 0
            parts = url[proto_len:].split('/')
            if len(parts) > 1:
                url = url[:proto_len] + parts[0] + '/' + parts[1][:8].split('?')[0].split('.')[0]
            if len(url) > max_len * 1.5:
                url = url[:max_len]
            if url != before_clip:
                amp = url.rfind('&')
                if amp > max_len - 5:
                    url = url[:amp]
                url += '...'
                if len(url) >= len(before_clip):
                    url = before_clip
                else:
                    params += ' title="%s"' % href
        return '<a href="%s"%s>%s</a>' % (href, params, url)

    text = _unicode(xhtml_escape(text))
    return _URL_RE.sub(make_link, text)


def _convert_entity(m):
    if m.group(1) == '#':
        try:
            return unichr(int(m.group(2)))
        except ValueError:
            return '&#%s;' % m.group(2)

    try:
        return _HTML_UNICODE_MAP[m.group(2)]
    except KeyError:
        return '&%s;' % m.group(2)


def _build_unicode_map():
    unicode_map = {}
    for name, value in htmlentitydefs.name2codepoint.iteritems():
        unicode_map[name] = unichr(value)

    return unicode_map


_HTML_UNICODE_MAP = _build_unicode_map()