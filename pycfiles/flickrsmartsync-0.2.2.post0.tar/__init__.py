# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/faisal/Developer/Projects/github/flickrsmartsync/flickrapi/__init__.py
# Compiled at: 2014-09-07 17:31:46
"""A FlickrAPI interface.

The main functionality can be found in the `flickrapi.FlickrAPI`
class.

See `the FlickrAPI homepage`_ for more info.

.. _`the FlickrAPI homepage`: http://stuvel.eu/projects/flickrapi
"""
__version__ = '1.4.4'
__all__ = ('FlickrAPI', 'IllegalArgumentException', 'FlickrError',
 'CancelUpload', 'XMLNode', 'set_log_level', '__version__')
__author__ = ('Sybren Stüvel').encode('utf-8')
import urllib, urllib2, os.path, logging, webbrowser
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from flickrapi.tokencache import TokenCache, SimpleTokenCache, LockingTokenCache
from flickrapi.xmlnode import XMLNode
from flickrapi.multipart import Part, Multipart, FilePart
from flickrapi.exceptions import IllegalArgumentException, FlickrError, CancelUpload
from flickrapi.cache import SimpleCache
from flickrapi import reportinghttp
logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

def make_utf8(dictionary):
    """Encodes all Unicode strings in the dictionary to UTF-8. Converts
    all other objects to regular strings.

    Returns a copy of the dictionary, doesn't touch the original.
    """
    result = {}
    for key, value in dictionary.iteritems():
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        else:
            value = str(value)
        result[key] = value

    return result


def debug(method):
    """Method decorator for debugging method calls.

    Using this automatically sets the log level to DEBUG.
    """
    LOG.setLevel(logging.DEBUG)

    def debugged(*args, **kwargs):
        LOG.debug('Call: %s(%s, %s)' % (method.__name__, args,
         kwargs))
        result = method(*args, **kwargs)
        LOG.debug('\tResult: %s' % result)
        return result

    return debugged


rest_parsers = {}

def rest_parser(format):
    """Method decorator, use this to mark a function as the parser for
    REST as returned by Flickr.
    """

    def decorate_parser(method):
        rest_parsers[format] = method
        return method

    return decorate_parser


def require_format(required_format):
    """Method decorator, raises a ValueError when the decorated method
    is called if the default format is not set to ``required_format``.
    """

    def decorator(method):

        def decorated(self, *args, **kwargs):
            if self.default_format == required_format:
                return method(self, *args, **kwargs)
            msg = 'Function %s requires that you use ElementTree ("etree") as the communication format, while the current format is set to "%s".'
            raise ValueError(msg % (method.func_name, self.default_format))

        return decorated

    return decorator


