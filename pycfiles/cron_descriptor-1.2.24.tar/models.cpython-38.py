# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/requests/models.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 34210 bytes
__doc__ = '\nrequests.models\n~~~~~~~~~~~~~~~\n\nThis module contains the primary objects that power Requests.\n'
import datetime, sys, encodings.idna
from urllib3.fields import RequestField
from urllib3.filepost import encode_multipart_formdata
from urllib3.util import parse_url
from urllib3.exceptions import DecodeError, ReadTimeoutError, ProtocolError, LocationParseError
from io import UnsupportedOperation
from .hooks import default_hooks
from .structures import CaseInsensitiveDict
from .auth import HTTPBasicAuth
from .cookies import cookiejar_from_dict, get_cookie_header, _copy_cookie_jar
from .exceptions import HTTPError, MissingSchema, InvalidURL, ChunkedEncodingError, ContentDecodingError, ConnectionError, StreamConsumedError
from ._internal_utils import to_native_string, unicode_is_ascii
from .utils import guess_filename, get_auth_from_url, requote_uri, stream_decode_response_unicode, to_key_val_list, parse_header_links, iter_slices, guess_json_utf, super_len, check_header_validity
from .compat import Callable, Mapping, cookielib, urlunparse, urlsplit, urlencode, str, bytes, is_py2, chardet, builtin_str, basestring
from .compat import json as complexjson
from .status_codes import codes
REDIRECT_STATI = (
 codes.moved,
 codes.found,
 codes.other,
 codes.temporary_redirect,
 codes.permanent_redirect)
DEFAULT_REDIRECT_LIMIT = 30
CONTENT_CHUNK_SIZE = 10240
ITER_CHUNK_SIZE = 512

