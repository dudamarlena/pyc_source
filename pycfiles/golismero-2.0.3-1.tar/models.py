# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/requests/models.py
# Compiled at: 2013-08-26 10:52:44
"""
requests.models
~~~~~~~~~~~~~~~

This module contains the primary objects that power Requests.
"""
import collections, logging, datetime
from io import BytesIO
from .hooks import default_hooks
from .structures import CaseInsensitiveDict
from .auth import HTTPBasicAuth
from .cookies import cookiejar_from_dict, get_cookie_header
from .packages.urllib3.filepost import encode_multipart_formdata
from .packages.urllib3.util import parse_url
from .exceptions import HTTPError, RequestException, MissingSchema, InvalidURL, ChunkedEncodingError
from .utils import guess_filename, get_auth_from_url, requote_uri, stream_decode_response_unicode, to_key_val_list, parse_header_links, iter_slices, guess_json_utf, super_len
from .compat import cookielib, urlunparse, urlsplit, urlencode, str, bytes, StringIO, is_py2, chardet, json, builtin_str, basestring, IncompleteRead
CONTENT_CHUNK_SIZE = 10240
ITER_CHUNK_SIZE = 512
log = logging.getLogger(__name__)

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
        return ('').join(url)

    @staticmethod
    def _encode_params(data):
        """Encode parameters in a piece of data.

        Will successfully encode parameters when passed as a dict or a list of
        2-tuples. Order is retained if data is a list of 2-tuples but arbitrary
        if parameters are supplied as a dict.
        """
        if isinstance(data, (str, bytes)):
            return data
        else:
            if hasattr(data, 'read'):
                return data
            else:
                if hasattr(data, '__iter__'):
                    result = []
                    for k, vs in to_key_val_list(data):
                        if isinstance(vs, basestring) or not hasattr(vs, '__iter__'):
                            vs = [
                             vs]
                        for v in vs:
                            if v is not None:
                                result.append((
                                 k.encode('utf-8') if isinstance(k, str) else k,
                                 v.encode('utf-8') if isinstance(v, str) else v))

                    return urlencode(result, doseq=True)
                return data

            return

    @staticmethod
    def _encode_files(files, data):
        """Build the body for a multipart/form-data request.

        Will successfully encode files when passed as a dict or a list of
        2-tuples. Order is retained if data is a list of 2-tuples but abritrary
        if parameters are supplied as a dict.

        """
        if not files or isinstance(data, str):
            return
        new_fields = []
        fields = to_key_val_list(data or {})
        files = to_key_val_list(files or {})
        for field, val in fields:
            if isinstance(val, basestring) or not hasattr(val, '__iter__'):
                val = [
                 val]
            for v in val:
                if v is not None:
                    new_fields.append((
                     field.decode('utf-8') if isinstance(field, bytes) else field,
                     v.encode('utf-8') if isinstance(v, str) else v))

        for k, v in files:
            ft = None
            if isinstance(v, (tuple, list)):
                if len(v) == 2:
                    fn, fp = v
                else:
                    fn, fp, ft = v
            else:
                fn = guess_filename(v) or k
                fp = v
            if isinstance(fp, str):
                fp = StringIO(fp)
            if isinstance(fp, bytes):
                fp = BytesIO(fp)
            if ft:
                new_v = (
                 fn, fp.read(), ft)
            else:
                new_v = (
                 fn, fp.read())
            new_fields.append((k, new_v))

        body, content_type = encode_multipart_formdata(new_fields)
        return (
         body, content_type)


class RequestHooksMixin(object):

    def register_hook(self, event, hook):
        """Properly register a hook."""
        if isinstance(hook, collections.Callable):
            self.hooks[event].append(hook)
        elif hasattr(hook, '__iter__'):
            self.hooks[event].extend(h for h in hook if isinstance(h, collections.Callable))

    def deregister_hook(self, event, hook):
        """Deregister a previously registered hook.
        Returns True if the hook existed, False if not.
        """
        try:
            self.hooks[event].remove(hook)
            return True
        except ValueError:
            return False


