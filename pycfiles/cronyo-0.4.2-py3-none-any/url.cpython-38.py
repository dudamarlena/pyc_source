# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/urllib3/util/url.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 14230 bytes
from __future__ import absolute_import
import re
from collections import namedtuple
from ..exceptions import LocationParseError
from ..packages import six
url_attrs = [
 'scheme', 'auth', 'host', 'port', 'path', 'query', 'fragment']
NORMALIZABLE_SCHEMES = ('http', 'https', None)
PERCENT_RE = re.compile('%[a-fA-F0-9]{2}')
SCHEME_RE = re.compile('^(?:[a-zA-Z][a-zA-Z0-9+-]*:|/)')
URI_RE = re.compile('^(?:([a-zA-Z][a-zA-Z0-9+.-]*):)?(?://([^/?#]*))?([^?#]*)(?:\\?([^#]*))?(?:#(.*))?$', re.UNICODE | re.DOTALL)
IPV4_PAT = '(?:[0-9]{1,3}\\.){3}[0-9]{1,3}'
HEX_PAT = '[0-9A-Fa-f]{1,4}'
LS32_PAT = '(?:{hex}:{hex}|{ipv4})'.format(hex=HEX_PAT, ipv4=IPV4_PAT)
_subs = {'hex':HEX_PAT,  'ls32':LS32_PAT}
_variations = [
 '(?:%(hex)s:){6}%(ls32)s',
 '::(?:%(hex)s:){5}%(ls32)s',
 '(?:%(hex)s)?::(?:%(hex)s:){4}%(ls32)s',
 '(?:(?:%(hex)s:)?%(hex)s)?::(?:%(hex)s:){3}%(ls32)s',
 '(?:(?:%(hex)s:){0,2}%(hex)s)?::(?:%(hex)s:){2}%(ls32)s',
 '(?:(?:%(hex)s:){0,3}%(hex)s)?::%(hex)s:%(ls32)s',
 '(?:(?:%(hex)s:){0,4}%(hex)s)?::%(ls32)s',
 '(?:(?:%(hex)s:){0,5}%(hex)s)?::%(hex)s',
 '(?:(?:%(hex)s:){0,6}%(hex)s)?::']
UNRESERVED_PAT = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._!\\-~'
IPV6_PAT = '(?:' + '|'.join([x % _subs for x in _variations]) + ')'
ZONE_ID_PAT = '(?:%25|%)(?:[' + UNRESERVED_PAT + ']|%[a-fA-F0-9]{2})+'
IPV6_ADDRZ_PAT = '\\[' + IPV6_PAT + '(?:' + ZONE_ID_PAT + ')?\\]'
REG_NAME_PAT = '(?:[^\\[\\]%:/?#]|%[a-fA-F0-9]{2})*'
TARGET_RE = re.compile('^(/[^?]*)(?:\\?([^#]+))?(?:#(.*))?$')
IPV4_RE = re.compile('^' + IPV4_PAT + '$')
IPV6_RE = re.compile('^' + IPV6_PAT + '$')
IPV6_ADDRZ_RE = re.compile('^' + IPV6_ADDRZ_PAT + '$')
BRACELESS_IPV6_ADDRZ_RE = re.compile('^' + IPV6_ADDRZ_PAT[2:-2] + '$')
ZONE_ID_RE = re.compile('(' + ZONE_ID_PAT + ')\\]$')
SUBAUTHORITY_PAT = '^(?:(.*)@)?(%s|%s|%s)(?::([0-9]{0,5}))?$' % (
 REG_NAME_PAT,
 IPV4_PAT,
 IPV6_ADDRZ_PAT)
SUBAUTHORITY_RE = re.compile(SUBAUTHORITY_PAT, re.UNICODE | re.DOTALL)
UNRESERVED_CHARS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-~')
SUB_DELIM_CHARS = set("!$&'()*+,;=")
USERINFO_CHARS = UNRESERVED_CHARS | SUB_DELIM_CHARS | {':'}
PATH_CHARS = USERINFO_CHARS | {'@', '/'}
QUERY_CHARS = FRAGMENT_CHARS = PATH_CHARS | {'?'}