class RequestEncodingMixin(object):

    @property
    def path_url(self):
        """Build the path URL to use."""
        url = []
        p = urlsplit(self.url)
        path = p.path
        if not path:
            path = '/'
        url.append(path)
        query = p.query
        if query:
            url.append('?')
            url.append(query)
        return ''.join(url)

    @staticmethod
    def _encode_params(data):
        """Encode parameters in a piece of data.

        Will successfully encode parameters when passed as a dict or a list of
        2-tuples. Order is retained if data is a list of 2-tuples but arbitrary
        if parameters are supplied as a dict.
        """
        if isinstance(data, (str, bytes)):
            return data
        if hasattr(data, 'read'):
            return data
        if hasattr(data, '__iter__'):
            result = []
            for k, vs in to_key_val_list(data):
                if not (isinstance(vs, basestring) or hasattr(vs, '__iter__')):
                    vs = [
                     vs]
                for v in vs:
                    if v is not None:
                        result.append((
                         k.encode('utf-8') if isinstance(k, str) else k,
                         v.encode('utf-8') if isinstance(v, str) else v))

                return urlencode(result, doseq=True)

        return data

    @staticmethod
    def _encode_files--- This code section failed: ---

 L. 119         0  LOAD_FAST                'files'
                2  POP_JUMP_IF_TRUE     14  'to 14'

 L. 120         4  LOAD_GLOBAL              ValueError
                6  LOAD_STR                 'Files must be provided.'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  ''
               12  JUMP_FORWARD         32  'to 32'
             14_0  COME_FROM             2  '2'

 L. 121        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'data'
               18  LOAD_GLOBAL              basestring
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 122        24  LOAD_GLOBAL              ValueError
               26  LOAD_STR                 'Data must not be a string.'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  ''
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            12  '12'

 L. 124        32  BUILD_LIST_0          0 
               34  STORE_FAST               'new_fields'

 L. 125        36  LOAD_GLOBAL              to_key_val_list
               38  LOAD_FAST                'data'
               40  JUMP_IF_TRUE_OR_POP    44  'to 44'
               42  BUILD_MAP_0           0 
             44_0  COME_FROM            40  '40'
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'fields'

 L. 126        48  LOAD_GLOBAL              to_key_val_list
               50  LOAD_FAST                'files'
               52  JUMP_IF_TRUE_OR_POP    56  'to 56'
               54  BUILD_MAP_0           0 
             56_0  COME_FROM            52  '52'
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'files'

 L. 128        60  LOAD_FAST                'fields'
               62  GET_ITER         
               64  FOR_ITER            190  'to 190'
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'field'
               70  STORE_FAST               'val'

 L. 129        72  LOAD_GLOBAL              isinstance
               74  LOAD_FAST                'val'
               76  LOAD_GLOBAL              basestring
               78  CALL_FUNCTION_2       2  ''
               80  POP_JUMP_IF_TRUE     92  'to 92'
               82  LOAD_GLOBAL              hasattr
               84  LOAD_FAST                'val'
               86  LOAD_STR                 '__iter__'
               88  CALL_FUNCTION_2       2  ''
               90  POP_JUMP_IF_TRUE     98  'to 98'
             92_0  COME_FROM            80  '80'

 L. 130        92  LOAD_FAST                'val'
               94  BUILD_LIST_1          1 
               96  STORE_FAST               'val'
             98_0  COME_FROM            90  '90'

 L. 131        98  LOAD_FAST                'val'
              100  GET_ITER         
            102_0  COME_FROM           112  '112'
              102  FOR_ITER            188  'to 188'
              104  STORE_FAST               'v'

 L. 132       106  LOAD_FAST                'v'
              108  LOAD_CONST               None
              110  COMPARE_OP               is-not
              112  POP_JUMP_IF_FALSE   102  'to 102'

 L. 134       114  LOAD_GLOBAL              isinstance
              116  LOAD_FAST                'v'
              118  LOAD_GLOBAL              bytes
              120  CALL_FUNCTION_2       2  ''
              122  POP_JUMP_IF_TRUE    132  'to 132'

 L. 135       124  LOAD_GLOBAL              str
              126  LOAD_FAST                'v'
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'v'
            132_0  COME_FROM           122  '122'

 L. 137       132  LOAD_FAST                'new_fields'
              134  LOAD_METHOD              append

 L. 138       136  LOAD_GLOBAL              isinstance
              138  LOAD_FAST                'field'
              140  LOAD_GLOBAL              bytes
              142  CALL_FUNCTION_2       2  ''
              144  POP_JUMP_IF_FALSE   156  'to 156'
              146  LOAD_FAST                'field'
              148  LOAD_METHOD              decode
              150  LOAD_STR                 'utf-8'
              152  CALL_METHOD_1         1  ''
              154  JUMP_FORWARD        158  'to 158'
            156_0  COME_FROM           144  '144'
              156  LOAD_FAST                'field'
            158_0  COME_FROM           154  '154'

 L. 139       158  LOAD_GLOBAL              isinstance
              160  LOAD_FAST                'v'
              162  LOAD_GLOBAL              str
              164  CALL_FUNCTION_2       2  ''
              166  POP_JUMP_IF_FALSE   178  'to 178'
              168  LOAD_FAST                'v'
              170  LOAD_METHOD              encode
              172  LOAD_STR                 'utf-8'
              174  CALL_METHOD_1         1  ''
              176  JUMP_FORWARD        180  'to 180'
            178_0  COME_FROM           166  '166'
              178  LOAD_FAST                'v'
            180_0  COME_FROM           176  '176'

 L. 138       180  BUILD_TUPLE_2         2 

 L. 137       182  CALL_METHOD_1         1  ''
              184  POP_TOP          
              186  JUMP_BACK           102  'to 102'
              188  JUMP_BACK            64  'to 64'

 L. 141       190  LOAD_FAST                'files'
              192  GET_ITER         
              194  FOR_ITER            410  'to 410'
              196  UNPACK_SEQUENCE_2     2 
              198  STORE_FAST               'k'
              200  STORE_FAST               'v'

 L. 143       202  LOAD_CONST               None
              204  STORE_FAST               'ft'

 L. 144       206  LOAD_CONST               None
              208  STORE_FAST               'fh'

 L. 145       210  LOAD_GLOBAL              isinstance
              212  LOAD_FAST                'v'
              214  LOAD_GLOBAL              tuple
              216  LOAD_GLOBAL              list
              218  BUILD_TUPLE_2         2 
              220  CALL_FUNCTION_2       2  ''
          222_224  POP_JUMP_IF_FALSE   288  'to 288'

 L. 146       226  LOAD_GLOBAL              len
              228  LOAD_FAST                'v'
              230  CALL_FUNCTION_1       1  ''
              232  LOAD_CONST               2
              234  COMPARE_OP               ==
              236  POP_JUMP_IF_FALSE   248  'to 248'

 L. 147       238  LOAD_FAST                'v'
              240  UNPACK_SEQUENCE_2     2 
              242  STORE_FAST               'fn'
              244  STORE_FAST               'fp'
              246  JUMP_FORWARD        286  'to 286'
            248_0  COME_FROM           236  '236'

 L. 148       248  LOAD_GLOBAL              len
              250  LOAD_FAST                'v'
              252  CALL_FUNCTION_1       1  ''
              254  LOAD_CONST               3
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   274  'to 274'

 L. 149       262  LOAD_FAST                'v'
              264  UNPACK_SEQUENCE_3     3 
              266  STORE_FAST               'fn'
              268  STORE_FAST               'fp'
              270  STORE_FAST               'ft'
              272  JUMP_FORWARD        286  'to 286'
            274_0  COME_FROM           258  '258'

 L. 151       274  LOAD_FAST                'v'
              276  UNPACK_SEQUENCE_4     4 
              278  STORE_FAST               'fn'
              280  STORE_FAST               'fp'
              282  STORE_FAST               'ft'
              284  STORE_FAST               'fh'
            286_0  COME_FROM           272  '272'
            286_1  COME_FROM           246  '246'
              286  JUMP_FORWARD        306  'to 306'
            288_0  COME_FROM           222  '222'

 L. 153       288  LOAD_GLOBAL              guess_filename
              290  LOAD_FAST                'v'
              292  CALL_FUNCTION_1       1  ''
          294_296  JUMP_IF_TRUE_OR_POP   300  'to 300'
              298  LOAD_FAST                'k'
            300_0  COME_FROM           294  '294'
              300  STORE_FAST               'fn'

 L. 154       302  LOAD_FAST                'v'
              304  STORE_FAST               'fp'
            306_0  COME_FROM           286  '286'

 L. 156       306  LOAD_GLOBAL              isinstance
              308  LOAD_FAST                'fp'
              310  LOAD_GLOBAL              str
              312  LOAD_GLOBAL              bytes
              314  LOAD_GLOBAL              bytearray
              316  BUILD_TUPLE_3         3 
              318  CALL_FUNCTION_2       2  ''
          320_322  POP_JUMP_IF_FALSE   330  'to 330'

 L. 157       324  LOAD_FAST                'fp'
              326  STORE_FAST               'fdata'
              328  JUMP_FORWARD        370  'to 370'
            330_0  COME_FROM           320  '320'

 L. 158       330  LOAD_GLOBAL              hasattr
              332  LOAD_FAST                'fp'
              334  LOAD_STR                 'read'
              336  CALL_FUNCTION_2       2  ''
          338_340  POP_JUMP_IF_FALSE   352  'to 352'

 L. 159       342  LOAD_FAST                'fp'
              344  LOAD_METHOD              read
              346  CALL_METHOD_0         0  ''
              348  STORE_FAST               'fdata'
              350  JUMP_FORWARD        370  'to 370'
            352_0  COME_FROM           338  '338'

 L. 160       352  LOAD_FAST                'fp'
              354  LOAD_CONST               None
              356  COMPARE_OP               is
          358_360  POP_JUMP_IF_FALSE   366  'to 366'

 L. 161       362  JUMP_BACK           194  'to 194'
              364  JUMP_FORWARD        370  'to 370'
            366_0  COME_FROM           358  '358'

 L. 163       366  LOAD_FAST                'fp'
              368  STORE_FAST               'fdata'
            370_0  COME_FROM           364  '364'
            370_1  COME_FROM           350  '350'
            370_2  COME_FROM           328  '328'

 L. 165       370  LOAD_GLOBAL              RequestField
              372  LOAD_FAST                'k'
              374  LOAD_FAST                'fdata'
              376  LOAD_FAST                'fn'
              378  LOAD_FAST                'fh'
              380  LOAD_CONST               ('name', 'data', 'filename', 'headers')
              382  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              384  STORE_FAST               'rf'

 L. 166       386  LOAD_FAST                'rf'
              388  LOAD_ATTR                make_multipart
              390  LOAD_FAST                'ft'
              392  LOAD_CONST               ('content_type',)
              394  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              396  POP_TOP          

 L. 167       398  LOAD_FAST                'new_fields'
              400  LOAD_METHOD              append
              402  LOAD_FAST                'rf'
              404  CALL_METHOD_1         1  ''
              406  POP_TOP          
              408  JUMP_BACK           194  'to 194'

 L. 169       410  LOAD_GLOBAL              encode_multipart_formdata
              412  LOAD_FAST                'new_fields'
              414  CALL_FUNCTION_1       1  ''
              416  UNPACK_SEQUENCE_2     2 
              418  STORE_FAST               'body'
              420  STORE_FAST               'content_type'

 L. 171       422  LOAD_FAST                'body'
              424  LOAD_FAST                'content_type'
              426  BUILD_TUPLE_2         2 
              428  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 364