class Request(RequestHooksMixin):
    """A user-created :class:`Request <Request>` object.

    Used to prepare a :class:`PreparedRequest <PreparedRequest>`, which is sent to the server.

    :param method: HTTP method to use.
    :param url: URL to send.
    :param headers: dictionary of headers to send.
    :param files: dictionary of {filename: fileobject} files to multipart upload.
    :param data: the body to attach the request. If a dictionary is provided, form-encoding will take place.
    :param params: dictionary of URL parameters to append to the URL.
    :param auth: Auth handler or (user, pass) tuple.
    :param cookies: dictionary or CookieJar of cookies to attach to this request.
    :param hooks: dictionary of callback hooks, for internal usage.

    Usage::

      >>> import requests
      >>> req = requests.Request('GET', 'http://httpbin.org/get')
      >>> req.prepare()
      <PreparedRequest [GET]>

    """

    def __init__(self, method=None, url=None, headers=None, files=None, data=dict(), params=dict(), auth=None, cookies=None, hooks=None):
        data = [] if data is None else data
        files = [] if files is None else files
        headers = {} if headers is None else headers
        params = {} if params is None else params
        hooks = {} if hooks is None else hooks
        self.hooks = default_hooks()
        for k, v in list(hooks.items()):
            self.register_hook(event=k, hook=v)

        self.method = method
        self.url = url
        self.headers = headers
        self.files = files
        self.data = data
        self.params = params
        self.auth = auth
        self.cookies = cookies
        return

    def __repr__(self):
        return '<Request [%s]>' % self.method

    def prepare(self):
        """Constructs a :class:`PreparedRequest <PreparedRequest>` for transmission and returns it."""
        p = PreparedRequest()
        p.prepare(method=self.method, url=self.url, headers=self.headers, files=self.files, data=self.data, params=self.params, auth=self.auth, cookies=self.cookies, hooks=self.hooks)
        return p


