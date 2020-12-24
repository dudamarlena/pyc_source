# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\api\request.py
# Compiled at: 2017-04-19 05:14:02
from __future__ import unicode_literals
import base64, logging, mimetypes, os, random, shutil, sys
from io import BytesIO
from json import loads as json_loads
import six
from six.moves.http_client import UNAUTHORIZED, NOT_MODIFIED
from six.moves.http_cookiejar import Cookie, CookieJar, MozillaCookieJar
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from six.moves.urllib.request import BaseHandler, HTTPBasicAuthHandler, HTTPCookieProcessor, HTTPDigestAuthHandler, HTTPErrorProcessor, HTTPPasswordMgr, ProxyHandler, Request as URLRequest, build_opener, install_opener, urlopen
from rbtools import get_package_version
from rbtools.api.cache import APICache
from rbtools.api.errors import APIError, create_api_error, ServerInterfaceError
from rbtools.utils.filesystem import get_home_path
try:
    import ssl
    from six.moves.urllib.request import HTTPSHandler
except ImportError:
    ssl = None
    HTTPSHandler = None

RBTOOLS_COOKIE_FILE = b'.rbtools-cookies'
RB_COOKIE_NAME = b'rbsessionid'

class HttpRequest(object):
    """High-level HTTP-request object."""

    def __init__(self, url, method=b'GET', query_args={}):
        self.method = method
        self.headers = {}
        self._fields = {}
        self._files = {}
        query_args = dict([ (key.replace(b'_', b'-'), value) for key, value in six.iteritems(query_args)
                          ])
        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(query_args)
        url_parts[4] = urlencode(query)
        self.url = urlunparse(url_parts)

    def add_field(self, name, value):
        self._fields[name] = value

    def add_file(self, name, filename, content):
        self._files[name] = {b'filename': filename, 
           b'content': content}

    def del_field(self, name):
        del self._fields[name]

    def del_file(self, filename):
        del self._files[filename]

    def encode_multipart_formdata(self):
        """Encodes data for use in an HTTP request.

        Parameters:
            fields - the fields to be encoded.  This should be a dict in a
                     key:value format
            files  - the files to be encoded.  This should be a dict in a
                     key:dict, filename:value and content:value format
        """
        if not (self._fields or self._files):
            return (None, None)
        else:
            NEWLINE = b'\r\n'
            BOUNDARY = self._make_mime_boundary()
            content = BytesIO()
            for key in self._fields:
                content.write(b'--' + BOUNDARY + NEWLINE)
                content.write(b'Content-Disposition: form-data; name="%s"' % key.encode(b'utf-8'))
                content.write(NEWLINE + NEWLINE)
                if isinstance(self._fields[key], six.binary_type):
                    content.write(self._fields[key] + NEWLINE)
                else:
                    content.write(six.text_type(self._fields[key]).encode(b'utf-8') + NEWLINE)

            for key in self._files:
                filename = self._files[key][b'filename']
                value = self._files[key][b'content']
                mime_type = mimetypes.guess_type(filename)[0]
                if mime_type:
                    mime_type = mime_type.encode(b'utf-8')
                else:
                    mime_type = b'application/octet-stream'
                content.write(b'--' + BOUNDARY + NEWLINE)
                content.write(b'Content-Disposition: form-data; name="%s"; ' % key.encode(b'utf-8'))
                content.write(b'filename="%s"' % filename.encode(b'utf-8') + NEWLINE)
                content.write(b'Content-Type: %s' % mime_type + NEWLINE)
                content.write(NEWLINE)
                if isinstance(value, six.text_type):
                    content.write(value.encode(b'utf-8'))
                else:
                    content.write(value)
                content.write(NEWLINE)

            content.write(b'--' + BOUNDARY + b'--' + NEWLINE + NEWLINE)
            content_type = b'multipart/form-data; boundary=%s' % BOUNDARY
            return (
             content_type, content.getvalue())

    def _make_mime_boundary(self):
        """Create a mime boundary.

        This exists because mimetools.choose_boundary() is gone in Python 3.x,
        and email.generator._make_boundary isn't really appropriate to use
        here.
        """
        fmt = b'%%0%dd' % len(repr(sys.maxsize - 1))
        token = random.randrange(sys.maxsize)
        return b'===============' + (fmt % token).encode(b'utf-8') + b'=='