class RequestHooksMixin(object):

    def register_hook(self, event, hook):
        """Properly register a hook."""
        if event not in self.hooks:
            raise ValueError('Unsupported event specified, with event name "%s"' % event)
        elif isinstance(hook, Callable):
            self.hooks[event].append(hook)
        elif hasattr(hook, '__iter__'):
            self.hooks[event].extend((h for h in hook if isinstance(h, Callable)))

    def deregister_hook--- This code section failed: ---

 L. 191         0  SETUP_FINALLY        24  'to 24'

 L. 192         2  LOAD_FAST                'self'
                4  LOAD_ATTR                hooks
                6  LOAD_FAST                'event'
                8  BINARY_SUBSCR    
               10  LOAD_METHOD              remove
               12  LOAD_FAST                'hook'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L. 193        18  POP_BLOCK        
               20  LOAD_CONST               True
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L. 194        24  DUP_TOP          
               26  LOAD_GLOBAL              ValueError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 195        38  POP_EXCEPT       
               40  LOAD_CONST               False
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'
               44  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 22


class Request(RequestHooksMixin):
    """Request"""

    def __init__(self, method=None, url=None, headers=None, files=None, data=None, params=None, auth=None, cookies=None, hooks=None, json=None):
        data = [] if data is None else data
        files = [] if files is None else files
        headers = {} if headers is None else headers
        params = {} if params is None else params
        hooks = {} if hooks is None else hooks
        self.hooks = default_hooks()
        for k, v in list(hooks.items):
            self.register_hook(event=k, hook=v)

        self.method = method
        self.url = url
        self.headers = headers
        self.files = files
        self.data = data
        self.json = json
        self.params = params
        self.auth = auth
        self.cookies = cookies

    def __repr__(self):
        return '<Request [%s]>' % self.method

    def prepare(self):
        """Constructs a :class:`PreparedRequest <PreparedRequest>` for transmission and returns it."""
        p = PreparedRequest()
        p.prepare(method=(self.method),
          url=(self.url),
          headers=(self.headers),
          files=(self.files),
          data=(self.data),
          json=(self.json),
          params=(self.params),
          auth=(self.auth),
          cookies=(self.cookies),
          hooks=(self.hooks))
        return p