class PreparedRequest(RequestEncodingMixin, RequestHooksMixin):
    """The fully mutable :class:`PreparedRequest <PreparedRequest>` object,
    containing the exact bytes that will be sent to the server.

    Generated from either a :class:`Request <Request>` object or manually.

    Usage::

      >>> import requests
      >>> req = requests.Request('GET', 'http://httpbin.org/get')
      >>> r = req.prepare()
      <PreparedRequest [GET]>

      >>> s = requests.Session()
      >>> s.send(r)
      <Response [200]>

    """

    def __init__(self):
        self.method = None
        self.url = None
        self.headers = None
        self.body = None
        self.hooks = default_hooks()
        return

    def prepare(self, method=None, url=None, headers=None, files=None, data=None, params=None, auth=None, cookies=None, hooks=None):
        """Prepares the the entire request with the given parameters."""
        self.prepare_method(method)
        self.prepare_url(url, params)
        self.prepare_headers(headers)
        self.prepare_cookies(cookies)
        self.prepare_body(data, files)
        self.prepare_auth(auth, url)
        self.prepare_hooks(hooks)

    def __repr__(self):
        return '<PreparedRequest [%s]>' % self.method

    def copy(self):
        p = PreparedRequest()
        p.method = self.method
        p.url = self.url
        p.headers = self.headers
        p.body = self.body
        p.hooks = self.hooks
        return p

    def prepare_method(self, method):
        """Prepares the given HTTP method."""
        self.method = method
        if self.method is not None:
            self.method = self.method.upper()
        return

    def prepare_url(self, url, params):
        """Prepares the given HTTP URL."""
        try:
            url = unicode(url)
        except NameError:
            url = str(url)
        except UnicodeDecodeError:
            pass

        scheme, auth, host, port, path, query, fragment = parse_url(url)
        if not scheme:
            raise MissingSchema('Invalid URL %r: No schema supplied' % url)
        if not host:
            raise InvalidURL('Invalid URL %r: No host supplied' % url)
        try:
            host = host.encode('idna').decode('utf-8')
        except UnicodeError:
            raise InvalidURL('URL has an invalid label.')

        netloc = auth or ''
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
        enc_params = self._encode_params(params)
        if enc_params:
            if query:
                query = '%s&%s' % (query, enc_params)
            else:
                query = enc_params
        url = requote_uri(urlunparse([scheme, netloc, path, None, query, fragment]))
        self.url = url
        return

    def prepare_headers(self, headers):
        """Prepares the given HTTP headers."""
        if headers:
            headers = dict((name.encode('ascii'), value) for name, value in headers.items())
            self.headers = CaseInsensitiveDict(headers)
        else:
            self.headers = CaseInsensitiveDict()

    def prepare_body(self, data, files):
        """Prepares the given HTTP body data."""
        body = None
        content_type = None
        length = None
        is_stream = all([
         hasattr(data, '__iter__'),
         not isinstance(data, basestring),
         not isinstance(data, list),
         not isinstance(data, dict)])
        try:
            length = super_len(data)
        except (TypeError, AttributeError):
            length = None

        if is_stream:
            body = data
            if files:
                raise NotImplementedError('Streamed bodies and files are mutually exclusive.')
            if length is not None:
                self.headers['Content-Length'] = str(length)
            else:
                self.headers['Transfer-Encoding'] = 'chunked'
        else:
            if files:
                body, content_type = self._encode_files(files, data)
            elif data:
                body = self._encode_params(data)
                if isinstance(data, str) or isinstance(data, builtin_str) or hasattr(data, 'read'):
                    content_type = None
                else:
                    content_type = 'application/x-www-form-urlencoded'
            self.prepare_content_length(body)
            if content_type and 'content-type' not in self.headers:
                self.headers['Content-Type'] = content_type
        self.body = body
        return

    def prepare_content_length(self, body):
        if hasattr(body, 'seek') and hasattr(body, 'tell'):
            body.seek(0, 2)
            self.headers['Content-Length'] = str(body.tell())
            body.seek(0, 0)
        elif body is not None:
            l = super_len(body)
            if l:
                self.headers['Content-Length'] = str(l)
        elif self.method not in ('GET', 'HEAD'):
            self.headers['Content-Length'] = '0'
        return

    def prepare_auth(self, auth, url=''):
        """Prepares the given HTTP auth data."""
        if auth is None:
            url_auth = get_auth_from_url(self.url)
            auth = url_auth if any(url_auth) else None
        if auth:
            if isinstance(auth, tuple) and len(auth) == 2:
                auth = HTTPBasicAuth(*auth)
            r = auth(self)
            self.__dict__.update(r.__dict__)
            self.prepare_content_length(self.body)
        return

    def prepare_cookies(self, cookies):
        """Prepares the given HTTP cookie data."""
        if isinstance(cookies, cookielib.CookieJar):
            cookies = cookies
        else:
            cookies = cookiejar_from_dict(cookies)
        if 'cookie' not in self.headers:
            cookie_header = get_cookie_header(cookies, self)
            if cookie_header is not None:
                self.headers['Cookie'] = cookie_header
        return

    def prepare_hooks(self, hooks):
        """Prepares the given hooks."""
        for event in hooks:
            self.register_hook(event, hooks[event])