class Url(namedtuple('Url', url_attrs)):
    __doc__ = '\n    Data structure for representing an HTTP URL. Used as a return value for\n    :func:`parse_url`. Both the scheme and host are normalized as they are\n    both case-insensitive according to RFC 3986.\n    '
    __slots__ = ()

    def __new__(cls, scheme=None, auth=None, host=None, port=None, path=None, query=None, fragment=None):
        if path:
            if not path.startswith('/'):
                path = '/' + path
        if scheme is not None:
            scheme = scheme.lower()
        return super(Url, cls).__new__(cls, scheme, auth, host, port, path, query, fragment)

    @property
    def hostname(self):
        """For backwards-compatibility with urlparse. We're nice like that."""
        return self.host

    @property
    def request_uri(self):
        """Absolute path including the query string."""
        uri = self.path or '/'
        if self.query is not None:
            uri += '?' + self.query
        return uri

    @property
    def netloc(self):
        """Network location including host and port"""
        if self.port:
            return '%s:%d' % (self.host, self.port)
        return self.host

    @property
    def url(self):
        """
        Convert self into a url

        This function should more or less round-trip with :func:`.parse_url`. The
        returned url may not be exactly the same as the url inputted to
        :func:`.parse_url`, but it should be equivalent by the RFC (e.g., urls
        with a blank port will have : removed).

        Example: ::

            >>> U = parse_url('http://google.com/mail/')
            >>> U.url
            'http://google.com/mail/'
            >>> Url('http', 'username:password', 'host.com', 80,
            ... '/path', 'query', 'fragment').url
            'http://username:password@host.com:80/path?query#fragment'
        """
        scheme, auth, host, port, path, query, fragment = self
        url = ''
        if scheme is not None:
            url += scheme + '://'
        if auth is not None:
            url += auth + '@'
        if host is not None:
            url += host
        if port is not None:
            url += ':' + str(port)
        if path is not None:
            url += path
        if query is not None:
            url += '?' + query
        if fragment is not None:
            url += '#' + fragment
        return url

    def __str__(self):
        return self.url


def split_first(s, delims):
    """
    .. deprecated:: 1.25

    Given a string and an iterable of delimiters, split on the first found
    delimiter. Return two split parts and the matched delimiter.

    If not found, then the first part is the full input string.

    Example::

        >>> split_first('foo/bar?baz', '?/=')
        ('foo', 'bar?baz', '/')
        >>> split_first('foo/bar?baz', '123')
        ('foo/bar?baz', '', None)

    Scales linearly with number of delims. Not ideal for large number of delims.
    """
    min_idx = None
    min_delim = None
    for d in delims:
        idx = s.find(d)
        if idx < 0:
            pass
        else:
            if not min_idx is None:
                if idx < min_idx:
                    min_idx = idx
                    min_delim = d
                if min_idx is None or min_idx < 0:
                    return (
                     s, '', None)
            return (
             s[:min_idx], s[min_idx + 1:], min_delim)


def _encode_invalid_chars(component, allowed_chars, encoding='utf-8'):
    """Percent-encodes a URI component without reapplying
    onto an already percent-encoded component.
    """
    if component is None:
        return component
    component = six.ensure_text(component)
    percent_encodings = PERCENT_RE.findall(component)
    for enc in percent_encodings:
        if not enc.isupper():
            component = component.replace(enc, enc.upper())
        uri_bytes = component.encode('utf-8', 'surrogatepass')
        is_percent_encoded = len(percent_encodings) == uri_bytes.count(b'%')
        encoded_component = bytearray()
        for i in range(0, len(uri_bytes)):
            byte = uri_bytes[i:i + 1]
            byte_ord = ord(byte)
            if not (is_percent_encoded and byte == b'%'):
                if byte_ord < 128:
                    if byte.decode() in allowed_chars:
                        encoded_component.extend(byte)
                encoded_component.extend(b'%' + hex(byte_ord)[2:].encode().zfill(2).upper())
            return encoded_component.decode(encoding)