class PreparedRequest(RequestEncodingMixin, RequestHooksMixin):
    """PreparedRequest"""

    def __init__(self):
        self.method = None
        self.url = None
        self.headers = None
        self._cookies = None
        self.body = None
        self.hooks = default_hooks()
        self._body_position = None

    def prepare(self, method=None, url=None, headers=None, files=None, data=None, params=None, auth=None, cookies=None, hooks=None, json=None):
        """Prepares the entire request with the given parameters."""
        self.prepare_method(method)
        self.prepare_url(url, params)
        self.prepare_headers(headers)
        self.prepare_cookies(cookies)
        self.prepare_body(data, files, json)
        self.prepare_auth(auth, url)
        self.prepare_hooks(hooks)

    def __repr__(self):
        return '<PreparedRequest [%s]>' % self.method

    def copy(self):
        p = PreparedRequest()
        p.method = self.method
        p.url = self.url
        p.headers = self.headers.copy if self.headers is not None else None
        p._cookies = _copy_cookie_jar(self._cookies)
        p.body = self.body
        p.hooks = self.hooks
        p._body_position = self._body_position
        return p

    def prepare_method(self, method):
        """Prepares the given HTTP method."""
        self.method = method
        if self.method is not None:
            self.method = to_native_string(self.method.upper)

    @staticmethod
    def _get_idna_encoded_host(host):
        import idna
        try:
            host = idna.encode(host, uts46=True).decode('utf-8')
        except idna.IDNAError:
            raise UnicodeError
        else:
            return host

    def prepare_url(self, url, params):
        """Prepares the given HTTP URL."""
        if isinstance(url, bytes):
            url = url.decode('utf8')
        else:
            url = unicode(url) if is_py2 else str(url)
        url = url.lstrip
        if ':' in url:
            if not url.lower.startswith('http'):
                self.url = url
                return
        try:
            scheme, auth, host, port, path, query, fragment = parse_url(url)
        except LocationParseError as e:
            try:
                raise InvalidURL(*e.args)
            finally:
                e = None
                del e

        else:
            if not scheme:
                error = 'Invalid URL {0!r}: No schema supplied. Perhaps you meant http://{0}?'
                error = error.format(to_native_string(url, 'utf8'))
                raise MissingSchema(error)
            elif not host:
                raise InvalidURL('Invalid URL %r: No host supplied' % url)
            else:
                if not unicode_is_ascii(host):
                    try:
                        host = self._get_idna_encoded_host(host)
                    except UnicodeError:
                        raise InvalidURL('URL has an invalid label.')

                elif host.startswith('*'):
                    raise InvalidURL('URL has an invalid label.')
                netloc = auth or 
                if netloc:
                    netloc += '@'
                netloc += host
                if port:
                    netloc += ':' + str(port)
                if not path:
                    path = '/'
                if is_py2:
                    if isinstance(scheme, str):
                        scheme = scheme.encode('utf-8')
                    if isinstance(netloc, str):
                        netloc = netloc.encode('utf-8')
                    if isinstance(path, str):
                        path = path.encode('utf-8')
                    if isinstance(query, str):
                        query = query.encode('utf-8')
                    if isinstance(fragment, str):
                        fragment = fragment.encode('utf-8')
                    if isinstance(params, (str, bytes)):
                        params = to_native_string(params)
                    enc_params = self._encode_params(params)
                    if enc_params:
                        if query:
                            query = '%s&%s' % (query, enc_params)
                else:
                    query = enc_params
            url = requote_uri(urlunparse([scheme, netloc, path, None, query, fragment]))
            self.url = url

    def prepare_headers(self, headers):
        """Prepares the given HTTP headers."""
        self.headers = CaseInsensitiveDict()
        if headers:
            for header in headers.items:
                check_header_validity(header)
                name, value = header
                self.headers[to_native_string(name)] = value

    def prepare_body(self, data, files, json=None):
        """Prepares the given HTTP body data."""
        body = None
        content_type = None
        if not data:
            if json is not None:
                content_type = 'application/json'
                body = complexjson.dumps(json)
                if not isinstance(body, bytes):
                    body = body.encode('utf-8')
        is_stream = all([
         hasattr(data, '__iter__'),
         not isinstance(data, (basestring, list, tuple, Mapping))])
        try:
            length = super_len(data)
        except (TypeError, AttributeError, UnsupportedOperation):
            length = None
        else:
            if is_stream:
                body = data
                if getattr(body, 'tell', None) is not None:
                    try:
                        self._body_position = body.tell
                    except (IOError, OSError):
                        self._body_position = object()
                    else:
                        if files:
                            raise NotImplementedError('Streamed bodies and files are mutually exclusive.')
                        if length:
                            self.headers['Content-Length'] = builtin_str(length)
                        else:
                            self.headers['Transfer-Encoding'] = 'chunked'
                elif files:
                    body, content_type = self._encode_files(files, data)
            elif data:
                body = self._encode_params(data)
                if isinstance(data, basestring) or hasattr(data, 'read'):
                    content_type = None
                else:
                    content_type = 'application/x-www-form-urlencoded'
            self.prepare_content_length(body)
            if content_type:
                if 'content-type' not in self.headers:
                    self.headers['Content-Type'] = content_type
            self.body = body

    def prepare_content_length(self, body):
        """Prepare Content-Length header based on request method and body"""
        if body is not None:
            length = super_len(body)
            if length:
                self.headers['Content-Length'] = builtin_str(length)
        elif self.method not in ('GET', 'HEAD') and self.headers.get('Content-Length') is None:
            self.headers['Content-Length'] = '0'

    def prepare_auth(self, auth, url=''):
        """Prepares the given HTTP auth data."""
        if auth is None:
            url_auth = get_auth_from_url(self.url)
            auth = url_auth if any(url_auth) else None
        if auth:
            if isinstance(auth, tuple):
                if len(auth) == 2:
                    auth = HTTPBasicAuth(*auth)
            r = auth(self)
            self.__dict__.update(r.__dict__)
            self.prepare_content_length(self.body)

    def prepare_cookies(self, cookies):
        """Prepares the given HTTP cookie data.

        This function eventually generates a ``Cookie`` header from the
        given cookies using cookielib. Due to cookielib's design, the header
        will not be regenerated if it already exists, meaning this function
        can only be called once for the life of the
        :class:`PreparedRequest <PreparedRequest>` object. Any subsequent calls
        to ``prepare_cookies`` will have no actual effect, unless the "Cookie"
        header is removed beforehand.
        """
        if isinstance(cookies, cookielib.CookieJar):
            self._cookies = cookies
        else:
            self._cookies = cookiejar_from_dict(cookies)
        cookie_header = get_cookie_header(self._cookies, self)
        if cookie_header is not None:
            self.headers['Cookie'] = cookie_header

    def prepare_hooks(self, hooks):
        """Prepares the given hooks."""
        hooks = hooks or 
        for event in hooks:
            self.register_hook(event, hooks[event])