class Response(object):
    """The :class:`Response <Response>` object, which contains a
    server's response to an HTTP request.
    """

    def __init__(self):
        super(Response, self).__init__()
        self._content = False
        self._content_consumed = False
        self.status_code = None
        self.headers = CaseInsensitiveDict()
        self.raw = None
        self.url = None
        self.encoding = None
        self.history = []
        self.reason = None
        self.cookies = cookiejar_from_dict({})
        self.elapsed = datetime.timedelta(0)
        return

    def __repr__(self):
        return '<Response [%s]>' % self.status_code

    def __bool__(self):
        """Returns true if :attr:`status_code` is 'OK'."""
        return self.ok

    def __nonzero__(self):
        """Returns true if :attr:`status_code` is 'OK'."""
        return self.ok

    def __iter__(self):
        """Allows you to use a response as an iterator."""
        return self.iter_content(128)

    @property
    def ok(self):
        try:
            self.raise_for_status()
        except RequestException:
            return False

        return True

    @property
    def apparent_encoding(self):
        """The apparent encoding, provided by the lovely Charade library
        (Thanks, Ian!)."""
        return chardet.detect(self.content)['encoding']

    def iter_content(self, chunk_size=1, decode_unicode=False):
        """Iterates over the response data.  When stream=True is set on the
        request, this avoids reading the content at once into memory for
        large responses.  The chunk size is the number of bytes it should
        read into memory.  This is not necessarily the length of each item
        returned as decoding can take place.
        """
        if self._content_consumed:
            return iter_slices(self._content, chunk_size)

        def generate():
            try:
                try:
                    for chunk in self.raw.stream(chunk_size, decode_content=True):
                        yield chunk

                except IncompleteRead as e:
                    raise ChunkedEncodingError(e)

            except AttributeError:
                while 1:
                    chunk = self.raw.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

            self._content_consumed = True

        gen = generate()
        if decode_unicode:
            gen = stream_decode_response_unicode(gen, self)
        return gen

    def iter_lines(self, chunk_size=ITER_CHUNK_SIZE, decode_unicode=None):
        """Iterates over the response data, one line at a time.  When
        stream=True is set on the request, this avoids reading the
        content at once into memory for large responses.
        """
        pending = None
        for chunk in self.iter_content(chunk_size=chunk_size, decode_unicode=decode_unicode):
            if pending is not None:
                chunk = pending + chunk
            lines = chunk.splitlines()
            if lines and lines[(-1)] and chunk and lines[(-1)][(-1)] == chunk[(-1)]:
                pending = lines.pop()
            else:
                pending = None
            for line in lines:
                yield line

        if pending is not None:
            yield pending
        return

    @property
    def content(self):
        """Content of the response, in bytes."""
        if self._content is False:
            try:
                if self._content_consumed:
                    raise RuntimeError('The content for this response was already consumed')
                if self.status_code == 0:
                    self._content = None
                else:
                    self._content = bytes().join(self.iter_content(CONTENT_CHUNK_SIZE)) or bytes()
            except AttributeError:
                self._content = None

        self._content_consumed = True
        return self._content

    @property
    def text(self):
        """Content of the response, in unicode.

        if Response.encoding is None and chardet module is available, encoding
        will be guessed.
        """
        content = None
        encoding = self.encoding
        if not self.content:
            return str('')
        else:
            if self.encoding is None:
                encoding = self.apparent_encoding
            try:
                content = str(self.content, encoding, errors='replace')
            except (LookupError, TypeError):
                content = str(self.content, errors='replace')

            return content

    def json(self, **kwargs):
        r"""Returns the json-encoded content of a response, if any.

        :param \*\*kwargs: Optional arguments that ``json.loads`` takes.
        """
        if not self.encoding and len(self.content) > 3:
            encoding = guess_json_utf(self.content)
            if encoding is not None:
                return json.loads(self.content.decode(encoding), **kwargs)
        return json.loads((self.text or self.content), **kwargs)

    @property
    def links(self):
        """Returns the parsed header links of the response, if any."""
        header = self.headers.get('link')
        l = {}
        if header:
            links = parse_header_links(header)
            for link in links:
                key = link.get('rel') or link.get('url')
                l[key] = link

        return l

    def raise_for_status(self):
        """Raises stored :class:`HTTPError`, if one occurred."""
        http_error_msg = ''
        if 400 <= self.status_code < 500:
            http_error_msg = '%s Client Error: %s' % (self.status_code, self.reason)
        elif 500 <= self.status_code < 600:
            http_error_msg = '%s Server Error: %s' % (self.status_code, self.reason)
        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)

    def close(self):
        """Closes the underlying file descriptor and releases the connection
        back to the pool.

        *Note: Should not normally need to be called explicitly.*
        """
        return self.raw.release_conn()