def _remove_path_dot_segments(path):
    segments = path.split('/')
    output = []
    for segment in segments:
        if segment == '.':
            continue
        elif segment != '..':
            output.append(segment)
        else:
            if output:
                output.pop()
            if path.startswith('/'):
                if not output or output[0]:
                    output.insert(0, '')
            if path.endswith(('/.', '/..')):
                output.append('')
            return '/'.join(output)


def _normalize_host(host, scheme):
    if host:
        if isinstance(host, six.binary_type):
            host = six.ensure_str(host)
        elif scheme in NORMALIZABLE_SCHEMES:
            is_ipv6 = IPV6_ADDRZ_RE.match(host)
            if is_ipv6:
                match = ZONE_ID_RE.search(host)
                if match:
                    start, end = match.span(1)
                    zone_id = host[start:end]
                    if zone_id.startswith('%25') and zone_id != '%25':
                        zone_id = zone_id[3:]
                    else:
                        zone_id = zone_id[1:]
                    zone_id = '%' + _encode_invalid_chars(zone_id, UNRESERVED_CHARS)
                    return host[:start].lower() + zone_id + host[end:]
                    return host.lower()
                else:
                    pass
            if not IPV4_RE.match(host):
                return six.ensure_str((b'.').join([_idna_encode(label) for label in host.split('.')]))
    return host


def _idna_encode--- This code section failed: ---

 L. 306         0  LOAD_FAST                'name'
                2  POP_JUMP_IF_FALSE   138  'to 138'
                4  LOAD_GLOBAL              any
                6  LOAD_LISTCOMP            '<code_object <listcomp>>'
                8  LOAD_STR                 '_idna_encode.<locals>.<listcomp>'
               10  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               12  LOAD_FAST                'name'
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  CALL_FUNCTION_1       1  ''
               20  POP_JUMP_IF_FALSE   138  'to 138'

 L. 307        22  SETUP_FINALLY        36  'to 36'

 L. 308        24  LOAD_CONST               0
               26  LOAD_CONST               None
               28  IMPORT_NAME              idna
               30  STORE_FAST               'idna'
               32  POP_BLOCK        
               34  JUMP_FORWARD         72  'to 72'
             36_0  COME_FROM_FINALLY    22  '22'

 L. 309        36  DUP_TOP          
               38  LOAD_GLOBAL              ImportError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    70  'to 70'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 310        50  LOAD_GLOBAL              six
               52  LOAD_METHOD              raise_from

 L. 311        54  LOAD_GLOBAL              LocationParseError
               56  LOAD_STR                 "Unable to parse URL without the 'idna' module"
               58  CALL_FUNCTION_1       1  ''

 L. 312        60  LOAD_CONST               None

 L. 310        62  CALL_METHOD_2         2  ''
               64  POP_TOP          
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            42  '42'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            34  '34'

 L. 314        72  SETUP_FINALLY        96  'to 96'

 L. 315        74  LOAD_FAST                'idna'
               76  LOAD_ATTR                encode
               78  LOAD_FAST                'name'
               80  LOAD_METHOD              lower
               82  CALL_METHOD_0         0  ''
               84  LOAD_CONST               True
               86  LOAD_CONST               True
               88  LOAD_CONST               ('strict', 'std3_rules')
               90  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               92  POP_BLOCK        
               94  RETURN_VALUE     
             96_0  COME_FROM_FINALLY    72  '72'

 L. 316        96  DUP_TOP          
               98  LOAD_FAST                'idna'
              100  LOAD_ATTR                IDNAError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   136  'to 136'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L. 317       112  LOAD_GLOBAL              six
              114  LOAD_METHOD              raise_from

 L. 318       116  LOAD_GLOBAL              LocationParseError
              118  LOAD_STR                 "Name '%s' is not a valid IDNA label"
              120  LOAD_FAST                'name'
              122  BINARY_MODULO    
              124  CALL_FUNCTION_1       1  ''

 L. 318       126  LOAD_CONST               None

 L. 317       128  CALL_METHOD_2         2  ''
              130  POP_TOP          
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM           104  '104'
              136  END_FINALLY      
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM            20  '20'
            138_2  COME_FROM             2  '2'

 L. 320       138  LOAD_FAST                'name'
              140  LOAD_METHOD              lower
              142  CALL_METHOD_0         0  ''
              144  LOAD_METHOD              encode
              146  LOAD_STR                 'ascii'
              148  CALL_METHOD_1         1  ''
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 108


