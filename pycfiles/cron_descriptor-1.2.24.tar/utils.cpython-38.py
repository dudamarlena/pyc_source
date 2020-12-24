# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/requests/utils.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 30049 bytes
__doc__ = '\nrequests.utils\n~~~~~~~~~~~~~~\n\nThis module provides utility functions that are used within Requests\nthat are also useful for external consumption.\n'
import codecs, contextlib, io, os, re, socket, struct, sys, tempfile, warnings, zipfile
from .__version__ import __version__
from . import certs
from ._internal_utils import to_native_string
from .compat import parse_http_list as _parse_list_header
from .compat import quote, urlparse, bytes, str, OrderedDict, unquote, getproxies, proxy_bypass, urlunparse, basestring, integer_types, is_py3, proxy_bypass_environment, getproxies_environment, Mapping
from .cookies import cookiejar_from_dict
from .structures import CaseInsensitiveDict
from .exceptions import InvalidURL, InvalidHeader, FileModeWarning, UnrewindableBodyError
NETRC_FILES = ('.netrc', '_netrc')
DEFAULT_CA_BUNDLE_PATH = certs.where()
DEFAULT_PORTS = {'http':80, 
 'https':443}
if sys.platform == 'win32':

    def proxy_bypass_registry(host):
        try:
            if is_py3:
                import winreg
            else:
                import _winreg as winreg
        except ImportError:
            return False
        else:
            try:
                internetSettings = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings')
                proxyEnable = int(winreg.QueryValueEx(internetSettings, 'ProxyEnable')[0])
                proxyOverride = winreg.QueryValueEx(internetSettings, 'ProxyOverride')[0]
            except OSError:
                return False
            else:
                return proxyEnable and proxyOverride or 
                proxyOverride = proxyOverride.split(';')
                for test in proxyOverride:
                    if test == '<local>' and '.' not in host:
                        return True
                    return True

                return False


    def proxy_bypass(host):
        """Return True, if the host should be bypassed.

        Checks proxy settings gathered from the environment, if specified,
        or the registry.
        """
        if getproxies_environment():
            return proxy_bypass_environment(host)
        return proxy_bypass_registry(host)


def dict_to_sequence(d):
    """Returns an internal sequence dictionary update."""
    if hasattr(d, 'items'):
        d = d.items()
    return d


def super_len(o):
    total_length = None
    current_position = 0
    if hasattr(o, '__len__'):
        total_length = len(o)
    elif hasattr(o, 'len'):
        total_length = o.len
    elif hasattr(o, 'fileno'):
        try:
            fileno = o.fileno()
        except io.UnsupportedOperation:
            pass
        else:
            total_length = os.fstat(fileno).st_size
            if 'b' not in o.mode:
                warnings.warn("Requests has determined the content-length for this request using the binary size of the file: however, the file has been opened in text mode (i.e. without the 'b' flag in the mode). This may lead to an incorrect content-length. In Requests 3.0, support will be removed for files in text mode.", FileModeWarning)
    if hasattr(o, 'tell'):
        try:
            current_position = o.tell()
        except (OSError, IOError):
            if total_length is not None:
                current_position = total_length

        if hasattr(o, 'seek') and total_length is None:
            try:
                o.seek(0, 2)
                total_length = o.tell()
                o.seek(current_position or )
            except (OSError, IOError):
                total_length = 0

    if total_length is None:
        total_length = 0
    return max(0, total_length - current_position)