class Request(URLRequest):
    """A request which contains a method attribute."""

    def __init__(self, url, body=b'', headers={}, method=b'PUT'):
        URLRequest.__init__(self, url, body, headers)
        self.method = method

    def get_method(self):
        return self.method


class PresetHTTPAuthHandler(BaseHandler):
    """Handler that presets the use of HTTP Basic Auth."""
    handler_order = 480
    AUTH_HEADER = b'Authorization'

    def __init__(self, url, password_mgr):
        self.url = url
        self.password_mgr = password_mgr
        self.used = False

    def reset(self, username, password):
        self.password_mgr.rb_user = username
        self.password_mgr.rb_pass = password
        self.used = False

    def http_request(self, request):
        if not self.used:
            if self.password_mgr.api_token:
                request.add_header(self.AUTH_HEADER, b'token %s' % self.password_mgr.api_token)
                self.used = True
            elif self.password_mgr.rb_user:
                username, password = self.password_mgr.find_user_password(b'Web API', self.url)
                raw = b'%s:%s' % (username, password)
                request.add_header(self.AUTH_HEADER, b'Basic %s' % base64.b64encode(raw).strip())
                self.used = True
        return request

    https_request = http_request


class ReviewBoardHTTPErrorProcessor(HTTPErrorProcessor):
    """Processes HTTP error codes.

    Python 2.6 gets HTTP error code processing right, but 2.4 and 2.5 only
    accepts HTTP 200 and 206 as success codes. This handler ensures that
    anything in the 200 range, as well as 304, is a success.
    """

    def http_response(self, request, response):
        if not (200 <= response.code < 300 or response.code == NOT_MODIFIED):
            response = self.parent.error(b'http', request, response, response.code, response.msg, response.info())
        return response

    https_response = http_response


class ReviewBoardHTTPBasicAuthHandler(HTTPBasicAuthHandler):
    """Custom Basic Auth handler that doesn't retry excessively.

    urllib's HTTPBasicAuthHandler retries over and over, which is useless. This
    subclass only retries once to make sure we've attempted with a valid
    username and password. It will then fail so we can use our own retry
    handler.

    This also supports two-factor auth, for Review Board servers that
    support it. When requested by the server, the client will be prompted
    for a one-time password token, which would be sent generally through
    a mobile device. In this case, the client will prompt up to a set
    number of times until a valid token is entered.
    """
    OTP_TOKEN_HEADER = b'X-ReviewBoard-OTP'
    MAX_OTP_TOKEN_ATTEMPTS = 5

    def __init__(self, *args, **kwargs):
        HTTPBasicAuthHandler.__init__(self, *args, **kwargs)
        self._retried = False
        self._lasturl = b''
        self._needs_otp_token = False
        self._otp_token_attempts = 0

    def retry_http_basic_auth(self, host, request, realm, *args, **kwargs):
        if self._lasturl != host:
            self._retried = False
        self._lasturl = host
        if self._retried:
            return None
        else:
            self._retried = True
            response = self._do_http_basic_auth(host, request, realm)
            if response and response.code != UNAUTHORIZED:
                self._retried = False
            return response

    def _do_http_basic_auth(self, host, request, realm):
        user, password = self.passwd.find_user_password(realm, host)
        if password is None:
            return
        else:
            raw = b'%s:%s' % (user, password)
            auth = b'Basic %s' % base64.b64encode(raw).strip()
            if request.headers.get(self.auth_header, None) == auth and (not self._needs_otp_token or self._otp_token_attempts > self.MAX_OTP_TOKEN_ATTEMPTS):
                return
            request.add_unredirected_header(self.auth_header, auth)
            try:
                response = self.parent.open(request, timeout=request.timeout)
                return response
            except HTTPError as e:
                if e.code == UNAUTHORIZED:
                    headers = e.info()
                    otp_header = headers.get(self.OTP_TOKEN_HEADER, b'')
                    if otp_header.startswith(b'required'):
                        self._needs_otp_token = True
                        required, token_method = otp_header.split(b';')
                        token = self.passwd.get_otp_token(request.get_full_url(), token_method.strip())
                        if not token:
                            return
                        request.add_unredirected_header(self.OTP_TOKEN_HEADER, token)
                        self._otp_token_attempts += 1
                        return self._do_http_basic_auth(host, request, realm)
                raise

            return