class FlickrAPI(object):
    """Encapsulates Flickr functionality.

    Example usage::

      flickr = flickrapi.FlickrAPI(api_key)
      photos = flickr.photos_search(user_id='73509078@N00', per_page='10')
      sets = flickr.photosets_getList(user_id='73509078@N00')
    """
    flickr_host = 'api.flickr.com'
    flickr_rest_form = '/services/rest/'
    flickr_auth_form = '/services/auth/'
    flickr_upload_form = '/services/upload/'
    flickr_replace_form = '/services/replace/'

    def __init__(self, api_key, secret=None, username=None, token=None, format='etree', store_token=True, cache=False):
        """Construct a new FlickrAPI instance for a given API key
        and secret.

        api_key
            The API key as obtained from Flickr.

        secret
            The secret belonging to the API key.

        username
            Used to identify the appropriate authentication token for a
            certain user.

        token
            If you already have an authentication token, you can give
            it here. It won't be stored on disk by the FlickrAPI instance.

        format
            The response format. Use either "xmlnode" or "etree" to get a
            parsed response, or use any response format supported by Flickr
            to get an unparsed response from method calls. It's also possible
            to pass the ``format`` parameter on individual calls.

        store_token
            Disables the on-disk token cache if set to False (default is True).
            Use this to ensure that tokens aren't read nor written to disk, for
            example in web applications that store tokens in cookies.

        cache
            Enables in-memory caching of FlickrAPI calls - set to ``True`` to
            use. If you don't want to use the default settings, you can
            instantiate a cache yourself too:

            >>> f = FlickrAPI(api_key='123')
            >>> f.cache = SimpleCache(timeout=5, max_entries=100)
        """
        self.api_key = api_key
        self.secret = secret
        self.default_format = format
        self.__handler_cache = {}
        if token:
            self.token_cache = SimpleTokenCache()
            self.token_cache.token = token
        elif not store_token:
            self.token_cache = SimpleTokenCache()
        else:
            self.token_cache = TokenCache(api_key, username)
        if cache:
            self.cache = SimpleCache()
        else:
            self.cache = None
        return

    def __repr__(self):
        """Returns a string representation of this object."""
        return '[FlickrAPI for key "%s"]' % self.api_key

    __str__ = __repr__

    def trait_names(self):
        """Returns a list of method names as supported by the Flickr
        API. Used for tab completion in IPython.
        """
        try:
            rsp = self.reflection_getMethods(format='etree')
        except FlickrError:
            return

        def tr(name):
            """Translates Flickr names to something that can be called
            here.

            >>> tr(u'flickr.photos.getInfo')
            u'photos_getInfo'
            """
            return name[7:].replace('.', '_')

        return [ tr(m.text) for m in rsp.getiterator('method') ]

    @rest_parser('xmlnode')
    def parse_xmlnode(self, rest_xml):
        """Parses a REST XML response from Flickr into an XMLNode object."""
        rsp = XMLNode.parse(rest_xml, store_xml=True)
        if rsp['stat'] == 'ok':
            return rsp
        err = rsp.err[0]
        raise FlickrError('Error: %(code)s: %(msg)s' % err)

    @rest_parser('etree')
    def parse_etree(self, rest_xml):
        """Parses a REST XML response from Flickr into
           an ElementTree object."""
        try:
            import xml.etree.ElementTree as ElementTree
        except ImportError:
            try:
                import elementtree.ElementTree as ElementTree
            except ImportError:
                raise ImportError('You need to install ElementTree for using the etree format')

        rsp = ElementTree.fromstring(rest_xml)
        if rsp.attrib['stat'] == 'ok':
            return rsp
        err = rsp.find('err')
        raise FlickrError('Error: %(code)s: %(msg)s' % err.attrib)

    def sign(self, dictionary):
        """Calculate the flickr signature for a set of params.

        data
            a hash of all the params and values to be hashed, e.g.
            ``{"api_key":"AAAA", "auth_token":"TTTT", "key":
            u"value".encode('utf-8')}``

        """
        data = [
         self.secret]
        for key in sorted(dictionary.keys()):
            data.append(key)
            datum = dictionary[key]
            if isinstance(datum, unicode):
                raise IllegalArgumentException('No Unicode allowed, argument %s (%r) should have been UTF-8 by now' % (
                 key, datum))
            data.append(datum)

        md5_hash = md5(('').join(data))
        return md5_hash.hexdigest()

    def encode_and_sign(self, dictionary):
        """URL encodes the data in the dictionary, and signs it using the
        given secret, if a secret was given.
        """
        dictionary = make_utf8(dictionary)
        if self.secret:
            dictionary['api_sig'] = self.sign(dictionary)
        return urllib.urlencode(dictionary)

    def __getattr__(self, attrib):
        """Handle all the regular Flickr API calls.

        Example::

            flickr.auth_getFrob(api_key="AAAAAA")
            etree = flickr.photos_getInfo(photo_id='1234')
            etree = flickr.photos_getInfo(photo_id='1234', format='etree')
            xmlnode = flickr.photos_getInfo(photo_id='1234', format='xmlnode')
            json = flickr.photos_getInfo(photo_id='1234', format='json')
        """
        if attrib.startswith('_'):
            raise AttributeError("No such attribute '%s'" % attrib)
        method = 'flickr.' + attrib.replace('_', '.')
        if method in self.__handler_cache:
            return self.__handler_cache[method]

        def handler(**args):
            """Dynamically created handler for a Flickr API call"""
            if self.token_cache.token and not self.secret:
                raise ValueError('Auth tokens cannot be used without API secret')
            defaults = {'method': method, 'auth_token': self.token_cache.token, 
               'api_key': self.api_key, 
               'format': self.default_format}
            args = self.__supply_defaults(args, defaults)
            return self.__wrap_in_parser(self.__flickr_call, parse_format=args['format'], **args)

        handler.method = method
        self.__handler_cache[method] = handler
        return handler

    def __supply_defaults(self, args, defaults):
        """Returns a new dictionary containing ``args``, augmented with defaults
        from ``defaults``.

        Defaults can be overridden, or completely removed by setting the
        appropriate value in ``args`` to ``None``.

        >>> f = FlickrAPI('123')
        >>> f._FlickrAPI__supply_defaults(
        ...  {'foo': 'bar', 'baz': None, 'token': None},
        ...  {'baz': 'foobar', 'room': 'door'})
        {'foo': 'bar', 'room': 'door'}
        """
        result = args.copy()
        for key, default_value in defaults.iteritems():
            if key not in args:
                result[key] = default_value

        for key, value in result.copy().iteritems():
            if result[key] is None:
                del result[key]

        return result

    def __flickr_call(self, **kwargs):
        """Performs a Flickr API call with the given arguments. The method name
        itself should be passed as the 'method' parameter.

        Returns the unparsed data from Flickr::

            data = self.__flickr_call(method='flickr.photos.getInfo',
                photo_id='123', format='rest')
        """
        LOG.debug('Calling %s' % kwargs)
        post_data = self.encode_and_sign(kwargs)
        if self.cache and self.cache.get(post_data):
            return self.cache.get(post_data)
        else:
            url = 'https://' + self.flickr_host + self.flickr_rest_form
            flicksocket = urllib2.urlopen(url, post_data)
            reply = flicksocket.read()
            flicksocket.close()
            if self.cache is not None:
                self.cache.set(post_data, reply)
            return reply

    def __wrap_in_parser(self, wrapped_method, parse_format, *args, **kwargs):
        """Wraps a method call in a parser.

        The parser will be looked up by the ``parse_format`` specifier. If
        there is a parser and ``kwargs['format']`` is set, it's set to
        ``rest``, and the response of the method is parsed before it's
        returned.
        """
        if parse_format in rest_parsers and 'format' in kwargs:
            kwargs['format'] = 'rest'
        LOG.debug('Wrapping call %s(self, %s, %s)' % (wrapped_method, args,
         kwargs))
        data = wrapped_method(*args, **kwargs)
        if parse_format not in rest_parsers:
            return data
        parser = rest_parsers[parse_format]
        return parser(self, data)

    def auth_url(self, perms, frob):
        """Return the authorization URL to get a token.

        This is the URL the app will launch a browser toward if it
        needs a new token.

        perms
            "read", "write", or "delete"
        frob
            picked up from an earlier call to FlickrAPI.auth_getFrob()

        """
        encoded = self.encode_and_sign({'api_key': self.api_key, 'frob': frob, 
           'perms': perms})
        return 'https://%s%s?%s' % (self.flickr_host,
         self.flickr_auth_form, encoded)

    def web_login_url(self, perms):
        """Returns the web login URL to forward web users to.

        perms
            "read", "write", or "delete"
        """
        encoded = self.encode_and_sign({'api_key': self.api_key, 'perms': perms})
        return 'https://%s%s?%s' % (self.flickr_host,
         self.flickr_auth_form, encoded)

    def __extract_upload_response_format(self, kwargs):
        """Returns the response format given in kwargs['format'], or
        the default format if there is no such key.

        If kwargs contains 'format', it is removed from kwargs.

        If the format isn't compatible with Flickr's upload response
        type, a FlickrError exception is raised.
        """
        format = kwargs.get('format', self.default_format)
        if format not in rest_parsers and format != 'rest':
            raise FlickrError('Format %s not supported for uploading photos' % format)
        if 'format' in kwargs:
            del kwargs['format']
        return format

    def upload(self, filename, callback=None, **kwargs):
        """Upload a file to flickr.

        Be extra careful you spell the parameters correctly, or you will
        get a rather cryptic "Invalid Signature" error on the upload!

        Supported parameters:

        filename
            name of a file to upload
        callback
            method that gets progress reports
        title
            title of the photo
        description
            description a.k.a. caption of the photo
        tags
            space-delimited list of tags, ``'''tag1 tag2 "long
            tag"'''``
        is_public
            "1" or "0" for a public resp. private photo
        is_friend
            "1" or "0" whether friends can see the photo while it's
            marked as private
        is_family
            "1" or "0" whether family can see the photo while it's
            marked as private
        content_type
            Set to "1" for Photo, "2" for Screenshot, or "3" for Other.
        hidden
            Set to "1" to keep the photo in global search results, "2"
            to hide from public searches.
        format
            The response format. You can only choose between the
            parsed responses or 'rest' for plain REST.

        The callback method should take two parameters:
        ``def callback(progress, done)``

        Progress is a number between 0 and 100, and done is a boolean
        that's true only when the upload is done.
        """
        return self.__upload_to_form(self.flickr_upload_form, filename, callback, **kwargs)

    def replace(self, filename, photo_id, callback=None, **kwargs):
        """Replace an existing photo.

        Supported parameters:

        filename
            name of a file to upload
        photo_id
            the ID of the photo to replace
        callback
            method that gets progress reports
        format
            The response format. You can only choose between the
            parsed responses or 'rest' for plain REST. Defaults to the
            format passed to the constructor.

        The callback parameter has the same semantics as described in the
        ``upload`` function.
        """
        if not photo_id:
            raise IllegalArgumentException('photo_id must be specified')
        kwargs['photo_id'] = photo_id
        return self.__upload_to_form(self.flickr_replace_form, filename, callback, **kwargs)

    def __upload_to_form(self, form_url, filename, callback, **kwargs):
        """Uploads a photo - can be used to either upload a new photo
        or replace an existing one.

        form_url must be either ``FlickrAPI.flickr_replace_form`` or
        ``FlickrAPI.flickr_upload_form``.
        """
        if not filename:
            raise IllegalArgumentException('filename must be specified')
        if not self.token_cache.token:
            raise IllegalArgumentException('Authentication is required')
        format = self.__extract_upload_response_format(kwargs)
        arguments = {'auth_token': self.token_cache.token, 'api_key': self.api_key}
        arguments.update(kwargs)
        kwargs = make_utf8(arguments)
        if self.secret:
            kwargs['api_sig'] = self.sign(kwargs)
        url = 'https://%s%s' % (self.flickr_host, form_url)
        body = Multipart()
        for arg, value in kwargs.iteritems():
            part = Part({'name': arg}, value)
            body.attach(part)

        filepart = FilePart({'name': 'photo'}, filename, 'image/jpeg')
        body.attach(filepart)
        return self.__wrap_in_parser(self.__send_multipart, format, url, body, callback)

    def __send_multipart(self, url, body, progress_callback=None):
        """Sends a Multipart object to an URL.

        Returns the resulting unparsed XML from Flickr.
        """
        LOG.debug('Uploading to %s' % url)
        request = urllib2.Request(url)
        request.add_data(str(body))
        header, value = body.header()
        request.add_header(header, value)
        if not progress_callback:
            response = urllib2.urlopen(request)
            return response.read()

        def __upload_callback(percentage, done, seen_header=[False]):
            """Filters out the progress report on the HTTP header"""
            if seen_header[0]:
                return progress_callback(percentage, done)
            if done:
                seen_header[0] = True

        response = reportinghttp.urlopen(request, __upload_callback)
        return response.read()

    def validate_frob(self, frob, perms):
        """Lets the user validate the frob by launching a browser to
        the Flickr website.
        """
        auth_url = self.auth_url(perms, frob)
        try:
            browser = webbrowser.get()
        except webbrowser.Error:
            if 'BROWSER' not in os.environ:
                print 'Please authorize: %s' % auth_url
                return
            browser = webbrowser.GenericBrowser(os.environ['BROWSER'])

        browser.open(auth_url, True, True)

    def get_token_part_one(self, perms='read', auth_callback=None):
        """Get a token either from the cache, or make a new one from
        the frob.

        This first attempts to find a token in the user's token cache
        on disk. If that token is present and valid, it is returned by
        the method.

        If that fails (or if the token is no longer valid based on
        flickr.auth.checkToken) a new frob is acquired. If an auth_callback
        method has been specified it will be called. Otherwise the frob is
        validated by having the user log into flickr (with a browser).

        To get a proper token, follow these steps:
            - Store the result value of this method call
            - Give the user a way to signal the program that he/she
              has authorized it, for example show a button that can be
              pressed.
            - Wait for the user to signal the program that the
              authorization was performed, but only if there was no
              cached token.
            - Call flickrapi.get_token_part_two(...) and pass it the
              result value you stored.

        The newly minted token is then cached locally for the next
        run.

        perms
            "read", "write", or "delete"
        auth_callback
            method to be called if authorization is needed. When not
            passed, ``self.validate_frob(...)`` is called. You can
            call this method yourself from the callback method too.

            If authorization should be blocked, pass
            ``auth_callback=False``.

            The auth_callback method should take ``(frob, perms)`` as
            parameters.

        An example::

            (token, frob) = flickr.get_token_part_one(perms='write')
            if not token:
                raw_input("Press ENTER after you authorized this program")
            flickr.get_token_part_two((token, frob))

        Also take a look at ``authenticate_console(perms)``.
        """
        authenticate = self.validate_frob
        if auth_callback is not None:
            if hasattr(auth_callback, '__call__'):
                authenticate = auth_callback
            elif auth_callback is False:
                authenticate = None
            else:
                raise ValueError('Invalid value for auth_callback: %s' % auth_callback)
        token = self.token_cache.token
        frob = None
        if token:
            LOG.debug("Trying cached token '%s'" % token)
            try:
                rsp = self.auth_checkToken(auth_token=token, format='xmlnode')
                tokenPerms = rsp.auth[0].perms[0].text
                if tokenPerms == 'read' and perms != 'read':
                    token = None
                elif tokenPerms == 'write' and perms == 'delete':
                    token = None
            except FlickrError:
                LOG.debug('Cached token invalid')
                self.token_cache.forget()
                token = None

        if not token:
            if not authenticate:
                raise FlickrError('Authentication required but blocked using auth_callback=False')
            LOG.debug('Getting frob for new token')
            rsp = self.auth_getFrob(auth_token=None, format='xmlnode')
            frob = rsp.frob[0].text
            authenticate(frob, perms)
        return (token, frob)

    def get_token_part_two(self, (token, frob)):
        """Part two of getting a token,
           see ``get_token_part_one(...)`` for details."""
        if token:
            LOG.debug('get_token_part_two: no need, token already there')
            self.token_cache.token = token
            return token
        LOG.debug("get_token_part_two: getting a new token for frob '%s'" % frob)
        return self.get_token(frob)

    def get_token(self, frob):
        """Gets the token given a certain frob. Used by ``get_token_part_two`` and
        by the web authentication method.
        """
        rsp = self.auth_getToken(frob=frob, auth_token=None, format='xmlnode')
        token = rsp.auth[0].token[0].text
        LOG.debug("get_token: new token '%s'" % token)
        self.token_cache.token = token
        return token

    def authenticate_console(self, perms='read', auth_callback=None):
        """Performs the authentication, assuming a console program.

        Gets the token, if needed starts the browser and waits for the user to
        press ENTER before continuing.

        See ``get_token_part_one(...)`` for an explanation of the
        parameters.
        """
        token, frob = self.get_token_part_one(perms, auth_callback)
        if not token:
            raw_input('Press ENTER after you authorized this program')
        self.get_token_part_two((token, frob))

    @require_format('etree')
    def __data_walker(self, method, **params):
        """Calls 'method' with page=0, page=1 etc. until the total
        number of pages has been visited. Yields the photos
        returned.

        Assumes that ``method(page=n, **params).findall('*/photos')``
        results in a list of photos, and that the toplevel element of
        the result contains a 'pages' attribute with the total number
        of pages.
        """
        page = 1
        total = 1
        while page <= total:
            LOG.debug('Calling %s(page=%i of %i, %s)' % (
             method.func_name, page, total, params))
            rsp = method(page=page, **params)
            photoset = rsp.getchildren()[0]
            total = int(photoset.get('pages'))
            photos = rsp.findall('*/photo')
            for photo in photos:
                yield photo

            page += 1

    @require_format('etree')
    def walk_set(self, photoset_id, per_page=50, **kwargs):
        """walk_set(self, photoset_id, per_page=50, ...) ->                 generator, yields each photo in a single set.

        :Parameters:
            photoset_id
                the photoset ID
            per_page
                the number of photos that are fetched in one call to
                Flickr.

        Other arguments can be passed, as documented in the
        flickr.photosets.getPhotos_ API call in the Flickr API
        documentation, except for ``page`` because all pages will be
        returned eventually.

        .. _flickr.photosets.getPhotos:
            http://www.flickr.com/services/api/flickr.photosets.getPhotos.html

        Uses the ElementTree format, incompatible with other formats.
        """
        return self.__data_walker(self.photosets_getPhotos, photoset_id=photoset_id, per_page=per_page, **kwargs)

    @require_format('etree')
    def walk(self, per_page=50, **kwargs):
        """walk(self, user_id=..., tags=..., ...) -> generator,                 yields each photo in a search query result

        Accepts the same parameters as flickr.photos.search_ API call,
        except for ``page`` because all pages will be returned
        eventually.

        .. _flickr.photos.search:
            http://www.flickr.com/services/api/flickr.photos.search.html

        Also see `walk_set`.
        """
        return self.__data_walker(self.photos_search, per_page=per_page, **kwargs)


def set_log_level(level):
    """Sets the log level of the logger used by the FlickrAPI module.

    >>> import flickrapi
    >>> import logging
    >>> flickrapi.set_log_level(logging.INFO)
    """
    import flickrapi.tokencache
    LOG.setLevel(level)
    flickrapi.tokencache.LOG.setLevel(level)


if __name__ == '__main__':
    print 'Running doctests'
    import doctest
    doctest.testmod()
    print 'Tests OK'