def get_netrc_auth--- This code section failed: ---

 L. 171       0_2  SETUP_FINALLY       264  'to 264'

 L. 172         4  LOAD_CONST               0
                6  LOAD_CONST               ('netrc', 'NetrcParseError')
                8  IMPORT_NAME              netrc
               10  IMPORT_FROM              netrc
               12  STORE_FAST               'netrc'
               14  IMPORT_FROM              NetrcParseError
               16  STORE_FAST               'NetrcParseError'
               18  POP_TOP          

 L. 174        20  LOAD_CONST               None
               22  STORE_FAST               'netrc_path'

 L. 176        24  LOAD_GLOBAL              NETRC_FILES
               26  GET_ITER         
             28_0  COME_FROM            92  '92'
               28  FOR_ITER            104  'to 104'
               30  STORE_FAST               'f'

 L. 177        32  SETUP_FINALLY        56  'to 56'

 L. 178        34  LOAD_GLOBAL              os
               36  LOAD_ATTR                path
               38  LOAD_METHOD              expanduser
               40  LOAD_STR                 '~/{}'
               42  LOAD_METHOD              format
               44  LOAD_FAST                'f'
               46  CALL_METHOD_1         1  ''
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'loc'
               52  POP_BLOCK        
               54  JUMP_FORWARD         82  'to 82'
             56_0  COME_FROM_FINALLY    32  '32'

 L. 179        56  DUP_TOP          
               58  LOAD_GLOBAL              KeyError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    80  'to 80'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 183        70  POP_EXCEPT       
               72  POP_TOP          
               74  POP_BLOCK        
               76  LOAD_CONST               None
               78  RETURN_VALUE     
             80_0  COME_FROM            62  '62'
               80  END_FINALLY      
             82_0  COME_FROM            54  '54'

 L. 185        82  LOAD_GLOBAL              os
               84  LOAD_ATTR                path
               86  LOAD_METHOD              exists
               88  LOAD_FAST                'loc'
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_FALSE    28  'to 28'

 L. 186        94  LOAD_FAST                'loc'
               96  STORE_FAST               'netrc_path'

 L. 187        98  POP_TOP          
              100  BREAK_LOOP          104  'to 104'
              102  JUMP_BACK            28  'to 28'

 L. 190       104  LOAD_FAST                'netrc_path'
              106  LOAD_CONST               None
              108  COMPARE_OP               is
              110  POP_JUMP_IF_FALSE   118  'to 118'

 L. 191       112  POP_BLOCK        
              114  LOAD_CONST               None
              116  RETURN_VALUE     
            118_0  COME_FROM           110  '110'

 L. 193       118  LOAD_GLOBAL              urlparse
              120  LOAD_FAST                'url'
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'ri'

 L. 197       126  LOAD_CONST               b':'
              128  STORE_FAST               'splitstr'

 L. 198       130  LOAD_GLOBAL              isinstance
              132  LOAD_FAST                'url'
              134  LOAD_GLOBAL              str
              136  CALL_FUNCTION_2       2  ''
              138  POP_JUMP_IF_FALSE   150  'to 150'

 L. 199       140  LOAD_FAST                'splitstr'
              142  LOAD_METHOD              decode
              144  LOAD_STR                 'ascii'
              146  CALL_METHOD_1         1  ''
              148  STORE_FAST               'splitstr'
            150_0  COME_FROM           138  '138'

 L. 200       150  LOAD_FAST                'ri'
              152  LOAD_ATTR                netloc
              154  LOAD_METHOD              split
              156  LOAD_FAST                'splitstr'
              158  CALL_METHOD_1         1  ''
              160  LOAD_CONST               0
              162  BINARY_SUBSCR    
              164  STORE_FAST               'host'

 L. 202       166  SETUP_FINALLY       226  'to 226'

 L. 203       168  LOAD_FAST                'netrc'
              170  LOAD_FAST                'netrc_path'
              172  CALL_FUNCTION_1       1  ''
              174  LOAD_METHOD              authenticators
              176  LOAD_FAST                'host'
              178  CALL_METHOD_1         1  ''
              180  STORE_FAST               '_netrc'

 L. 204       182  LOAD_FAST                '_netrc'
              184  POP_JUMP_IF_FALSE   222  'to 222'

 L. 206       186  LOAD_FAST                '_netrc'
              188  LOAD_CONST               0
              190  BINARY_SUBSCR    
              192  POP_JUMP_IF_FALSE   198  'to 198'
              194  LOAD_CONST               0
              196  JUMP_FORWARD        200  'to 200'
            198_0  COME_FROM           192  '192'
              198  LOAD_CONST               1
            200_0  COME_FROM           196  '196'
              200  STORE_FAST               'login_i'

 L. 207       202  LOAD_FAST                '_netrc'
              204  LOAD_FAST                'login_i'
              206  BINARY_SUBSCR    
              208  LOAD_FAST                '_netrc'
              210  LOAD_CONST               2
              212  BINARY_SUBSCR    
              214  BUILD_TUPLE_2         2 
              216  POP_BLOCK        
              218  POP_BLOCK        
              220  RETURN_VALUE     
            222_0  COME_FROM           184  '184'
              222  POP_BLOCK        
              224  JUMP_FORWARD        260  'to 260'
            226_0  COME_FROM_FINALLY   166  '166'

 L. 208       226  DUP_TOP          
              228  LOAD_FAST                'NetrcParseError'
              230  LOAD_GLOBAL              IOError
              232  BUILD_TUPLE_2         2 
              234  COMPARE_OP               exception-match
          236_238  POP_JUMP_IF_FALSE   258  'to 258'
              240  POP_TOP          
              242  POP_TOP          
              244  POP_TOP          

 L. 211       246  LOAD_FAST                'raise_errors'
          248_250  POP_JUMP_IF_FALSE   254  'to 254'

 L. 212       252  RAISE_VARARGS_0       0  ''
            254_0  COME_FROM           248  '248'
              254  POP_EXCEPT       
              256  JUMP_FORWARD        260  'to 260'
            258_0  COME_FROM           236  '236'
              258  END_FINALLY      
            260_0  COME_FROM           256  '256'
            260_1  COME_FROM           224  '224'
              260  POP_BLOCK        
              262  JUMP_FORWARD        290  'to 290'
            264_0  COME_FROM_FINALLY     0  '0'

 L. 215       264  DUP_TOP          
              266  LOAD_GLOBAL              ImportError
              268  LOAD_GLOBAL              AttributeError
              270  BUILD_TUPLE_2         2 
              272  COMPARE_OP               exception-match
          274_276  POP_JUMP_IF_FALSE   288  'to 288'
              278  POP_TOP          
              280  POP_TOP          
              282  POP_TOP          

 L. 216       284  POP_EXCEPT       
              286  JUMP_FORWARD        290  'to 290'
            288_0  COME_FROM           274  '274'
              288  END_FINALLY      
            290_0  COME_FROM           286  '286'
            290_1  COME_FROM           262  '262'