class ReviewBoardHTTPPasswordMgr(HTTPPasswordMgr):
    """Adds HTTP authentication support for URLs.

    Python 2.4's password manager has a bug in http authentication
    when the target server uses a non-standard port.  This works
    around that bug on Python 2.4 installs.

    See: http://bugs.python.org/issue974757
    """

    def __init__(self, reviewboard_url, rb_user=None, rb_pass=None, api_token=None, auth_callback=None, otp_token_callback=None):
        HTTPPasswordMgr.__init__(self)
        self.passwd = {}
        self.rb_url = reviewboard_url
        self.rb_user = rb_user
        self.rb_pass = rb_pass
        self.api_token = api_token
        self.auth_callback = auth_callback
        self.otp_token_callback = otp_token_callback

    def find_user_password(self, realm, uri):
        if realm == b'Web API':
            if self.auth_callback:
                username, password = self.auth_callback(realm, uri, username=self.rb_user, password=self.rb_pass)
                self.rb_user = username
                self.rb_pass = password
            return (
             self.rb_user, self.rb_pass)
        else:
            return HTTPPasswordMgr.find_user_password(self, realm, uri)

    def get_otp_token(self, uri, method):
        if self.otp_token_callback:
            return self.otp_token_callback(uri, method)


def create_cookie_jar(cookie_file=None):
    """Return a cookie jar backed by cookie_file

    If cooie_file is not provided, we will default it. If the
    cookie_file does not exist, we will create it with the proper
    permissions.

    In the case where we default cookie_file, and it does not exist,
    we will attempt to copy the .post-review-cookies.txt file.
    """
    home_path = get_home_path()
    if not cookie_file:
        cookie_file = os.path.join(home_path, RBTOOLS_COOKIE_FILE)
        post_review_cookies = os.path.join(home_path, b'.post-review-cookies.txt')
        if not os.path.isfile(cookie_file) and os.path.isfile(post_review_cookies):
            try:
                shutil.copyfile(post_review_cookies, cookie_file)
                os.chmod(cookie_file, 384)
            except IOError as e:
                logging.warning(b"There was an error while copying post-review's cookies: %s", e)

    if not os.path.isfile(cookie_file):
        try:
            open(cookie_file, b'w').close()
            os.chmod(cookie_file, 384)
        except IOError as e:
            logging.warning(b'There was an error while creating a cookie file: %s', e)

    return (
     MozillaCookieJar(cookie_file), cookie_file)


