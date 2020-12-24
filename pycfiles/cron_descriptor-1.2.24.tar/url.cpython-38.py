# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """Url"""
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
        uri = self.path or 
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
                    return (s, '', None)
            return (s[:min_idx], s[min_idx + 1:], min_delim)


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
            elif not IPV4_RE.match(host):
                return six.ensure_str((b'.').join([_idna_encode(label) for label in host.split('.')]))
    return host


def _idna_encode--- This code section failed: ---

 L. 306         0  LOAD_FAST                'name'
                2  POP_JUMP_IF_FALSE   138  'to 138'
                4  LOAD_GLOBAL              any
                6  LOAD_LISTCOMP            '<code_object <listcomp>>'
                8  LOAD_STR                 '_idna_encode.<locals>.<listcomp>'
               10  MAKE_FUNCTION_0          ''
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

Parse error at or near `DUP_TOP' instruction at offset 96


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


def parse_url--- This code section failed: ---

 L. 361         0  LOAD_FAST                'url'
                2  POP_JUMP_IF_TRUE     10  'to 10'

 L. 363         4  LOAD_GLOBAL              Url
                6  CALL_FUNCTION_0       0  ''
                8  RETURN_VALUE     
             10_0  COME_FROM             2  '2'

 L. 365        10  LOAD_FAST                'url'
               12  STORE_FAST               'source_url'

 L. 366        14  LOAD_GLOBAL              SCHEME_RE
               16  LOAD_METHOD              search
               18  LOAD_FAST                'url'
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_TRUE     32  'to 32'

 L. 367        24  LOAD_STR                 '//'
               26  LOAD_FAST                'url'
               28  BINARY_ADD       
               30  STORE_FAST               'url'
             32_0  COME_FROM            22  '22'

 L. 369        32  SETUP_FINALLY       286  'to 286'

 L. 370        34  LOAD_GLOBAL              URI_RE
               36  LOAD_METHOD              match
               38  LOAD_FAST                'url'
               40  CALL_METHOD_1         1  ''
               42  LOAD_METHOD              groups
               44  CALL_METHOD_0         0  ''
               46  UNPACK_SEQUENCE_5     5 
               48  STORE_FAST               'scheme'
               50  STORE_FAST               'authority'
               52  STORE_FAST               'path'
               54  STORE_FAST               'query'
               56  STORE_FAST               'fragment'

 L. 371        58  LOAD_FAST                'scheme'
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  JUMP_IF_TRUE_OR_POP    76  'to 76'
               66  LOAD_FAST                'scheme'
               68  LOAD_METHOD              lower
               70  CALL_METHOD_0         0  ''
               72  LOAD_GLOBAL              NORMALIZABLE_SCHEMES
               74  COMPARE_OP               in
             76_0  COME_FROM            64  '64'
               76  STORE_FAST               'normalize_uri'

 L. 373        78  LOAD_FAST                'scheme'
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 374        82  LOAD_FAST                'scheme'
               84  LOAD_METHOD              lower
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'scheme'
             90_0  COME_FROM            80  '80'

 L. 376        90  LOAD_FAST                'authority'
               92  POP_JUMP_IF_FALSE   146  'to 146'

 L. 377        94  LOAD_GLOBAL              SUBAUTHORITY_RE
               96  LOAD_METHOD              match
               98  LOAD_FAST                'authority'
              100  CALL_METHOD_1         1  ''
              102  LOAD_METHOD              groups
              104  CALL_METHOD_0         0  ''
              106  UNPACK_SEQUENCE_3     3 
              108  STORE_FAST               'auth'
              110  STORE_FAST               'host'
              112  STORE_FAST               'port'

 L. 378       114  LOAD_FAST                'auth'
              116  POP_JUMP_IF_FALSE   132  'to 132'
              118  LOAD_FAST                'normalize_uri'
              120  POP_JUMP_IF_FALSE   132  'to 132'

 L. 379       122  LOAD_GLOBAL              _encode_invalid_chars
              124  LOAD_FAST                'auth'
              126  LOAD_GLOBAL              USERINFO_CHARS
              128  CALL_FUNCTION_2       2  ''
              130  STORE_FAST               'auth'
            132_0  COME_FROM           120  '120'
            132_1  COME_FROM           116  '116'

 L. 380       132  LOAD_FAST                'port'
              134  LOAD_STR                 ''
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   156  'to 156'

 L. 381       140  LOAD_CONST               None
              142  STORE_FAST               'port'
              144  JUMP_FORWARD        156  'to 156'
            146_0  COME_FROM            92  '92'

 L. 383       146  LOAD_CONST               (None, None, None)
              148  UNPACK_SEQUENCE_3     3 
              150  STORE_FAST               'auth'
              152  STORE_FAST               'host'
              154  STORE_FAST               'port'
            156_0  COME_FROM           144  '144'
            156_1  COME_FROM           138  '138'

 L. 385       156  LOAD_FAST                'port'
              158  LOAD_CONST               None
              160  COMPARE_OP               is-not
              162  POP_JUMP_IF_FALSE   202  'to 202'

 L. 386       164  LOAD_GLOBAL              int
              166  LOAD_FAST                'port'
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'port'

 L. 387       172  LOAD_CONST               0
              174  LOAD_FAST                'port'
              176  DUP_TOP          
              178  ROT_THREE        
              180  COMPARE_OP               <=
              182  POP_JUMP_IF_FALSE   192  'to 192'
              184  LOAD_CONST               65535
              186  COMPARE_OP               <=
              188  POP_JUMP_IF_TRUE    202  'to 202'
              190  JUMP_FORWARD        194  'to 194'
            192_0  COME_FROM           182  '182'
              192  POP_TOP          
            194_0  COME_FROM           190  '190'

 L. 388       194  LOAD_GLOBAL              LocationParseError
              196  LOAD_FAST                'url'
              198  CALL_FUNCTION_1       1  ''
              200  RAISE_VARARGS_1       1  ''
            202_0  COME_FROM           188  '188'
            202_1  COME_FROM           162  '162'

 L. 390       202  LOAD_GLOBAL              _normalize_host
              204  LOAD_FAST                'host'
              206  LOAD_FAST                'scheme'
              208  CALL_FUNCTION_2       2  ''
              210  STORE_FAST               'host'

 L. 392       212  LOAD_FAST                'normalize_uri'
              214  POP_JUMP_IF_FALSE   238  'to 238'
              216  LOAD_FAST                'path'
              218  POP_JUMP_IF_FALSE   238  'to 238'

 L. 393       220  LOAD_GLOBAL              _remove_path_dot_segments
              222  LOAD_FAST                'path'
              224  CALL_FUNCTION_1       1  ''
              226  STORE_FAST               'path'

 L. 394       228  LOAD_GLOBAL              _encode_invalid_chars
              230  LOAD_FAST                'path'
              232  LOAD_GLOBAL              PATH_CHARS
              234  CALL_FUNCTION_2       2  ''
              236  STORE_FAST               'path'
            238_0  COME_FROM           218  '218'
            238_1  COME_FROM           214  '214'

 L. 395       238  LOAD_FAST                'normalize_uri'
          240_242  POP_JUMP_IF_FALSE   260  'to 260'
              244  LOAD_FAST                'query'
          246_248  POP_JUMP_IF_FALSE   260  'to 260'

 L. 396       250  LOAD_GLOBAL              _encode_invalid_chars
              252  LOAD_FAST                'query'
              254  LOAD_GLOBAL              QUERY_CHARS
              256  CALL_FUNCTION_2       2  ''
              258  STORE_FAST               'query'
            260_0  COME_FROM           246  '246'
            260_1  COME_FROM           240  '240'

 L. 397       260  LOAD_FAST                'normalize_uri'
          262_264  POP_JUMP_IF_FALSE   282  'to 282'
              266  LOAD_FAST                'fragment'
          268_270  POP_JUMP_IF_FALSE   282  'to 282'

 L. 398       272  LOAD_GLOBAL              _encode_invalid_chars
              274  LOAD_FAST                'fragment'
              276  LOAD_GLOBAL              FRAGMENT_CHARS
              278  CALL_FUNCTION_2       2  ''
              280  STORE_FAST               'fragment'
            282_0  COME_FROM           268  '268'
            282_1  COME_FROM           262  '262'
              282  POP_BLOCK        
              284  JUMP_FORWARD        328  'to 328'
            286_0  COME_FROM_FINALLY    32  '32'

 L. 400       286  DUP_TOP          
              288  LOAD_GLOBAL              ValueError
              290  LOAD_GLOBAL              AttributeError
              292  BUILD_TUPLE_2         2 
              294  COMPARE_OP               exception-match
          296_298  POP_JUMP_IF_FALSE   326  'to 326'
              300  POP_TOP          
              302  POP_TOP          
              304  POP_TOP          

 L. 401       306  LOAD_GLOBAL              six
              308  LOAD_METHOD              raise_from
              310  LOAD_GLOBAL              LocationParseError
              312  LOAD_FAST                'source_url'
              314  CALL_FUNCTION_1       1  ''
              316  LOAD_CONST               None
              318  CALL_METHOD_2         2  ''
              320  ROT_FOUR         
              322  POP_EXCEPT       
              324  RETURN_VALUE     
            326_0  COME_FROM           296  '296'
              326  END_FINALLY      
            328_0  COME_FROM           284  '284'

 L. 407       328  LOAD_FAST                'path'
          330_332  POP_JUMP_IF_TRUE    364  'to 364'

 L. 408       334  LOAD_FAST                'query'
              336  LOAD_CONST               None
              338  COMPARE_OP               is-not
          340_342  POP_JUMP_IF_TRUE    354  'to 354'
              344  LOAD_FAST                'fragment'
              346  LOAD_CONST               None
              348  COMPARE_OP               is-not
          350_352  POP_JUMP_IF_FALSE   360  'to 360'
            354_0  COME_FROM           340  '340'

 L. 409       354  LOAD_STR                 ''
              356  STORE_FAST               'path'
              358  JUMP_FORWARD        364  'to 364'
            360_0  COME_FROM           350  '350'

 L. 411       360  LOAD_CONST               None
              362  STORE_FAST               'path'
            364_0  COME_FROM           358  '358'
            364_1  COME_FROM           330  '330'

 L. 415       364  LOAD_GLOBAL              isinstance
              366  LOAD_FAST                'url'
              368  LOAD_GLOBAL              six
              370  LOAD_ATTR                text_type
              372  CALL_FUNCTION_2       2  ''
          374_376  POP_JUMP_IF_FALSE   386  'to 386'

 L. 416       378  LOAD_GLOBAL              six
              380  LOAD_ATTR                ensure_text
              382  STORE_DEREF              'ensure_func'
              384  JUMP_FORWARD        392  'to 392'
            386_0  COME_FROM           374  '374'

 L. 418       386  LOAD_GLOBAL              six
              388  LOAD_ATTR                ensure_str
              390  STORE_DEREF              'ensure_func'
            392_0  COME_FROM           384  '384'

 L. 420       392  LOAD_CLOSURE             'ensure_func'
              394  BUILD_TUPLE_1         1 
              396  LOAD_CODE                <code_object ensure_type>
              398  LOAD_STR                 'parse_url.<locals>.ensure_type'
              400  MAKE_FUNCTION_8          'closure'
              402  STORE_FAST               'ensure_type'

 L. 423       404  LOAD_GLOBAL              Url

 L. 424       406  LOAD_FAST                'ensure_type'
              408  LOAD_FAST                'scheme'
              410  CALL_FUNCTION_1       1  ''

 L. 425       412  LOAD_FAST                'ensure_type'
              414  LOAD_FAST                'auth'
              416  CALL_FUNCTION_1       1  ''

 L. 426       418  LOAD_FAST                'ensure_type'
              420  LOAD_FAST                'host'
              422  CALL_FUNCTION_1       1  ''

 L. 427       424  LOAD_FAST                'port'

 L. 428       426  LOAD_FAST                'ensure_type'
              428  LOAD_FAST                'path'
              430  CALL_FUNCTION_1       1  ''

 L. 429       432  LOAD_FAST                'ensure_type'
              434  LOAD_FAST                'query'
              436  CALL_FUNCTION_1       1  ''

 L. 430       438  LOAD_FAST                'ensure_type'
              440  LOAD_FAST                'fragment'
              442  CALL_FUNCTION_1       1  ''

 L. 423       444  LOAD_CONST               ('scheme', 'auth', 'host', 'port', 'path', 'query', 'fragment')
              446  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              448  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 320


def get_host(url):
    """
    Deprecated. Use :func:`parse_url` instead.
    """
    p = parse_url(url)
    return (
     p.scheme or , p.hostname, p.port)