def _encode_target(target):
    """Percent-encodes a request target so that there are no invalid characters"""
    if not target.startswith('/'):
        return target
    path, query, fragment = TARGET_RE.match(target).groups()
    target = _encode_invalid_chars(path, PATH_CHARS)
    query = _encode_invalid_chars(query, QUERY_CHARS)
    fragment = _encode_invalid_chars(fragment, FRAGMENT_CHARS)
    if query is not None:
        target += '?' + query
    if fragment is not None:
        target += '#' + target
    return target


def parse_url(url):
    """
    Given a url, return a parsed :class:`.Url` namedtuple. Best-effort is
    performed to parse incomplete urls. Fields not provided will be None.
    This parser is RFC 3986 compliant.

    The parser logic and helper functions are based heavily on
    work done in the ``rfc3986`` module.

    :param str url: URL to parse into a :class:`.Url` namedtuple.

    Partly backwards-compatible with :mod:`urlparse`.

    Example::

        >>> parse_url('http://google.com/mail/')
        Url(scheme='http', host='google.com', port=None, path='/mail/', ...)
        >>> parse_url('google.com:80')
        Url(scheme=None, host='google.com', port=80, path=None, ...)
        >>> parse_url('/foo?bar')
        Url(scheme=None, host=None, port=None, path='/foo', query='bar', ...)
    """
    if not url:
        return Url()
    source_url = url
    if not SCHEME_RE.search(url):
        url = '//' + url
    try:
        scheme, authority, path, query, fragment = URI_RE.match(url).groups()
        normalize_uri = scheme is None or scheme.lower() in NORMALIZABLE_SCHEMES
        if scheme:
            scheme = scheme.lower()
        elif authority:
            auth, host, port = SUBAUTHORITY_RE.match(authority).groups()
            if auth:
                if normalize_uri:
                    auth = _encode_invalid_chars(auth, USERINFO_CHARS)
            if port == '':
                port = None
        else:
            auth, host, port = (None, None, None)
        if port is not None:
            port = int(port)
            if not 0 <= port <= 65535:
                raise LocationParseError(url)
        host = _normalize_host(host, scheme)
        if normalize_uri:
            if path:
                path = _remove_path_dot_segments(path)
                path = _encode_invalid_chars(path, PATH_CHARS)
        if normalize_uri:
            if query:
                query = _encode_invalid_chars(query, QUERY_CHARS)
        if normalize_uri:
            if fragment:
                fragment = _encode_invalid_chars(fragment, FRAGMENT_CHARS)
    except (ValueError, AttributeError):
        return six.raise_from(LocationParseError(source_url), None)
    else:
        if not path:
            if query is not None or fragment is not None:
                path = ''
            else:
                path = None
        elif isinstance(url, six.text_type):
            ensure_func = six.ensure_text
        else:
            ensure_func = six.ensure_str

        def ensure_type(x):
            if x is None:
                return x
            return ensure_func(x)

        return Url(scheme=(ensure_type(scheme)),
          auth=(ensure_type(auth)),
          host=(ensure_type(host)),
          port=port,
          path=(ensure_type(path)),
          query=(ensure_type(query)),
          fragment=(ensure_type(fragment)))


def get_host(url):
    """
    Deprecated. Use :func:`parse_url` instead.
    """
    p = parse_url(url)
    return (p.scheme or 'http', p.hostname, p.port)