class ReviewBoardServer(object):
    """Represents a Review Board server we are communicating with.

    Provides methods for executing HTTP requests on a Review Board
    server's Web API.

    The ``auth_callback`` parameter can be used to specify a callable
    which will be called when authentication fails. This callable will
    be passed the realm, and url of the Review Board server and should
    return a 2-tuple of username, password. The user can be prompted
    for their credentials using this mechanism.
    """

    def __init__(self, url, cookie_file=None, username=None, password=None, api_token=None, agent=None, session=None, disable_proxy=False, auth_callback=None, otp_token_callback=None, verify_ssl=True, save_cookies=True, ext_auth_cookies=None):
        if not url.endswith(b'/'):
            url += b'/'
        self.url = url + b'api/'
        self.save_cookies = save_cookies
        self.ext_auth_cookies = ext_auth_cookies
        if self.save_cookies:
            self.cookie_jar, self.cookie_file = create_cookie_jar(cookie_file=cookie_file)
            try:
                self.cookie_jar.load(ignore_expires=True)
            except IOError:
                pass

        else:
            self.cookie_jar = CookieJar()
            self.cookie_file = None
        if self.ext_auth_cookies:
            try:
                self.cookie_jar.load(ext_auth_cookies, ignore_expires=True)
            except IOError as e:
                logging.critical(b'There was an error while loading a cookie file: %s', e)

        parsed_url = urlparse(url)
        self.domain = parsed_url[1].partition(b':')[0]
        if self.domain.count(b'.') < 1:
            self.domain = b'%s.local' % self.domain
        if session:
            cookie = Cookie(version=0, name=RB_COOKIE_NAME, value=session, port=None, port_specified=False, domain=self.domain, domain_specified=True, domain_initial_dot=True, path=parsed_url[2], path_specified=True, secure=False, expires=None, discard=False, comment=None, comment_url=None, rest={b'HttpOnly': None})
            self.cookie_jar.set_cookie(cookie)
            if self.save_cookies:
                self.cookie_jar.save()
        if username:
            try:
                self.cookie_jar.clear(self.domain, parsed_url[2], RB_COOKIE_NAME)
            except KeyError:
                pass

        password_mgr = ReviewBoardHTTPPasswordMgr(self.url, username, password, api_token, auth_callback, otp_token_callback)
        self.preset_auth_handler = PresetHTTPAuthHandler(self.url, password_mgr)
        handlers = []
        if not verify_ssl:
            context = ssl._create_unverified_context()
            handlers.append(HTTPSHandler(context=context))
        if disable_proxy:
            handlers.append(ProxyHandler({}))
        handlers += [
         HTTPCookieProcessor(self.cookie_jar),
         ReviewBoardHTTPBasicAuthHandler(password_mgr),
         HTTPDigestAuthHandler(password_mgr),
         self.preset_auth_handler,
         ReviewBoardHTTPErrorProcessor()]
        if agent:
            self.agent = agent
        else:
            self.agent = (b'RBTools/' + get_package_version()).encode(b'utf-8')
        opener = build_opener(*handlers)
        opener.addheaders = [
         (
          b'User-agent', self.agent)]
        install_opener(opener)
        self._cache = None
        self._urlopen = urlopen
        return

    def enable_cache(self, cache_location=None, in_memory=False):
        """Enable caching for all future HTTP requests.

        The cache will be created at the default location if none is provided.

        If the in_memory parameter is True, the cache will be created in memory
        instead of on disk. This overrides the cache_location parameter.
        """
        if not self._cache:
            self._cache = APICache(create_db_in_memory=in_memory, db_location=cache_location)
            self._urlopen = self._cache.make_request

    def login(self, username, password):
        """Reset the user information"""
        self.preset_auth_handler.reset(username, password)

    def logout(self):
        """Logs the user out of the session."""
        self.preset_auth_handler.reset(None, None)
        self.make_request(HttpRequest(b'%ssession/' % self.url, method=b'DELETE'))
        self.cookie_jar.clear(self.domain)
        if self.save_cookies:
            self.cookie_jar.save()
        return

    def process_error(self, http_status, data):
        """Processes an error, raising an APIError with the information."""
        try:
            rsp = json_loads(data)
            assert rsp[b'stat'] == b'fail'
            logging.debug(b'Got API Error %d (HTTP code %d): %s' % (
             rsp[b'err'][b'code'], http_status, rsp[b'err'][b'msg']))
            logging.debug(b'Error data: %r' % rsp)
            raise create_api_error(http_status, rsp[b'err'][b'code'], rsp, rsp[b'err'][b'msg'])
        except ValueError:
            logging.debug(b'Got HTTP error: %s: %s' % (http_status, data))
            raise APIError(http_status, None, None, data)

        return

    def make_request(self, request):
        """Perform an http request.

        The request argument should be an instance of
        'rbtools.api.request.HttpRequest'.
        """
        try:
            content_type, body = request.encode_multipart_formdata()
            headers = request.headers
            if body:
                headers.update({b'Content-Type': content_type, 
                   b'Content-Length': str(len(body))})
            else:
                headers[b'Content-Length'] = b'0'
            r = Request(request.url.encode(b'utf-8'), body, headers, request.method.encode(b'utf-8'))
            rsp = self._urlopen(r)
        except HTTPError as e:
            self.process_error(e.code, e.read())
        except URLError as e:
            raise ServerInterfaceError(b'%s' % e.reason)

        if self.save_cookies:
            try:
                self.cookie_jar.save()
            except IOError:
                pass

        return rsp