Parse error at or near `POP_BLOCK' instruction at offset 74


def guess_filename(obj):
    """Tries to guess the filename of the given object."""
    name = getattr(obj, 'name', None)
    if name:
        if isinstance(name, basestring):
            if name[0] != '<':
                if name[(-1)] != '>':
                    return os.path.basename(name)


def extract_zipped_paths(path):
    """Replace nonexistent paths that look like they refer to a member of a zip
    archive with the location of an extracted copy of the target, or else
    just return the provided path unchanged.
    """
    if os.path.exists(path):
        return path
    else:
        archive, member = os.path.split(path)
        while archive:
            if not os.path.exists(archive):
                archive, prefix = os.path.split(archive)
                member = '/'.join([prefix, member])

        if not zipfile.is_zipfile(archive):
            return path
        zip_file = zipfile.ZipFile(archive)
        if member not in zip_file.namelist():
            return path
        tmp = tempfile.gettempdir()
        extracted_path = (os.path.join)(tmp, *member.split('/'))
        extracted_path = os.path.exists(extracted_path) or zip_file.extract(member, path=tmp)
    return extracted_path


def from_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. Unless it can not be represented as such, return an
    OrderedDict, e.g.,

    ::

        >>> from_key_val_list([('key', 'val')])
        OrderedDict([('key', 'val')])
        >>> from_key_val_list('string')
        ValueError: cannot encode objects that are not 2-tuples
        >>> from_key_val_list({'key': 'val'})
        OrderedDict([('key', 'val')])

    :rtype: OrderedDict
    """
    if value is None:
        return
    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')
    return OrderedDict(value)


def to_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,

    ::

        >>> to_key_val_list([('key', 'val')])
        [('key', 'val')]
        >>> to_key_val_list({'key': 'val'})
        [('key', 'val')]
        >>> to_key_val_list('string')
        ValueError: cannot encode objects that are not 2-tuples.

    :rtype: list
    """
    if value is None:
        return
    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')
    if isinstance(value, Mapping):
        value = value.items()
    return list(value)


def parse_list_header(value):
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Quotes are removed automatically after parsing.

    It basically works like :func:`parse_set_header` just that items
    may appear multiple times and case sensitivity is preserved.

    The return value is a standard :class:`list`:

    >>> parse_list_header('token, "quoted value"')
    ['token', 'quoted value']

    To create a header from the :class:`list` again, use the
    :func:`dump_header` function.

    :param value: a string with a list header.
    :return: :class:`list`
    :rtype: list
    """
    result = []
    for item in _parse_list_header(value):
        if item[:1] == item[-1:] == '"':
            item = unquote_header_value(item[1:-1])
        result.append(item)

    return result


def parse_dict_header(value):
    """Parse lists of key, value pairs as described by RFC 2068 Section 2 and
    convert them into a python dict:

    >>> d = parse_dict_header('foo="is a fish", bar="as well"')
    >>> type(d) is dict
    True
    >>> sorted(d.items())
    [('bar', 'as well'), ('foo', 'is a fish')]

    If there is no value for a key it will be `None`:

    >>> parse_dict_header('key_without_value')
    {'key_without_value': None}

    To create a header from the :class:`dict` again, use the
    :func:`dump_header` function.

    :param value: a string with a dict header.
    :return: :class:`dict`
    :rtype: dict
    """
    result = {}
    for item in _parse_list_header(value):
        if '=' not in item:
            result[item] = None
        else:
            name, value = item.split('=', 1)
            if value[:1] == value[-1:] == '"':
                value = unquote_header_value(value[1:-1])
            result[name] = value

    return result


def unquote_header_value(value, is_filename=False):
    """Unquotes a header value.  (Reversal of :func:`quote_header_value`).
    This does not use the real unquoting but what browsers are actually
    using for quoting.

    :param value: the header value to unquote.
    :rtype: str
    """
    if value:
        if value[0] == value[(-1)] == '"':
            value = value[1:-1]
            if is_filename:
                if value[:2] != '\\\\':
                    return value.replace('\\\\', '\\').replace('\\"', '"')
    return value


def dict_from_cookiejar(cj):
    """Returns a key/value dictionary from a CookieJar.

    :param cj: CookieJar object to extract cookies from.
    :rtype: dict
    """
    cookie_dict = {}
    for cookie in cj:
        cookie_dict[cookie.name] = cookie.value

    return cookie_dict


def add_dict_to_cookiejar(cj, cookie_dict):
    """Returns a CookieJar from a key/value dictionary.

    :param cj: CookieJar to insert cookies into.
    :param cookie_dict: Dict of key/values to insert into CookieJar.
    :rtype: CookieJar
    """
    return cookiejar_from_dict(cookie_dict, cj)


def get_encodings_from_content(content):
    """Returns encodings from given content string.

    :param content: bytestring to extract encodings from.
    """
    warnings.warn('In requests 3.0, get_encodings_from_content will be removed. For more information, please see the discussion on issue #2266. (This warning should only appear once.)', DeprecationWarning)
    charset_re = re.compile('<meta.*?charset=["\\\']*(.+?)["\\\'>]', flags=(re.I))
    pragma_re = re.compile('<meta.*?content=["\\\']*;?charset=(.+?)["\\\'>]', flags=(re.I))
    xml_re = re.compile('^<\\?xml.*?encoding=["\\\']*(.+?)["\\\'>]')
    return charset_re.findall(content) + pragma_re.findall(content) + xml_re.findall(content)


def _parse_content_type_header(header):
    """Returns content type and parameters from given header

    :param header: string
    :return: tuple containing content type and dictionary of
         parameters
    """
    tokens = header.split(';')
    content_type, params = tokens[0].strip(), tokens[1:]
    params_dict = {}
    items_to_strip = '"\' '
    for param in params:
        param = param.strip()
        if param:
            key, value = param, True
            index_of_equals = param.find('=')
            if index_of_equals != -1:
                key = param[:index_of_equals].strip(items_to_strip)
                value = param[index_of_equals + 1:].strip(items_to_strip)
            params_dict[key.lower()] = value
        return (content_type, params_dict)


def get_encoding_from_headers(headers):
    """Returns encodings from given HTTP Header Dict.

    :param headers: dictionary to extract encoding from.
    :rtype: str
    """
    content_type = headers.get('content-type')
    if not content_type:
        return
    content_type, params = _parse_content_type_header(content_type)
    if 'charset' in params:
        return params['charset'].strip('\'"')
    if 'text' in content_type:
        return 'ISO-8859-1'


def stream_decode_response_unicode(iterator, r):
    """Stream decodes a iterator."""
    if r.encoding is None:
        for item in iterator:
            yield item

        return
    decoder = codecs.getincrementaldecoder(r.encoding)(errors='replace')
    for chunk in iterator:
        rv = decoder.decode(chunk)
        if rv:
            yield rv
        rv = decoder.decode(b'', final=True)
        if rv:
            yield rv


def iter_slices(string, slice_length):
    """Iterate over slices of a string."""
    pos = 0
    if slice_length is None or slice_length <= 0:
        slice_length = len(string)
    else:
        while True:
            if pos < len(string):
                yield string[pos:pos + slice_length]
                pos += slice_length


def get_unicode_from_response--- This code section failed: ---

 L. 536         0  LOAD_GLOBAL              warnings
                2  LOAD_METHOD              warn

 L. 537         4  LOAD_STR                 'In requests 3.0, get_unicode_from_response will be removed. For more information, please see the discussion on issue #2266. (This warning should only appear once.)'

 L. 540         6  LOAD_GLOBAL              DeprecationWarning

 L. 536         8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 542        12  BUILD_LIST_0          0 
               14  STORE_FAST               'tried_encodings'

 L. 545        16  LOAD_GLOBAL              get_encoding_from_headers
               18  LOAD_FAST                'r'
               20  LOAD_ATTR                headers
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'encoding'

 L. 547        26  LOAD_FAST                'encoding'
               28  POP_JUMP_IF_FALSE    76  'to 76'

 L. 548        30  SETUP_FINALLY        46  'to 46'

 L. 549        32  LOAD_GLOBAL              str
               34  LOAD_FAST                'r'
               36  LOAD_ATTR                content
               38  LOAD_FAST                'encoding'
               40  CALL_FUNCTION_2       2  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY    30  '30'

 L. 550        46  DUP_TOP          
               48  LOAD_GLOBAL              UnicodeError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    74  'to 74'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 551        60  LOAD_FAST                'tried_encodings'
               62  LOAD_METHOD              append
               64  LOAD_FAST                'encoding'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            52  '52'
               74  END_FINALLY      
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            28  '28'

 L. 554        76  SETUP_FINALLY        96  'to 96'

 L. 555        78  LOAD_GLOBAL              str
               80  LOAD_FAST                'r'
               82  LOAD_ATTR                content
               84  LOAD_FAST                'encoding'
               86  LOAD_STR                 'replace'
               88  LOAD_CONST               ('errors',)
               90  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               92  POP_BLOCK        
               94  RETURN_VALUE     
             96_0  COME_FROM_FINALLY    76  '76'

 L. 556        96  DUP_TOP          
               98  LOAD_GLOBAL              TypeError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   120  'to 120'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 557       110  LOAD_FAST                'r'
              112  LOAD_ATTR                content
              114  ROT_FOUR         
              116  POP_EXCEPT       
              118  RETURN_VALUE     
            120_0  COME_FROM           102  '102'
              120  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 46


UNRESERVED_SET = frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~')

def unquote_unreserved(uri):
    """Un-escape any percent-escape sequences in a URI that are unreserved
    characters. This leaves all reserved, illegal and non-ASCII bytes encoded.

    :rtype: str
    """
    parts = uri.split('%')
    for i in range(1, len(parts)):
        h = parts[i][0:2]
        if len(h) == 2:
            if h.isalnum():
                try:
                    c = chr(int(h, 16))
                except ValueError:
                    raise InvalidURL("Invalid percent-escape sequence: '%s'" % h)
                else:
                    if c in UNRESERVED_SET:
                        parts[i] = c + parts[i][2:]
            else:
                parts[i] = '%' + parts[i]
        else:
            parts[i] = '%' + parts[i]

    return ''.join(parts)


def requote_uri--- This code section failed: ---

 L. 597         0  LOAD_STR                 "!#$%&'()*+,/:;=?@[]~"
                2  STORE_FAST               'safe_with_percent'

 L. 598         4  LOAD_STR                 "!#$&'()*+,/:;=?@[]~"
                6  STORE_FAST               'safe_without_percent'

 L. 599         8  SETUP_FINALLY        28  'to 28'

 L. 603        10  LOAD_GLOBAL              quote
               12  LOAD_GLOBAL              unquote_unreserved
               14  LOAD_FAST                'uri'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'safe_with_percent'
               20  LOAD_CONST               ('safe',)
               22  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY     8  '8'

 L. 604        28  DUP_TOP          
               30  LOAD_GLOBAL              InvalidURL
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    58  'to 58'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 608        42  LOAD_GLOBAL              quote
               44  LOAD_FAST                'uri'
               46  LOAD_FAST                'safe_without_percent'
               48  LOAD_CONST               ('safe',)
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  ROT_FOUR         
               54  POP_EXCEPT       
               56  RETURN_VALUE     
             58_0  COME_FROM            34  '34'
               58  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 28


def address_in_network(ip, net):
    """This function allows you to check if an IP belongs to a network subnet

    Example: returns True if ip = 192.168.1.1 and net = 192.168.1.0/24
             returns False if ip = 192.168.1.1 and net = 192.168.100.0/24

    :rtype: bool
    """
    ipaddr = struct.unpack('=L', socket.inet_aton(ip))[0]
    netaddr, bits = net.split('/')
    netmask = struct.unpack('=L', socket.inet_aton(dotted_netmask(int(bits))))[0]
    network = struct.unpack('=L', socket.inet_aton(netaddr))[0] & netmask
    return ipaddr & netmask == network & netmask


def dotted_netmask(mask):
    """Converts mask from /xx format to xxx.xxx.xxx.xxx

    Example: if mask is 24 function returns 255.255.255.0

    :rtype: str
    """
    bits = 4294967295 ^ (1 << 32 - mask) - 1
    return socket.inet_ntoa(struct.pack('>I', bits))


def is_ipv4_address(string_ip):
    """
    :rtype: bool
    """
    try:
        socket.inet_aton(string_ip)
    except socket.error:
        return False
    else:
        return True


def is_valid_cidr(string_network):
    """
    Very simple check of the cidr format in no_proxy variable.

    :rtype: bool
    """
    if string_network.count('/') == 1:
        try:
            mask = int(string_network.split('/')[1])
        except ValueError:
            return False
        else:
            if mask < 1 or mask > 32:
                return False
            try:
                socket.inet_aton(string_network.split('/')[0])
            except socket.error:
                return False

    else:
        return False
    return True


@contextlib.contextmanager
def set_environ(env_name, value):
    """Set the environment variable 'env_name' to 'value'

    Save previous value, yield, and then restore the previous value stored in
    the environment variable 'env_name'.

    If 'value' is None, do nothing"""
    value_changed = value is not None
    if value_changed:
        old_value = os.environ.get(env_name)
        os.environ[env_name] = value
    try:
        yield
    finally:
        if value_changed:
            if old_value is None:
                del os.environ[env_name]
            else:
                os.environ[env_name] = old_value


def should_bypass_proxies--- This code section failed: ---

 L. 702         0  LOAD_LAMBDA              '<code_object <lambda>>'
                2  LOAD_STR                 'should_bypass_proxies.<locals>.<lambda>'
                4  MAKE_FUNCTION_0          ''
                6  STORE_FAST               'get_proxy'

 L. 706         8  LOAD_FAST                'no_proxy'
               10  STORE_FAST               'no_proxy_arg'

 L. 707        12  LOAD_FAST                'no_proxy'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 708        20  LOAD_FAST                'get_proxy'
               22  LOAD_STR                 'no_proxy'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'no_proxy'
             28_0  COME_FROM            18  '18'

 L. 709        28  LOAD_GLOBAL              urlparse
               30  LOAD_FAST                'url'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'parsed'

 L. 711        36  LOAD_FAST                'parsed'
               38  LOAD_ATTR                hostname
               40  LOAD_CONST               None
               42  COMPARE_OP               is
               44  POP_JUMP_IF_FALSE    50  'to 50'

 L. 713        46  LOAD_CONST               True
               48  RETURN_VALUE     
             50_0  COME_FROM            44  '44'

 L. 715        50  LOAD_FAST                'no_proxy'
               52  POP_JUMP_IF_FALSE   214  'to 214'

 L. 718        54  LOAD_GENEXPR             '<code_object <genexpr>>'
               56  LOAD_STR                 'should_bypass_proxies.<locals>.<genexpr>'
               58  MAKE_FUNCTION_0          ''

 L. 719        60  LOAD_FAST                'no_proxy'
               62  LOAD_METHOD              replace
               64  LOAD_STR                 ' '
               66  LOAD_STR                 ''
               68  CALL_METHOD_2         2  ''
               70  LOAD_METHOD              split
               72  LOAD_STR                 ','
               74  CALL_METHOD_1         1  ''

 L. 718        76  GET_ITER         
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'no_proxy'

 L. 722        82  LOAD_GLOBAL              is_ipv4_address
               84  LOAD_FAST                'parsed'
               86  LOAD_ATTR                hostname
               88  CALL_FUNCTION_1       1  ''
               90  POP_JUMP_IF_FALSE   148  'to 148'

 L. 723        92  LOAD_FAST                'no_proxy'
               94  GET_ITER         
             96_0  COME_FROM           136  '136'
               96  FOR_ITER            146  'to 146'
               98  STORE_FAST               'proxy_ip'

 L. 724       100  LOAD_GLOBAL              is_valid_cidr
              102  LOAD_FAST                'proxy_ip'
              104  CALL_FUNCTION_1       1  ''
              106  POP_JUMP_IF_FALSE   128  'to 128'

 L. 725       108  LOAD_GLOBAL              address_in_network
              110  LOAD_FAST                'parsed'
              112  LOAD_ATTR                hostname
              114  LOAD_FAST                'proxy_ip'
              116  CALL_FUNCTION_2       2  ''
              118  POP_JUMP_IF_FALSE   144  'to 144'

 L. 726       120  POP_TOP          
              122  LOAD_CONST               True
              124  RETURN_VALUE     
              126  JUMP_BACK            96  'to 96'
            128_0  COME_FROM           106  '106'

 L. 727       128  LOAD_FAST                'parsed'
              130  LOAD_ATTR                hostname
              132  LOAD_FAST                'proxy_ip'
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE    96  'to 96'

 L. 730       138  POP_TOP          
              140  LOAD_CONST               True
              142  RETURN_VALUE     
            144_0  COME_FROM           118  '118'
              144  JUMP_BACK            96  'to 96'
              146  JUMP_FORWARD        214  'to 214'
            148_0  COME_FROM            90  '90'

 L. 732       148  LOAD_FAST                'parsed'
              150  LOAD_ATTR                hostname
              152  STORE_FAST               'host_with_port'

 L. 733       154  LOAD_FAST                'parsed'
              156  LOAD_ATTR                port
              158  POP_JUMP_IF_FALSE   176  'to 176'

 L. 734       160  LOAD_FAST                'host_with_port'
              162  LOAD_STR                 ':{}'
              164  LOAD_METHOD              format
              166  LOAD_FAST                'parsed'
              168  LOAD_ATTR                port
              170  CALL_METHOD_1         1  ''
              172  INPLACE_ADD      
              174  STORE_FAST               'host_with_port'
            176_0  COME_FROM           158  '158'

 L. 736       176  LOAD_FAST                'no_proxy'
              178  GET_ITER         
            180_0  COME_FROM           204  '204'
              180  FOR_ITER            214  'to 214'
              182  STORE_FAST               'host'

 L. 737       184  LOAD_FAST                'parsed'
              186  LOAD_ATTR                hostname
              188  LOAD_METHOD              endswith
              190  LOAD_FAST                'host'
              192  CALL_METHOD_1         1  ''
              194  POP_JUMP_IF_TRUE    206  'to 206'
              196  LOAD_FAST                'host_with_port'
              198  LOAD_METHOD              endswith
              200  LOAD_FAST                'host'
              202  CALL_METHOD_1         1  ''
              204  POP_JUMP_IF_FALSE   180  'to 180'
            206_0  COME_FROM           194  '194'

 L. 740       206  POP_TOP          
              208  LOAD_CONST               True
              210  RETURN_VALUE     
              212  JUMP_BACK           180  'to 180'
            214_0  COME_FROM           146  '146'
            214_1  COME_FROM            52  '52'

 L. 742       214  LOAD_GLOBAL              set_environ
              216  LOAD_STR                 'no_proxy'
              218  LOAD_FAST                'no_proxy_arg'
              220  CALL_FUNCTION_2       2  ''
              222  SETUP_WITH          278  'to 278'
              224  POP_TOP          

 L. 744       226  SETUP_FINALLY       242  'to 242'

 L. 745       228  LOAD_GLOBAL              proxy_bypass
              230  LOAD_FAST                'parsed'
              232  LOAD_ATTR                hostname
              234  CALL_FUNCTION_1       1  ''
              236  STORE_FAST               'bypass'
              238  POP_BLOCK        
              240  JUMP_FORWARD        274  'to 274'
            242_0  COME_FROM_FINALLY   226  '226'

 L. 746       242  DUP_TOP          
              244  LOAD_GLOBAL              TypeError
              246  LOAD_GLOBAL              socket
              248  LOAD_ATTR                gaierror
              250  BUILD_TUPLE_2         2 
              252  COMPARE_OP               exception-match
          254_256  POP_JUMP_IF_FALSE   272  'to 272'
              258  POP_TOP          
              260  POP_TOP          
              262  POP_TOP          

 L. 747       264  LOAD_CONST               False
              266  STORE_FAST               'bypass'
              268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
            272_0  COME_FROM           254  '254'
              272  END_FINALLY      
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           240  '240'
              274  POP_BLOCK        
              276  BEGIN_FINALLY    
            278_0  COME_FROM_WITH      222  '222'
              278  WITH_CLEANUP_START
              280  WITH_CLEANUP_FINISH
              282  END_FINALLY      

 L. 749       284  LOAD_FAST                'bypass'
          286_288  POP_JUMP_IF_FALSE   294  'to 294'

 L. 750       290  LOAD_CONST               True
              292  RETURN_VALUE     
            294_0  COME_FROM           286  '286'

 L. 752       294  LOAD_CONST               False
              296  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 128


def get_environ_proxies(url, no_proxy=None):
    """
    Return a dict of environment proxies.

    :rtype: dict
    """
    if should_bypass_proxies(url, no_proxy=no_proxy):
        return {}
    return getproxies()


def select_proxy(url, proxies):
    """Select a proxy for the url, if applicable.

    :param url: The url being for the request
    :param proxies: A dictionary of schemes or schemes and hosts to proxy URLs
    """
    proxies = proxies or 
    urlparts = urlparse(url)
    if urlparts.hostname is None:
        return proxies.get(urlparts.scheme, proxies.get('all'))
    proxy_keys = [
     urlparts.scheme + '://' + urlparts.hostname,
     urlparts.scheme,
     'all://' + urlparts.hostname,
     'all']
    proxy = None
    for proxy_key in proxy_keys:
        if proxy_key in proxies:
            proxy = proxies[proxy_key]
            break
        return proxy


def default_user_agent(name='python-requests'):
    """
    Return a string representing the default user agent.

    :rtype: str
    """
    return '%s/%s' % (name, __version__)


def default_headers():
    """
    :rtype: requests.structures.CaseInsensitiveDict
    """
    return CaseInsensitiveDict({'User-Agent':default_user_agent(), 
     'Accept-Encoding':', '.join(('gzip', 'deflate')), 
     'Accept':'*/*', 
     'Connection':'keep-alive'})


def parse_header_links(value):
    """Return a list of parsed link headers proxies.

    i.e. Link: <http:/.../front.jpeg>; rel=front; type="image/jpeg",<http://.../back.jpeg>; rel=back;type="image/jpeg"

    :rtype: list
    """
    links = []
    replace_chars = ' \'"'
    value = value.strip(replace_chars)
    if not value:
        return links
    for val in re.split(', *<', value):
        try:
            url, params = val.split(';', 1)
        except ValueError:
            url, params = val, ''
        else:
            link = {'url': url.strip('<> \'"')}
            for param in params.split(';'):
                try:
                    key, value = param.split('=')
                except ValueError:
                    break
                else:
                    link[key.strip(replace_chars)] = value.strip(replace_chars)

            links.append(link)

    return links


_null = '\x00'.encode('ascii')
_null2 = _null * 2
_null3 = _null * 3

def guess_json_utf(data):
    """
    :rtype: str
    """
    sample = data[:4]
    if sample in (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE):
        return 'utf-32'
    if sample[:3] == codecs.BOM_UTF8:
        return 'utf-8-sig'
    if sample[:2] in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE):
        return 'utf-16'
    nullcount = sample.count(_null)
    if nullcount == 0:
        return 'utf-8'
    if nullcount == 2:
        if sample[::2] == _null2:
            return 'utf-16-be'
        if sample[1::2] == _null2:
            return 'utf-16-le'
    if nullcount == 3:
        if sample[:3] == _null3:
            return 'utf-32-be'
        if sample[1:] == _null3:
            return 'utf-32-le'


def prepend_scheme_if_needed(url, new_scheme):
    """Given a URL that may or may not have a scheme, prepend the given scheme.
    Does not replace a present scheme with the one provided as an argument.

    :rtype: str
    """
    scheme, netloc, path, params, query, fragment = urlparse(url, new_scheme)
    if not netloc:
        netloc, path = path, netloc
    return urlunparse((scheme, netloc, path, params, query, fragment))


def get_auth_from_url(url):
    """Given a url with authentication components, extract them into a tuple of
    username,password.

    :rtype: (str,str)
    """
    parsed = urlparse(url)
    try:
        auth = (unquote(parsed.username), unquote(parsed.password))
    except (AttributeError, TypeError):
        auth = ('', '')
    else:
        return auth


_CLEAN_HEADER_REGEX_BYTE = re.compile(b'^\\S[^\\r\\n]*$|^$')
_CLEAN_HEADER_REGEX_STR = re.compile('^\\S[^\\r\\n]*$|^$')

def check_header_validity(header):
    """Verifies that header value is a string which doesn't contain
    leading whitespace or return characters. This prevents unintended
    header injection.

    :param header: tuple, in the format (name, value).
    """
    name, value = header
    if isinstance(value, bytes):
        pat = _CLEAN_HEADER_REGEX_BYTE
    else:
        pat = _CLEAN_HEADER_REGEX_STR
    try:
        if not pat.match(value):
            raise InvalidHeader('Invalid return character or leading space in header: %s' % name)
    except TypeError:
        raise InvalidHeader('Value for header {%s: %s} must be of type str or bytes, not %s' % (
         name, value, type(value)))


def urldefragauth(url):
    """
    Given a url remove the fragment and the authentication part.

    :rtype: str
    """
    scheme, netloc, path, params, query, fragment = urlparse(url)
    if not netloc:
        netloc, path = path, netloc
    netloc = netloc.rsplit('@', 1)[(-1)]
    return urlunparse((scheme, netloc, path, params, query, ''))


def rewind_body(prepared_request):
    """Move file pointer back to its recorded starting position
    so it can be read again on redirect.
    """
    body_seek = getattr(prepared_request.body, 'seek', None)
    if body_seek is not None and isinstance(prepared_request._body_position, integer_types):
        try:
            body_seek(prepared_request._body_position)
        except (IOError, OSError):
            raise UnrewindableBodyError('An error occurred when rewinding request body for redirect.')

    else:
        raise UnrewindableBodyError('Unable to rewind request body for redirect.')