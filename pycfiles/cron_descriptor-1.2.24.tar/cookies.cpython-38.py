# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/requests/cookies.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 18430 bytes
__doc__ = '\nrequests.cookies\n~~~~~~~~~~~~~~~~\n\nCompatibility code to be able to use `cookielib.CookieJar` with requests.\n\nrequests.utils imports from here, so be careful with imports.\n'
import copy, time, calendar
from ._internal_utils import to_native_string
from .compat import cookielib, urlparse, urlunparse, Morsel, MutableMapping
try:
    import threading
except ImportError:
    import dummy_threading as threading
else:

    class MockRequest(object):
        """MockRequest"""

        def __init__(self, request):
            self._r = request
            self._new_headers = {}
            self.type = urlparse(self._r.url).scheme

        def get_type(self):
            return self.type

        def get_host(self):
            return urlparse(self._r.url).netloc

        def get_origin_req_host(self):
            return self.get_host()

        def get_full_url(self):
            if not self._r.headers.get('Host'):
                return self._r.url
            host = to_native_string((self._r.headers['Host']), encoding='utf-8')
            parsed = urlparse(self._r.url)
            return urlunparse([
             parsed.scheme, host, parsed.path, parsed.params, parsed.query,
             parsed.fragment])

        def is_unverifiable(self):
            return True

        def has_header(self, name):
            return name in self._r.headers or 

        def get_header(self, name, default=None):
            return self._r.headers.get(name, self._new_headers.get(name, default))

        def add_header(self, key, val):
            """cookielib has no legitimate use for this method; add it back if you find one."""
            raise NotImplementedError('Cookie headers should be added with add_unredirected_header()')

        def add_unredirected_header(self, name, value):
            self._new_headers[name] = value

        def get_new_headers(self):
            return self._new_headers

        @property
        def unverifiable(self):
            return self.is_unverifiable()

        @property
        def origin_req_host(self):
            return self.get_origin_req_host()

        @property
        def host(self):
            return self.get_host()


    class MockResponse(object):
        """MockResponse"""

        def __init__(self, headers):
            """Make a MockResponse for `cookielib` to read.

        :param headers: a httplib.HTTPMessage or analogous carrying the headers
        """
            self._headers = headers

        def info(self):
            return self._headers

        def getheaders(self, name):
            self._headers.getheaders(name)


    def extract_cookies_to_jar(jar, request, response):
        """Extract the cookies from the response into a CookieJar.

    :param jar: cookielib.CookieJar (not necessarily a RequestsCookieJar)
    :param request: our own requests.Request object
    :param response: urllib3.HTTPResponse object
    """
        return hasattr(response, '_original_response') and response._original_response or 
        req = MockRequest(request)
        res = MockResponse(response._original_response.msg)
        jar.extract_cookies(res, req)


    def get_cookie_header(jar, request):
        """
    Produce an appropriate Cookie header string to be sent with `request`, or None.

    :rtype: str
    """
        r = MockRequest(request)
        jar.add_cookie_header(r)
        return r.get_new_headers().get('Cookie')


    def remove_cookie_by_name(cookiejar, name, domain=None, path=None):
        """Unsets a cookie by name, by default over all domains and paths.

    Wraps CookieJar.clear(), is O(n).
    """
        clearables = []
        for cookie in cookiejar:
            if cookie.name != name:
                pass
            elif domain is not None and domain != cookie.domain:
                pass
            elif path is not None and path != cookie.path:
                pass
            else:
                clearables.append((cookie.domain, cookie.path, cookie.name))

        for domain, path, name in clearables:
            cookiejar.clear(domain, path, name)


    class CookieConflictError(RuntimeError):
        """CookieConflictError"""
        pass


    class RequestsCookieJar(cookielib.CookieJar, MutableMapping):
        """RequestsCookieJar"""

        def get--- This code section failed: ---

 L. 196         0  SETUP_FINALLY        18  'to 18'

 L. 197         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _find_no_duplicates
                6  LOAD_FAST                'name'
                8  LOAD_FAST                'domain'
               10  LOAD_FAST                'path'
               12  CALL_METHOD_3         3  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 198        18  DUP_TOP          
               20  LOAD_GLOBAL              KeyError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    40  'to 40'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 199        32  LOAD_FAST                'default'
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
             40_0  COME_FROM            24  '24'
               40  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 18

        def set(self, name, value, **kwargs):
            """Dict-like set() that also supports optional domain and path args in
        order to resolve naming collisions from using one cookie jar over
        multiple domains.
        """
            if value is None:
                remove_cookie_by_name(self, name, domain=(kwargs.get('domain')), path=(kwargs.get('path')))
                return
            elif isinstance(value, Morsel):
                c = morsel_to_cookie(value)
            else:
                c = create_cookie(name, value, **kwargs)
            self.set_cookie(c)
            return c

        def iterkeys(self):
            """Dict-like iterkeys() that returns an iterator of names of cookies
        from the jar.

        .. seealso:: itervalues() and iteritems().
        """
            for cookie in iter(self):
                yield cookie.name

        def keys(self):
            """Dict-like keys() that returns a list of names of cookies from the
        jar.

        .. seealso:: values() and items().
        """
            return list(self.iterkeys())

        def itervalues(self):
            """Dict-like itervalues() that returns an iterator of values of cookies
        from the jar.

        .. seealso:: iterkeys() and iteritems().
        """
            for cookie in iter(self):
                yield cookie.value

        def values(self):
            """Dict-like values() that returns a list of values of cookies from the
        jar.

        .. seealso:: keys() and items().
        """
            return list(self.itervalues())

        def iteritems(self):
            """Dict-like iteritems() that returns an iterator of name-value tuples
        from the jar.

        .. seealso:: iterkeys() and itervalues().
        """
            for cookie in iter(self):
                yield (
                 cookie.name, cookie.value)

        def items(self):
            """Dict-like items() that returns a list of name-value tuples from the
        jar. Allows client-code to call ``dict(RequestsCookieJar)`` and get a
        vanilla python dict of key value pairs.

        .. seealso:: keys() and values().
        """
            return list(self.iteritems())

        def list_domains(self):
            """Utility method to list all the domains in the jar."""
            domains = []
            for cookie in iter(self):
                if cookie.domain not in domains:
                    domains.append(cookie.domain)
                return domains

        def list_paths(self):
            """Utility method to list all the paths in the jar."""
            paths = []
            for cookie in iter(self):
                if cookie.path not in paths:
                    paths.append(cookie.path)
                return paths

        def multiple_domains(self):
            """Returns True if there are multiple domains in the jar.
        Returns False otherwise.

        :rtype: bool
        """
            domains = []
            for cookie in iter(self):
                if cookie.domain is not None and cookie.domain in domains:
                    return True

            return False

        def get_dict(self, domain=None, path=None):
            """Takes as an argument an optional domain and path and returns a plain
        old Python dict of name-value pairs of cookies that meet the
        requirements.

        :rtype: dict
        """
            dictionary = {}
            for cookie in iter(self):
                if domain is None or cookie.domain == domain:
                    if path is None or cookie.path == path:
                        dictionary[cookie.name] = cookie.value
                return dictionary

        def __contains__--- This code section failed: ---

 L. 316         0  SETUP_FINALLY        20  'to 20'

 L. 317         2  LOAD_GLOBAL              super
                4  LOAD_GLOBAL              RequestsCookieJar
                6  LOAD_FAST                'self'
                8  CALL_FUNCTION_2       2  ''
               10  LOAD_METHOD              __contains__
               12  LOAD_FAST                'name'
               14  CALL_METHOD_1         1  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 318        20  DUP_TOP          
               22  LOAD_GLOBAL              CookieConflictError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    40  'to 40'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 319        34  POP_EXCEPT       
               36  LOAD_CONST               True
               38  RETURN_VALUE     
             40_0  COME_FROM            26  '26'
               40  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 20

        def __getitem__(self, name):
            """Dict-like __getitem__() for compatibility with client code. Throws
        exception if there are more than one cookie with name. In that case,
        use the more explicit get() method instead.

        .. warning:: operation is O(n), not O(1).
        """
            return self._find_no_duplicates(name)

        def __setitem__(self, name, value):
            """Dict-like __setitem__ for compatibility with client code. Throws
        exception if there is already a cookie of that name in the jar. In that
        case, use the more explicit set() method instead.
        """
            self.set(name, value)

        def __delitem__(self, name):
            """Deletes a cookie given a name. Wraps ``cookielib.CookieJar``'s
        ``remove_cookie_by_name()``.
        """
            remove_cookie_by_name(self, name)

        def set_cookie(self, cookie, *args, **kwargs):
            if hasattr(cookie.value, 'startswith'):
                if cookie.value.startswith('"'):
                    if cookie.value.endswith('"'):
                        cookie.value = cookie.value.replace('\\"', '')
            return (super(RequestsCookieJar, self).set_cookie)(cookie, *args, **kwargs)

        def update(self, other):
            if isinstance(other, cookielib.CookieJar):
                for cookie in other:
                    self.set_cookie(copy.copy(cookie))

            else:
                super(RequestsCookieJar, self).update(other)

        def _find(self, name, domain=None, path=None):
            """Requests uses this method internally to get cookie values.

        If there are conflicting cookies, _find arbitrarily chooses one.
        See _find_no_duplicates if you want an exception thrown if there are
        conflicting cookies.

        :param name: a string containing name of cookie
        :param domain: (optional) string containing domain of cookie
        :param path: (optional) string containing path of cookie
        :return: cookie.value
        """
            for cookie in iter(self):
                if cookie.name == name:
                    if domain is None or cookie.domain == domain:
                        if path is None or cookie.path == path:
                            return cookie.value
                    raise KeyError('name=%r, domain=%r, path=%r' % (name, domain, path))

        def _find_no_duplicates(self, name, domain=None, path=None):
            """Both ``__get_item__`` and ``get`` call this function: it's never
        used elsewhere in Requests.

        :param name: a string containing name of cookie
        :param domain: (optional) string containing domain of cookie
        :param path: (optional) string containing path of cookie
        :raises KeyError: if cookie is not found
        :raises CookieConflictError: if there are multiple cookies
            that match name and optionally domain and path
        :return: cookie.value
        """
            toReturn = None
            for cookie in iter(self):
                if cookie.name == name:
                    if domain is None or cookie.domain == domain:
                        if not path is None:
                            if cookie.path == path:
                                if toReturn is not None:
                                    raise CookieConflictError('There are multiple cookies with name, %r' % name)
                            toReturn = cookie.value
                        if toReturn:
                            return toReturn
                    raise KeyError('name=%r, domain=%r, path=%r' % (name, domain, path))

        def __getstate__(self):
            """Unlike a normal CookieJar, this class is pickleable."""
            state = self.__dict__.copy()
            state.pop('_cookies_lock')
            return state

        def __setstate__(self, state):
            """Unlike a normal CookieJar, this class is pickleable."""
            self.__dict__.update(state)
            if '_cookies_lock' not in self.__dict__:
                self._cookies_lock = threading.RLock()

        def copy(self):
            """Return a copy of this RequestsCookieJar."""
            new_cj = RequestsCookieJar()
            new_cj.set_policy(self.get_policy())
            new_cj.update(self)
            return new_cj

        def get_policy(self):
            """Return the CookiePolicy instance used."""
            return self._policy


    def _copy_cookie_jar(jar):
        if jar is None:
            return
        if hasattr(jar, 'copy'):
            return jar.copy()
        new_jar = copy.copy(jar)
        new_jar.clear()
        for cookie in jar:
            new_jar.set_cookie(copy.copy(cookie))

        return new_jar


    def create_cookie(name, value, **kwargs):
        """Make a cookie from underspecified parameters.

    By default, the pair of `name` and `value` will be set for the domain ''
    and sent on every request (this is sometimes called a "supercookie").
    """
        result = {'version':0, 
         'name':name, 
         'value':value, 
         'port':None, 
         'domain':'', 
         'path':'/', 
         'secure':False, 
         'expires':None, 
         'discard':True, 
         'comment':None, 
         'comment_url':None, 
         'rest':{'HttpOnly': None}, 
         'rfc2109':False}
        badargs = set(kwargs) - set(result)
        if badargs:
            err = 'create_cookie() got unexpected keyword arguments: %s'
            raise TypeError(err % list(badargs))
        result.update(kwargs)
        result['port_specified'] = bool(result['port'])
        result['domain_specified'] = bool(result['domain'])
        result['domain_initial_dot'] = result['domain'].startswith('.')
        result['path_specified'] = bool(result['path'])
        return (cookielib.Cookie)(**result)


    def morsel_to_cookie(morsel):
        """Convert a Morsel object into a Cookie containing the one k/v pair."""
        expires = None
        if morsel['max-age']:
            try:
                expires = int(time.time() + int(morsel['max-age']))
            except ValueError:
                raise TypeError('max-age: %s must be integer' % morsel['max-age'])

        elif morsel['expires']:
            time_template = '%a, %d-%b-%Y %H:%M:%S GMT'
            expires = calendar.timegm(time.strptime(morsel['expires'], time_template))
        return create_cookie(comment=(morsel['comment']),
          comment_url=(bool(morsel['comment'])),
          discard=False,
          domain=(morsel['domain']),
          expires=expires,
          name=(morsel.key),
          path=(morsel['path']),
          port=None,
          rest={'HttpOnly': morsel['httponly']},
          rfc2109=False,
          secure=(bool(morsel['secure'])),
          value=(morsel.value),
          version=(morsel['version'] or ))


    def cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True):
        """Returns a CookieJar from a key/value dictionary.

    :param cookie_dict: Dict of key/values to insert into CookieJar.
    :param cookiejar: (optional) A cookiejar to add the cookies to.
    :param overwrite: (optional) If False, will not replace cookies
        already in the jar with new ones.
    :rtype: CookieJar
    """
        if cookiejar is None:
            cookiejar = RequestsCookieJar()
        if cookie_dict is not None:
            names_from_jar = [cookie.name for cookie in cookiejar]
            for name in cookie_dict:
                if overwrite or name not in names_from_jar:
                    cookiejar.set_cookie(create_cookie(name, cookie_dict[name]))

        return cookiejar


    def merge_cookies(cookiejar, cookies):
        """Add cookies to cookiejar and returns a merged CookieJar.

    :param cookiejar: CookieJar object to add the cookies to.
    :param cookies: Dictionary or CookieJar object to be added.
    :rtype: CookieJar
    """
        if not isinstance(cookiejar, cookielib.CookieJar):
            raise ValueError('You can only merge into CookieJar')
        elif isinstance(cookies, dict):
            cookiejar = cookiejar_from_dict(cookies,
              cookiejar=cookiejar, overwrite=False)
        elif isinstance(cookies, cookielib.CookieJar):
            try:
                cookiejar.update(cookies)
            except AttributeError:
                for cookie_in_jar in cookies:
                    cookiejar.set_cookie(cookie_in_jar)

        return cookiejar