class Response(object):
    """Response"""
    __attrs__ = [
     '_content', 'status_code', 'headers', 'url', 'history',
     'encoding', 'reason', 'cookies', 'elapsed', 'request']

    def __init__(self):
        self._content = False
        self._content_consumed = False
        self._next = None
        self.status_code = None
        self.headers = CaseInsensitiveDict()
        self.raw = None
        self.url = None
        self.encoding = None
        self.history = []
        self.reason = None
        self.cookies = cookiejar_from_dict({})
        self.elapsed = datetime.timedelta(0)
        self.request = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close

    def __getstate__--- This code section failed: ---

 L. 652         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _content_consumed
                4  POP_JUMP_IF_TRUE     12  'to 12'

 L. 653         6  LOAD_DEREF               'self'
                8  LOAD_ATTR                content
               10  POP_TOP          
             12_0  COME_FROM             4  '4'

 L. 655        12  LOAD_CLOSURE             'self'
               14  BUILD_TUPLE_1         1 
               16  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               18  LOAD_STR                 'Response.__getstate__.<locals>.<dictcomp>'
               20  MAKE_FUNCTION_8          'closure'
               22  LOAD_DEREF               'self'
               24  LOAD_ATTR                __attrs__
               26  GET_ITER         
               28  CALL_FUNCTION_1       1  ''
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 16

    def __setstate__(self, state):
        for name, value in state.items:
            setattr(self, name, value)

        setattr(self, '_content_consumed', True)
        setattr(self, 'raw', None)

    def __repr__(self):
        return '<Response [%s]>' % self.status_code

    def __bool__(self):
        """Returns True if :attr:`status_code` is less than 400.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code, is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        return self.ok

    def __nonzero__(self):
        """Returns True if :attr:`status_code` is less than 400.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code, is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        return self.ok

    def __iter__(self):
        """Allows you to use a response as an iterator."""
        return self.iter_content(128)

    @property
    def ok(self):
        """Returns True if :attr:`status_code` is less than 400, False if not.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        try:
            self.raise_for_status
        except HTTPError:
            return False
        else:
            return True

    @property
    def is_redirect(self):
        """True if this Response is a well-formed HTTP redirect that could have
        been processed automatically (by :meth:`Session.resolve_redirects`).
        """
        return 'location' in self.headers and self.status_code in REDIRECT_STATI

    @property
    def is_permanent_redirect(self):
        """True if this Response one of the permanent versions of redirect."""
        return 'location' in self.headers and self.status_code in (codes.moved_permanently, codes.permanent_redirect)

    @property
    def next(self):
        """Returns a PreparedRequest for the next request in a redirect chain, if there is one."""
        return self._next

    @property
    def apparent_encoding(self):
        """The apparent encoding, provided by the chardet library."""
        return chardet.detect(self.content)['encoding']

    def iter_content(self, chunk_size=1, decode_unicode=False):
        """Iterates over the response data.  When stream=True is set on the
        request, this avoids reading the content at once into memory for
        large responses.  The chunk size is the number of bytes it should
        read into memory.  This is not necessarily the length of each item
        returned as decoding can take place.

        chunk_size must be of type int or None. A value of None will
        function differently depending on the value of `stream`.
        stream=True will read data as it arrives in whatever size the
        chunks are received. If stream=False, data is returned as
        a single chunk.

        If decode_unicode is True, content will be decoded using the best
        available encoding based on the response.
        """

        def generate():
            if hasattr(self.raw, 'stream'):
                try:
                    for chunk in self.raw.stream(chunk_size, decode_content=True):
                        yield chunk

                except ProtocolError as e:
                    try:
                        raise ChunkedEncodingError(e)
                    finally:
                        e = None
                        del e

                except DecodeError as e:
                    try:
                        raise ContentDecodingError(e)
                    finally:
                        e = None
                        del e

                except ReadTimeoutError as e:
                    try:
                        raise ConnectionError(e)
                    finally:
                        e = None
                        del e

            else:
                while True:
                    chunk = self.raw.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

            self._content_consumed = True

        if self._content_consumed and isinstance(self._content, bool):
            raise StreamConsumedError()
        elif chunk_size is not None and not isinstance(chunk_size, int):
            raise TypeError('chunk_size must be an int, it is instead a %s.' % type(chunk_size))
        reused_chunks = iter_slices(self._content, chunk_size)
        stream_chunks = generate()
        chunks = reused_chunks if self._content_consumed else stream_chunks
        if decode_unicode:
            chunks = stream_decode_response_unicode(chunks, self)
        return chunks

    def iter_lines(self, chunk_size=ITER_CHUNK_SIZE, decode_unicode=False, delimiter=None):
        """Iterates over the response data, one line at a time.  When
        stream=True is set on the request, this avoids reading the
        content at once into memory for large responses.

        .. note:: This method is not reentrant safe.
        """
        pending = None
        for chunk in self.iter_content(chunk_size=chunk_size, decode_unicode=decode_unicode):
            if pending is not None:
                chunk = pending + chunk
            elif delimiter:
                lines = chunk.split(delimiter)
            else:
                lines = chunk.splitlines
            if lines and lines[(-1)] and chunk and lines[(-1)][(-1)] == chunk[(-1)]:
                pending = lines.pop
            else:
                pending = None
            for line in lines:
                yield line

            if pending is not None:
                yield pending

    @property
    def content(self):
        """Content of the response, in bytes."""
        if self._content is False:
            if self._content_consumed:
                raise RuntimeError('The content for this response was already consumed')
            elif self.status_code == 0 or self.raw is None:
                self._content = None
            else:
                self._content = (b'').join(self.iter_content(CONTENT_CHUNK_SIZE)) or 
        self._content_consumed = True
        return self._content

    @property
    def text(self):
        """Content of the response, in unicode.

        If Response.encoding is None, encoding will be guessed using
        ``chardet``.

        The encoding of the response content is determined based solely on HTTP
        headers, following RFC 2616 to the letter. If you can take advantage of
        non-HTTP knowledge to make a better guess at the encoding, you should
        set ``r.encoding`` appropriately before accessing this property.
        """
        content = None
        encoding = self.encoding
        if not self.content:
            return str('')
        if self.encoding is None:
            encoding = self.apparent_encoding
        try:
            content = str((self.content), encoding, errors='replace')
        except (LookupError, TypeError):
            content = str((self.content), errors='replace')
        else:
            return content

    def json--- This code section failed: ---

 L. 880         0  LOAD_FAST                'self'
                2  LOAD_ATTR                encoding
                4  POP_JUMP_IF_TRUE     90  'to 90'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                content
               10  POP_JUMP_IF_FALSE    90  'to 90'
               12  LOAD_GLOBAL              len
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                content
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_CONST               3
               22  COMPARE_OP               >
               24  POP_JUMP_IF_FALSE    90  'to 90'

 L. 885        26  LOAD_GLOBAL              guess_json_utf
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                content
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'encoding'

 L. 886        36  LOAD_FAST                'encoding'
               38  LOAD_CONST               None
               40  COMPARE_OP               is-not
               42  POP_JUMP_IF_FALSE    90  'to 90'

 L. 887        44  SETUP_FINALLY        70  'to 70'

 L. 888        46  LOAD_GLOBAL              complexjson
               48  LOAD_ATTR                loads

 L. 889        50  LOAD_FAST                'self'
               52  LOAD_ATTR                content
               54  LOAD_METHOD              decode
               56  LOAD_FAST                'encoding'
               58  CALL_METHOD_1         1  ''

 L. 888        60  BUILD_TUPLE_1         1 

 L. 889        62  LOAD_FAST                'kwargs'

 L. 888        64  CALL_FUNCTION_EX_KW     1  'keyword args'
               66  POP_BLOCK        
               68  RETURN_VALUE     
             70_0  COME_FROM_FINALLY    44  '44'

 L. 891        70  DUP_TOP          
               72  LOAD_GLOBAL              UnicodeDecodeError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE    88  'to 88'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 896        84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            76  '76'
               88  END_FINALLY      
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            42  '42'
             90_2  COME_FROM            24  '24'
             90_3  COME_FROM            10  '10'
             90_4  COME_FROM             4  '4'

 L. 897        90  LOAD_GLOBAL              complexjson
               92  LOAD_ATTR                loads
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                text
               98  BUILD_TUPLE_1         1 
              100  LOAD_FAST                'kwargs'
              102  CALL_FUNCTION_EX_KW     1  'keyword args'
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 70

    @property
    def links(self):
        """Returns the parsed header links of the response, if any."""
        header = self.headers.get('link')
        l = {}
        if header:
            links = parse_header_links(header)
            for link in links:
                key = link.get('rel') or 
                l[key] = link

        return l

    def raise_for_status(self):
        """Raises stored :class:`HTTPError`, if one occurred."""
        http_error_msg = ''
        if isinstance(self.reason, bytes):
            try:
                reason = self.reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = self.reason.decode('iso-8859-1')

        else:
            reason = self.reason
        if 400 <= self.status_code < 500:
            http_error_msg = '%s Client Error: %s for url: %s' % (self.status_code, reason, self.url)
        elif 500 <= self.status_code < 600:
            http_error_msg = '%s Server Error: %s for url: %s' % (self.status_code, reason, self.url)
        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)

    def close(self):
        """Releases the connection back to the pool. Once this method has been
        called the underlying ``raw`` object must not be accessed again.

        *Note: Should not normally need to be called explicitly.*
        """
        if not self._content_consumed:
            self.raw.close
        release_conn = getattr(self.raw, 'release_conn', None)
        if release_conn is not None:
            release_conn()


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break
#      L. 763       186  BREAK_LOOP          196  'to 196'