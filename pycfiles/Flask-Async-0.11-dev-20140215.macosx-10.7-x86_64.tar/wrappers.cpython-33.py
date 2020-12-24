# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/werkzeug/wrappers.py
# Compiled at: 2014-01-20 15:46:16
# Size of source mod 2**32: 76207 bytes
"""
    werkzeug.wrappers
    ~~~~~~~~~~~~~~~~~

    The wrappers are simple request and response objects which you can
    subclass to do whatever you want them to do.  The request object contains
    the information transmitted by the client (webbrowser) and the response
    object contains all the information sent back to the browser.

    An important detail is that the request object is created with the WSGI
    environ and will act as high-level proxy whereas the response object is an
    actual WSGI application.

    Like everything else in Werkzeug these objects will work correctly with
    unicode data.  Incoming form data parsed by the response object will be
    decoded into an unicode object if possible and if it makes sense.

    :copyright: (c) 2013 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from functools import update_wrapper
from datetime import datetime, timedelta
from werkzeug.http import HTTP_STATUS_CODES, parse_accept_header, parse_cache_control_header, parse_etags, parse_date, generate_etag, is_resource_modified, unquote_etag, quote_etag, parse_set_header, parse_authorization_header, parse_www_authenticate_header, remove_entity_headers, parse_options_header, dump_options_header, http_date, parse_if_range_header, parse_cookie, dump_cookie, parse_range_header, parse_content_range_header, dump_header
from werkzeug.urls import url_decode, iri_to_uri, url_join
from werkzeug.formparser import FormDataParser, default_stream_factory
from werkzeug.utils import cached_property, environ_property, header_property, get_content_type, yields, call_maybe_yield
from werkzeug.wsgi import get_current_url, get_host, ClosingIterator, get_input_stream, get_content_length
from werkzeug.datastructures import MultiDict, CombinedMultiDict, Headers, EnvironHeaders, ImmutableMultiDict, ImmutableTypeConversionDict, ImmutableList, MIMEAccept, CharsetAccept, LanguageAccept, ResponseCacheControl, RequestCacheControl, CallbackDict, ContentRange, iter_multi_items
from werkzeug._internal import _get_environ
from werkzeug._compat import to_bytes, string_types, text_type, integer_types, wsgi_decoding_dance, wsgi_get_bytes, to_unicode, to_native, BytesIO

def _run_wsgi_app(*args):
    """This function replaces itself to ensure that the test module is not
    imported unless required.  DO NOT USE!
    """
    global _run_wsgi_app
    from werkzeug.test import run_wsgi_app as _run_wsgi_app
    return _run_wsgi_app(*args)


def _warn_if_string(iterable):
    """Helper for the response objects to check if the iterable returned
    to the WSGI server is not a string.
    """
    if isinstance(iterable, string_types):
        from warnings import warn
        warn(Warning('response iterable was set to a string.  This appears to work but means that the server will send the data to the client char, by char.  This is almost never intended behavior, use response.data to assign strings to the response object.'), stacklevel=2)


def _assert_not_shallow(request):
    if request.shallow:
        raise RuntimeError('A shallow request tried to consume form data.  If you really want to do that, set `shallow` to False.')


def _iter_encoded(iterable, charset):
    for item in iterable:
        if isinstance(item, text_type):
            yield item.encode(charset)
        else:
            yield item


class BaseRequest(object):
    __doc__ = "Very basic request object.  This does not implement advanced stuff like\n    entity tag parsing or cache controls.  The request object is created with\n    the WSGI environment as first argument and will add itself to the WSGI\n    environment as ``'werkzeug.request'`` unless it's created with\n    `populate_request` set to False.\n\n    There are a couple of mixins available that add additional functionality\n    to the request object, there is also a class called `Request` which\n    subclasses `BaseRequest` and all the important mixins.\n\n    It's a good idea to create a custom subclass of the :class:`BaseRequest`\n    and add missing functionality either via mixins or direct implementation.\n    Here an example for such subclasses::\n\n        from werkzeug.wrappers import BaseRequest, ETagRequestMixin\n\n        class Request(BaseRequest, ETagRequestMixin):\n            pass\n\n    Request objects are **read only**.  As of 0.5 modifications are not\n    allowed in any place.  Unlike the lower level parsing functions the\n    request object will use immutable objects everywhere possible.\n\n    Per default the request object will assume all the text data is `utf-8`\n    encoded.  Please refer to `the unicode chapter <unicode.txt>`_ for more\n    details about customizing the behavior.\n\n    Per default the request object will be added to the WSGI\n    environment as `werkzeug.request` to support the debugging system.\n    If you don't want that, set `populate_request` to `False`.\n\n    If `shallow` is `True` the environment is initialized as shallow\n    object around the environ.  Every operation that would modify the\n    environ in any way (such as consuming form data) raises an exception\n    unless the `shallow` attribute is explicitly set to `False`.  This\n    is useful for middlewares where you don't want to consume the form\n    data by accident.  A shallow request is not populated to the WSGI\n    environment.\n\n    .. versionchanged:: 0.5\n       read-only mode was enforced by using immutables classes for all\n       data.\n    "
    charset = 'utf-8'
    encoding_errors = 'replace'
    max_content_length = None
    max_form_memory_size = None
    parameter_storage_class = ImmutableMultiDict
    list_storage_class = ImmutableList
    dict_storage_class = ImmutableTypeConversionDict
    form_data_parser_class = FormDataParser
    trusted_hosts = None
    disable_data_descriptor = False

    def __init__(self, environ, populate_request=True, shallow=False):
        self.environ = environ
        if populate_request:
            if not shallow:
                self.environ['werkzeug.request'] = self
        self.shallow = shallow

    def __repr__(self):
        args = []
        try:
            args.append("'%s'" % self.url)
            args.append('[%s]' % self.method)
        except Exception:
            args.append('(invalid WSGI environ)')

        return '<%s %s>' % (
         self.__class__.__name__,
         ' '.join(args))

    @property
    def url_charset(self):
        """The charset that is assumed for URLs.  Defaults to the value
        of :attr:`charset`.

        .. versionadded:: 0.6
        """
        return self.charset

    @classmethod
    def from_values(cls, *args, **kwargs):
        """Create a new request object based on the values provided.  If
        environ is given missing values are filled from there.  This method is
        useful for small scripts when you need to simulate a request from an URL.
        Do not use this method for unittesting, there is a full featured client
        object (:class:`Client`) that allows to create multipart requests,
        support for cookies etc.

        This accepts the same options as the
        :class:`~werkzeug.test.EnvironBuilder`.

        .. versionchanged:: 0.5
           This method now accepts the same arguments as
           :class:`~werkzeug.test.EnvironBuilder`.  Because of this the
           `environ` parameter is now called `environ_overrides`.

        :return: request object
        """
        from werkzeug.test import EnvironBuilder
        charset = kwargs.pop('charset', cls.charset)
        builder = EnvironBuilder(*args, **kwargs)
        try:
            return builder.get_request(cls)
        finally:
            builder.close()

    @classmethod
    def application(cls, f):
        """Decorate a function as responder that accepts the request as first
        argument.  This works like the :func:`responder` decorator but the
        function is passed the request object as first argument and the
        request object will be closed automatically::

            @Request.application
            def my_wsgi_app(request):
                return Response('Hello World!')

        :param f: the WSGI callable to decorate
        :return: a new WSGI callable
        """

        def application(*args):
            request = cls(args[(-2)])
            with request:
                return f(*(args[:-2] + (request,)))(*args[-2:])

        return update_wrapper(application, f)

    def _get_file_stream(self, total_content_length, content_type, filename=None, content_length=None):
        """Called to get a stream for the file upload.

        This must provide a file-like class with `read()`, `readline()`
        and `seek()` methods that is both writeable and readable.

        The default implementation returns a temporary file if the total
        content length is higher than 500KB.  Because many browsers do not
        provide a content length for the files only the total content
        length matters.

        :param total_content_length: the total content length of all the
                                     data in the request combined.  This value
                                     is guaranteed to be there.
        :param content_type: the mimetype of the uploaded file.
        :param filename: the filename of the uploaded file.  May be `None`.
        :param content_length: the length of this file.  This value is usually
                               not provided because webbrowsers do not provide
                               this value.
        """
        return default_stream_factory(total_content_length, content_type, filename, content_length)

    @property
    def want_form_data_parsed(self):
        """Returns True if the request method carries content.  As of
        Werkzeug 0.9 this will be the case if a content type is transmitted.

        .. versionadded:: 0.8
        """
        return bool(self.environ.get('CONTENT_TYPE'))

    def make_form_data_parser(self):
        """Creates the form data parser.  Instanciates the
        :attr:`form_data_parser_class` with some parameters.

        .. versionadded:: 0.8
        """
        return self.form_data_parser_class(self._get_file_stream, self.charset, self.encoding_errors, self.max_form_memory_size, self.max_content_length, self.parameter_storage_class)

    def _load_form_data(self):
        """Method used internally to retrieve submitted data.  After calling
        this sets `form` and `files` on the request object to multi dicts
        filled with the incoming form data.  As a matter of fact the input
        stream will be empty afterwards.  You can also call this method to
        force the parsing of the form data.

        .. versionadded:: 0.8
        """
        if 'form' in self.__dict__:
            return
        _assert_not_shallow(self)
        if self.want_form_data_parsed:
            content_type = self.environ.get('CONTENT_TYPE', '')
            content_length = get_content_length(self.environ)
            mimetype, options = parse_options_header(content_type)
            parser = self.make_form_data_parser()
            data = parser.parse(self._get_stream_for_parsing(), mimetype, content_length, options)
        else:
            data = (
             self.stream, self.parameter_storage_class(),
             self.parameter_storage_class())
        d = self.__dict__
        d['stream'], d['form'], d['files'] = data

    def _get_stream_for_parsing(self):
        """This is the same as accessing :attr:`stream` with the difference
        that if it finds cached data from calling :meth:`get_data` first it
        will create a new stream out of the cached data.

        .. versionadded:: 0.9.3
        """
        cached_data = getattr(self, '_cached_data', None)
        if cached_data is not None:
            return BytesIO(cached_data)
        else:
            return self.stream

    def close(self):
        """Closes associated resources of this request object.  This
        closes all file handles explicitly.  You can also use the request
        object in a with statement with will automatically close it.

        .. versionadded:: 0.9
        """
        files = self.__dict__.get('files')
        for key, value in iter_multi_items(files or ()):
            value.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()

    @cached_property
    def stream(self):
        """The stream to read incoming data from.  Unlike :attr:`input_stream`
        this stream is properly guarded that you can't accidentally read past
        the length of the input.  Werkzeug will internally always refer to
        this stream to read data which makes it possible to wrap this
        object with a stream that does filtering.

        .. versionchanged:: 0.9
           This stream is now always available but might be consumed by the
           form parser later on.  Previously the stream was only set if no
           parsing happened.
        """
        _assert_not_shallow(self)
        return get_input_stream(self.environ)

    input_stream = environ_property('wsgi.input', "The WSGI input stream.\nIn general it's a bad idea to use this one because you can easily read past the boundary.  Use the :attr:`stream` instead.")

    @cached_property
    def args(self):
        """The parsed URL parameters.  By default an
        :class:`~werkzeug.datastructures.ImmutableMultiDict`
        is returned from this function.  This can be changed by setting
        :attr:`parameter_storage_class` to a different type.  This might
        be necessary if the order of the form data is important.
        """
        return url_decode(wsgi_get_bytes(self.environ.get('QUERY_STRING', '')), self.url_charset, errors=self.encoding_errors, cls=self.parameter_storage_class)

    @cached_property
    def data(self):
        if self.disable_data_descriptor:
            raise AttributeError('data descriptor is disabled')
        return self.get_data(parse_form_data=True)

    def get_data(self, cache=True, as_text=False, parse_form_data=False):
        """This reads the buffered incoming data from the client into one
        bytestring.  By default this is cached but that behavior can be
        changed by setting `cache` to `False`.

        Usually it's a bad idea to call this method without checking the
        content length first as a client could send dozens of megabytes or more
        to cause memory problems on the server.

        Note that if the form data was already parsed this method will not
        return anything as form data parsing does not cache the data like
        this method does.  To implicitly invoke form data parsing function
        set `parse_form_data` to `True`.  When this is done the return value
        of this method will be an empty string if the form parser handles
        the data.  This generally is not necessary as if the whole data is
        cached (which is the default) the form parser will used the cached
        data to parse the form data.  Please be generally aware of checking
        the content length first in any case before calling this method
        to avoid exhausting server memory.

        If `as_text` is set to `True` the return value will be a decoded
        unicode string.

        .. versionadded:: 0.9
        """
        rv = getattr(self, '_cached_data', None)
        if rv is None:
            if parse_form_data:
                self._load_form_data()
            rv = self.stream.read()
            if cache:
                self._cached_data = rv
        if as_text:
            rv = rv.decode(self.charset, self.encoding_errors)
        return rv

    @cached_property
    def form(self):
        """The form parameters.  By default an
        :class:`~werkzeug.datastructures.ImmutableMultiDict`
        is returned from this function.  This can be changed by setting
        :attr:`parameter_storage_class` to a different type.  This might
        be necessary if the order of the form data is important.
        """
        self._load_form_data()
        return self.form

    @cached_property
    def values(self):
        """Combined multi dict for :attr:`args` and :attr:`form`."""
        args = []
        for d in (self.args, self.form):
            if not isinstance(d, MultiDict):
                d = MultiDict(d)
            args.append(d)

        return CombinedMultiDict(args)

    @cached_property
    def files(self):
        """:class:`~werkzeug.datastructures.MultiDict` object containing
        all uploaded files.  Each key in :attr:`files` is the name from the
        ``<input type="file" name="">``.  Each value in :attr:`files` is a
        Werkzeug :class:`~werkzeug.datastructures.FileStorage` object.

        Note that :attr:`files` will only contain data if the request method was
        POST, PUT or PATCH and the ``<form>`` that posted to the request had
        ``enctype="multipart/form-data"``.  It will be empty otherwise.

        See the :class:`~werkzeug.datastructures.MultiDict` /
        :class:`~werkzeug.datastructures.FileStorage` documentation for
        more details about the used data structure.
        """
        self._load_form_data()
        return self.files

    @cached_property
    def cookies(self):
        """Read only access to the retrieved cookie values as dictionary."""
        return parse_cookie(self.environ, self.charset, self.encoding_errors, cls=self.dict_storage_class)

    @cached_property
    def headers(self):
        """The headers from the WSGI environ as immutable
        :class:`~werkzeug.datastructures.EnvironHeaders`.
        """
        return EnvironHeaders(self.environ)

    @cached_property
    def path(self):
        """Requested path as unicode.  This works a bit like the regular path
        info in the WSGI environment but will always include a leading slash,
        even if the URL root is accessed.
        """
        raw_path = wsgi_decoding_dance(self.environ.get('PATH_INFO') or '', self.charset, self.encoding_errors)
        return '/' + raw_path.lstrip('/')

    @cached_property
    def full_path(self):
        """Requested path as unicode, including the query string."""
        return self.path + '?' + to_unicode(self.query_string, self.url_charset)

    @cached_property
    def script_root(self):
        """The root path of the script without the trailing slash."""
        raw_path = wsgi_decoding_dance(self.environ.get('SCRIPT_NAME') or '', self.charset, self.encoding_errors)
        return raw_path.rstrip('/')

    @cached_property
    def url(self):
        """The reconstructed current URL"""
        return get_current_url(self.environ, trusted_hosts=self.trusted_hosts)

    @cached_property
    def base_url(self):
        """Like :attr:`url` but without the querystring"""
        return get_current_url(self.environ, strip_querystring=True, trusted_hosts=self.trusted_hosts)

    @cached_property
    def url_root(self):
        """The full URL root (with hostname), this is the application root."""
        return get_current_url(self.environ, True, trusted_hosts=self.trusted_hosts)

    @cached_property
    def host_url(self):
        """Just the host with scheme."""
        return get_current_url(self.environ, host_only=True, trusted_hosts=self.trusted_hosts)

    @cached_property
    def host(self):
        """Just the host including the port if available."""
        return get_host(self.environ, trusted_hosts=self.trusted_hosts)

    query_string = environ_property('QUERY_STRING', '', read_only=True, load_func=wsgi_get_bytes, doc='The URL parameters as raw bytestring.')
    method = environ_property('REQUEST_METHOD', 'GET', read_only=True, doc="The transmission method. (For example ``'GET'`` or ``'POST'``).")

    @cached_property
    def access_route(self):
        """If a forwarded header exists this is a list of all ip addresses
        from the client ip to the last proxy server.
        """
        if 'HTTP_X_FORWARDED_FOR' in self.environ:
            addr = self.environ['HTTP_X_FORWARDED_FOR'].split(',')
            return self.list_storage_class([x.strip() for x in addr])
        if 'REMOTE_ADDR' in self.environ:
            return self.list_storage_class([self.environ['REMOTE_ADDR']])
        return self.list_storage_class()

    @property
    def remote_addr(self):
        """The remote address of the client."""
        return self.environ.get('REMOTE_ADDR')

    remote_user = environ_property('REMOTE_USER', doc='\n        If the server supports user authentication, and the script is\n        protected, this attribute contains the username the user has\n        authenticated as.')
    scheme = environ_property('wsgi.url_scheme', doc='\n        URL scheme (http or https).\n\n        .. versionadded:: 0.7')
    is_xhr = property(lambda x: x.environ.get('HTTP_X_REQUESTED_WITH', '').lower() == 'xmlhttprequest', doc='\n        True if the request was triggered via a JavaScript XMLHttpRequest.\n        This only works with libraries that support the `X-Requested-With`\n        header and set it to "XMLHttpRequest".  Libraries that do that are\n        prototype, jQuery and Mochikit and probably some more.')
    is_secure = property(lambda x: x.environ['wsgi.url_scheme'] == 'https', doc='`True` if the request is secure.')
    is_multithread = environ_property('wsgi.multithread', doc='\n        boolean that is `True` if the application is served by\n        a multithreaded WSGI server.')
    is_multiprocess = environ_property('wsgi.multiprocess', doc='\n        boolean that is `True` if the application is served by\n        a WSGI server that spawns multiple processes.')
    is_run_once = environ_property('wsgi.run_once', doc="\n        boolean that is `True` if the application will be executed only\n        once in a process lifetime.  This is the case for CGI for example,\n        but it's not guaranteed that the exeuction only happens one time.")


class BaseResponse(object):
    __doc__ = "Base response class.  The most important fact about a response object\n    is that it's a regular WSGI application.  It's initialized with a couple\n    of response parameters (headers, body, status code etc.) and will start a\n    valid WSGI response when called with the environ and start response\n    callable.\n\n    Because it's a WSGI application itself processing usually ends before the\n    actual response is sent to the server.  This helps debugging systems\n    because they can catch all the exceptions before responses are started.\n\n    Here a small example WSGI application that takes advantage of the\n    response objects::\n\n        from werkzeug.wrappers import BaseResponse as Response\n\n        def index():\n            return Response('Index page')\n\n        def application(environ, start_response):\n            path = environ.get('PATH_INFO') or '/'\n            if path == '/':\n                response = index()\n            else:\n                response = Response('Not Found', status=404)\n            return response(environ, start_response)\n\n    Like :class:`BaseRequest` which object is lacking a lot of functionality\n    implemented in mixins.  This gives you a better control about the actual\n    API of your response objects, so you can create subclasses and add custom\n    functionality.  A full featured response object is available as\n    :class:`Response` which implements a couple of useful mixins.\n\n    To enforce a new type of already existing responses you can use the\n    :meth:`force_type` method.  This is useful if you're working with different\n    subclasses of response objects and you want to post process them with a\n    know interface.\n\n    Per default the request object will assume all the text data is `utf-8`\n    encoded.  Please refer to `the unicode chapter <unicode.txt>`_ for more\n    details about customizing the behavior.\n\n    Response can be any kind of iterable or string.  If it's a string it's\n    considered being an iterable with one item which is the string passed.\n    Headers can be a list of tuples or a\n    :class:`~werkzeug.datastructures.Headers` object.\n\n    Special note for `mimetype` and `content_type`:  For most mime types\n    `mimetype` and `content_type` work the same, the difference affects\n    only 'text' mimetypes.  If the mimetype passed with `mimetype` is a\n    mimetype starting with `text/`, the charset parameter of the response\n    object is appended to it.  In contrast the `content_type` parameter is\n    always added as header unmodified.\n\n    .. versionchanged:: 0.5\n       the `direct_passthrough` parameter was added.\n\n    :param response: a string or response iterable.\n    :param status: a string with a status or an integer with the status code.\n    :param headers: a list of headers or a\n                    :class:`~werkzeug.datastructures.Headers` object.\n    :param mimetype: the mimetype for the request.  See notice above.\n    :param content_type: the content type for the request.  See notice above.\n    :param direct_passthrough: if set to `True` :meth:`iter_encoded` is not\n                               called before iteration which makes it\n                               possible to pass special iterators though\n                               unchanged (see :func:`wrap_file` for more\n                               details.)\n    "
    charset = 'utf-8'
    default_status = 200
    default_mimetype = 'text/plain'
    implicit_sequence_conversion = True
    autocorrect_location_header = True
    automatically_set_content_length = True

    def __init__(self, response=None, status=None, headers=None, mimetype=None, content_type=None, direct_passthrough=False):
        if isinstance(headers, Headers):
            self.headers = headers
        else:
            if not headers:
                self.headers = Headers()
            else:
                self.headers = Headers(headers)
            if content_type is None:
                if mimetype is None:
                    if 'content-type' not in self.headers:
                        mimetype = self.default_mimetype
                if mimetype is not None:
                    mimetype = get_content_type(mimetype, self.charset)
                content_type = mimetype
            if content_type is not None:
                self.headers['Content-Type'] = content_type
            if status is None:
                status = self.default_status
            if isinstance(status, integer_types):
                self.status_code = status
            else:
                self.status = status
            self.direct_passthrough = direct_passthrough
            self._on_close = []
            if response is None:
                self.response = []
            else:
                if isinstance(response, (text_type, bytes, bytearray)):
                    self.set_data(response)
                else:
                    self.response = response
        return

    def call_on_close(self, func):
        """Adds a function to the internal list of functions that should
        be called as part of closing down the response.  Since 0.7 this
        function also returns the function that was passed so that this
        can be used as a decorator.

        .. versionadded:: 0.6
        """
        self._on_close.append(func)
        return func

    def __repr__(self):
        if self.is_sequence:
            body_info = '%d bytes' % sum(map(len, self.iter_encoded()))
        else:
            body_info = self.is_streamed and 'streamed' or 'likely-streamed'
        return '<%s %s [%s]>' % (
         self.__class__.__name__,
         body_info,
         self.status)

    @classmethod
    def force_type(cls, response, environ=None):
        """Enforce that the WSGI response is a response object of the current
        type.  Werkzeug will use the :class:`BaseResponse` internally in many
        situations like the exceptions.  If you call :meth:`get_response` on an
        exception you will get back a regular :class:`BaseResponse` object, even
        if you are using a custom subclass.

        This method can enforce a given response type, and it will also
        convert arbitrary WSGI callables into response objects if an environ
        is provided::

            # convert a Werkzeug response object into an instance of the
            # MyResponseClass subclass.
            response = MyResponseClass.force_type(response)

            # convert any WSGI application into a response object
            response = MyResponseClass.force_type(response, environ)

        This is especially useful if you want to post-process responses in
        the main dispatcher and use functionality provided by your subclass.

        Keep in mind that this will modify response objects in place if
        possible!

        :param response: a response object or wsgi application.
        :param environ: a WSGI environment object.
        :return: a response object.
        """
        if not isinstance(response, BaseResponse):
            if environ is None:
                raise TypeError('cannot convert WSGI application into response objects without an environ')
            rv = yield from call_maybe_yield(_run_wsgi_app, response, environ)
            response = BaseResponse(*rv)
        response.__class__ = cls
        return response

    @classmethod
    def from_app(cls, app, environ, buffered=False):
        """Create a new response object from an application output.  This
        works best if you pass it an application that returns a generator all
        the time.  Sometimes applications may use the `write()` callable
        returned by the `start_response` function.  This tries to resolve such
        edge cases automatically.  But if you don't get the expected output
        you should set `buffered` to `True` which enforces buffering.

        :param app: the WSGI application to execute.
        :param environ: the WSGI environment to execute against.
        :param buffered: set to `True` to enforce buffering.
        :return: a response object.
        """
        return cls(*_run_wsgi_app(app, environ, buffered))

    def _get_status_code(self):
        return self._status_code

    def _set_status_code(self, code):
        self._status_code = code
        try:
            self._status = '%d %s' % (code, HTTP_STATUS_CODES[code].upper())
        except KeyError:
            self._status = '%d UNKNOWN' % code

    status_code = property(_get_status_code, _set_status_code, doc='The HTTP Status code as number')
    del _get_status_code
    del _set_status_code

    def _get_status(self):
        return self._status

    def _set_status(self, value):
        self._status = to_native(value)
        try:
            self._status_code = int(self._status.split(None, 1)[0])
        except ValueError:
            self._status_code = 0
            self._status = '0 %s' % self._status

        return

    status = property(_get_status, _set_status, doc='The HTTP Status code')
    del _get_status
    del _set_status

    def get_data(self, as_text=False):
        """The string representation of the request body.  Whenever you call
        this property the request iterable is encoded and flattened.  This
        can lead to unwanted behavior if you stream big data.

        This behavior can be disabled by setting
        :attr:`implicit_sequence_conversion` to `False`.

        If `as_text` is set to `True` the return value will be a decoded
        unicode string.

        .. versionadded:: 0.9
        """
        self._ensure_sequence()
        rv = (b'').join(self.iter_encoded())
        if as_text:
            rv = rv.decode(self.charset)
        return rv

    def set_data(self, value):
        """Sets a new string as response.  The value set must either by a
        unicode or bytestring.  If a unicode string is set it's encoded
        automatically to the charset of the response (utf-8 by default).

        .. versionadded:: 0.9
        """
        if isinstance(value, text_type):
            value = value.encode(self.charset)
        else:
            value = bytes(value)
        self.response = [
         value]
        if self.automatically_set_content_length:
            self.headers['Content-Length'] = str(len(value))

    data = property(get_data, set_data, doc='\n        A descriptor that calls :meth:`get_data` and :meth:`set_data`.  This\n        should not be used and will eventually get deprecated.\n        ')

    def calculate_content_length(self):
        """Returns the content length if available or `None` otherwise."""
        try:
            self._ensure_sequence()
        except RuntimeError:
            return

        return sum(len(x) for x in self.response)

    def _ensure_sequence(self, mutable=False):
        """This method can be called by methods that need a sequence.  If
        `mutable` is true, it will also ensure that the response sequence
        is a standard Python list.

        .. versionadded:: 0.6
        """
        if self.is_sequence:
            if mutable:
                if not isinstance(self.response, list):
                    self.response = list(self.response)
            return
        if self.direct_passthrough:
            raise RuntimeError('Attempted implicit sequence conversion but the response object is in direct passthrough mode.')
        if not self.implicit_sequence_conversion:
            raise RuntimeError('The response object required the iterable to be a sequence, but the implicit conversion was disabled.  Call make_sequence() yourself.')
        self.make_sequence()

    def make_sequence(self):
        """Converts the response iterator in a list.  By default this happens
        automatically if required.  If `implicit_sequence_conversion` is
        disabled, this method is not automatically called and some properties
        might raise exceptions.  This also encodes all the items.

        .. versionadded:: 0.6
        """
        if not self.is_sequence:
            close = getattr(self.response, 'close', None)
            self.response = list(self.iter_encoded())
            if close is not None:
                self.call_on_close(close)
        return

    def iter_encoded(self):
        """Iter the response encoded with the encoding of the response.
        If the response object is invoked as WSGI application the return
        value of this method is used as application iterator unless
        :attr:`direct_passthrough` was activated.
        """
        charset = self.charset
        _warn_if_string(self.response)
        return _iter_encoded(self.response, self.charset)

    def set_cookie(self, key, value='', max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False):
        """Sets a cookie. The parameters are the same as in the cookie `Morsel`
        object in the Python standard library but it accepts unicode data, too.

        :param key: the key (name) of the cookie to be set.
        :param value: the value of the cookie.
        :param max_age: should be a number of seconds, or `None` (default) if
                        the cookie should last only as long as the client's
                        browser session.
        :param expires: should be a `datetime` object or UNIX timestamp.
        :param domain: if you want to set a cross-domain cookie.  For example,
                       ``domain=".example.com"`` will set a cookie that is
                       readable by the domain ``www.example.com``,
                       ``foo.example.com`` etc.  Otherwise, a cookie will only
                       be readable by the domain that set it.
        :param path: limits the cookie to a given path, per default it will
                     span the whole domain.
        """
        self.headers.add('Set-Cookie', dump_cookie(key, value, max_age, expires, path, domain, secure, httponly, self.charset))

    def delete_cookie(self, key, path='/', domain=None):
        """Delete a cookie.  Fails silently if key doesn't exist.

        :param key: the key (name) of the cookie to be deleted.
        :param path: if the cookie that should be deleted was limited to a
                     path, the path has to be defined here.
        :param domain: if the cookie that should be deleted was limited to a
                       domain, that domain has to be defined here.
        """
        self.set_cookie(key, expires=0, max_age=0, path=path, domain=domain)

    @property
    def is_streamed(self):
        """If the response is streamed (the response is not an iterable with
        a length information) this property is `True`.  In this case streamed
        means that there is no information about the number of iterations.
        This is usually `True` if a generator is passed to the response object.

        This is useful for checking before applying some sort of post
        filtering that should not take place for streamed responses.
        """
        try:
            len(self.response)
        except (TypeError, AttributeError):
            return True

        return False

    @property
    def is_sequence(self):
        """If the iterator is buffered, this property will be `True`.  A
        response object will consider an iterator to be buffered if the
        response attribute is a list or tuple.

        .. versionadded:: 0.6
        """
        return isinstance(self.response, (tuple, list))

    def close(self):
        """Close the wrapped response if possible.  You can also use the object
        in a with statement which will automatically close it.

        .. versionadded:: 0.9
           Can now be used in a with statement.
        """
        if hasattr(self.response, 'close'):
            self.response.close()
        for func in self._on_close:
            func()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()

    def freeze(self):
        """Call this method if you want to make your response object ready for
        being pickled.  This buffers the generator if there is one.  It will
        also set the `Content-Length` header to the length of the body.

        .. versionchanged:: 0.6
           The `Content-Length` header is now set.
        """
        self.response = list(self.iter_encoded())
        self.headers['Content-Length'] = str(sum(map(len, self.response)))

    def get_wsgi_headers(self, environ):
        """This is automatically called right before the response is started
        and returns headers modified for the given environment.  It returns a
        copy of the headers from the response with some modifications applied
        if necessary.

        For example the location header (if present) is joined with the root
        URL of the environment.  Also the content length is automatically set
        to zero here for certain status codes.

        .. versionchanged:: 0.6
           Previously that function was called `fix_headers` and modified
           the response object in place.  Also since 0.6, IRIs in location
           and content-location headers are handled properly.

           Also starting with 0.6, Werkzeug will attempt to set the content
           length if it is able to figure it out on its own.  This is the
           case if all the strings in the response iterable are already
           encoded and the iterable is buffered.

        :param environ: the WSGI environment of the request.
        :return: returns a new :class:`~werkzeug.datastructures.Headers`
                 object.
        """
        headers = Headers(self.headers)
        location = None
        content_location = None
        content_length = None
        status = self.status_code
        for key, value in headers:
            ikey = key.lower()
            if ikey == 'location':
                location = value
            elif ikey == 'content-location':
                content_location = value
            elif ikey == 'content-length':
                content_length = value
                continue

        if location is not None:
            old_location = location
            if isinstance(location, text_type):
                location = iri_to_uri(location)
            if self.autocorrect_location_header:
                current_url = get_current_url(environ, root_only=True)
                if isinstance(current_url, text_type):
                    current_url = iri_to_uri(current_url)
                location = url_join(current_url, location)
            if location != old_location:
                headers['Location'] = location
        if content_location is not None:
            if isinstance(content_location, text_type):
                headers['Content-Location'] = iri_to_uri(content_location)
        if 100 <= status < 200 or status == 204:
            headers['Content-Length'] = content_length = '0'
        elif status == 304:
            remove_entity_headers(headers)
        if self.automatically_set_content_length:
            if self.is_sequence and content_length is None and status != 304:
                try:
                    content_length = sum(len(to_bytes(x, 'ascii')) for x in self.response)
                except UnicodeError:
                    pass
                else:
                    headers['Content-Length'] = str(content_length)
        return headers

    def get_app_iter(self, environ):
        """Returns the application iterator for the given environ.  Depending
        on the request method and the current status code the return value
        might be an empty response rather than the one from the response.

        If the request method is `HEAD` or the status code is in a range
        where the HTTP specification requires an empty response, an empty
        iterable is returned.

        .. versionadded:: 0.6

        :param environ: the WSGI environment of the request.
        :return: a response iterable.
        """
        status = self.status_code
        if environ['REQUEST_METHOD'] == 'HEAD' or 100 <= status < 200 or status in (204,
                                                                                    304):
            iterable = ()
        else:
            if self.direct_passthrough:
                _warn_if_string(self.response)
                return self.response
            iterable = self.iter_encoded()
        return ClosingIterator(iterable, self.close)

    def get_wsgi_response(self, environ):
        """Returns the final WSGI response as tuple.  The first item in
        the tuple is the application iterator, the second the status and
        the third the list of headers.  The response returned is created
        specially for the given environment.  For example if the request
        method in the WSGI environment is ``'HEAD'`` the response will
        be empty and only the headers and status code will be present.

        .. versionadded:: 0.6

        :param environ: the WSGI environment of the request.
        :return: an ``(app_iter, status, headers)`` tuple.
        """
        headers = self.get_wsgi_headers(environ)
        app_iter = self.get_app_iter(environ)
        return (app_iter, self.status, headers.to_wsgi_list())

    def __call__(self, environ, start_response):
        """Process this response as WSGI application.

        :param environ: the WSGI environment.
        :param start_response: the response callable provided by the WSGI
                               server.
        :return: an application iterator
        """
        app_iter, status, headers = self.get_wsgi_response(environ)
        start_response(status, headers)
        return app_iter


class AcceptMixin(object):
    __doc__ = 'A mixin for classes with an :attr:`~BaseResponse.environ` attribute\n    to get all the HTTP accept headers as\n    :class:`~werkzeug.datastructures.Accept` objects (or subclasses\n    thereof).\n    '

    @cached_property
    def accept_mimetypes(self):
        """List of mimetypes this client supports as
        :class:`~werkzeug.datastructures.MIMEAccept` object.
        """
        return parse_accept_header(self.environ.get('HTTP_ACCEPT'), MIMEAccept)

    @cached_property
    def accept_charsets(self):
        """List of charsets this client supports as
        :class:`~werkzeug.datastructures.CharsetAccept` object.
        """
        return parse_accept_header(self.environ.get('HTTP_ACCEPT_CHARSET'), CharsetAccept)

    @cached_property
    def accept_encodings(self):
        """List of encodings this client accepts.  Encodings in a HTTP term
        are compression encodings such as gzip.  For charsets have a look at
        :attr:`accept_charset`.
        """
        return parse_accept_header(self.environ.get('HTTP_ACCEPT_ENCODING'))

    @cached_property
    def accept_languages(self):
        """List of languages this client accepts as
        :class:`~werkzeug.datastructures.LanguageAccept` object.

        .. versionchanged 0.5
           In previous versions this was a regular
           :class:`~werkzeug.datastructures.Accept` object.
        """
        return parse_accept_header(self.environ.get('HTTP_ACCEPT_LANGUAGE'), LanguageAccept)


class ETagRequestMixin(object):
    __doc__ = 'Add entity tag and cache descriptors to a request object or object with\n    a WSGI environment available as :attr:`~BaseRequest.environ`.  This not\n    only provides access to etags but also to the cache control header.\n    '

    @cached_property
    def cache_control(self):
        """A :class:`~werkzeug.datastructures.RequestCacheControl` object
        for the incoming cache control headers.
        """
        cache_control = self.environ.get('HTTP_CACHE_CONTROL')
        return parse_cache_control_header(cache_control, None, RequestCacheControl)

    @cached_property
    def if_match(self):
        """An object containing all the etags in the `If-Match` header.

        :rtype: :class:`~werkzeug.datastructures.ETags`
        """
        return parse_etags(self.environ.get('HTTP_IF_MATCH'))

    @cached_property
    def if_none_match(self):
        """An object containing all the etags in the `If-None-Match` header.

        :rtype: :class:`~werkzeug.datastructures.ETags`
        """
        return parse_etags(self.environ.get('HTTP_IF_NONE_MATCH'))

    @cached_property
    def if_modified_since(self):
        """The parsed `If-Modified-Since` header as datetime object."""
        return parse_date(self.environ.get('HTTP_IF_MODIFIED_SINCE'))

    @cached_property
    def if_unmodified_since(self):
        """The parsed `If-Unmodified-Since` header as datetime object."""
        return parse_date(self.environ.get('HTTP_IF_UNMODIFIED_SINCE'))

    @cached_property
    def if_range(self):
        """The parsed `If-Range` header.

        .. versionadded:: 0.7

        :rtype: :class:`~werkzeug.datastructures.IfRange`
        """
        return parse_if_range_header(self.environ.get('HTTP_IF_RANGE'))

    @cached_property
    def range(self):
        """The parsed `Range` header.

        .. versionadded:: 0.7

        :rtype: :class:`~werkzeug.datastructures.Range`
        """
        return parse_range_header(self.environ.get('HTTP_RANGE'))


class UserAgentMixin(object):
    __doc__ = 'Adds a `user_agent` attribute to the request object which contains the\n    parsed user agent of the browser that triggered the request as a\n    :class:`~werkzeug.useragents.UserAgent` object.\n    '

    @cached_property
    def user_agent(self):
        """The current user agent."""
        from werkzeug.useragents import UserAgent
        return UserAgent(self.environ)


class AuthorizationMixin(object):
    __doc__ = 'Adds an :attr:`authorization` property that represents the parsed\n    value of the `Authorization` header as\n    :class:`~werkzeug.datastructures.Authorization` object.\n    '

    @cached_property
    def authorization(self):
        """The `Authorization` object in parsed form."""
        header = self.environ.get('HTTP_AUTHORIZATION')
        return parse_authorization_header(header)


class StreamOnlyMixin(object):
    __doc__ = 'If mixed in before the request object this will change the bahavior\n    of it to disable handling of form parsing.  This disables the\n    :attr:`files`, :attr:`form` attributes and will just provide a\n    :attr:`stream` attribute that however is always available.\n\n    .. versionadded:: 0.9\n    '
    disable_data_descriptor = True
    want_form_data_parsed = False


class ETagResponseMixin(object):
    __doc__ = 'Adds extra functionality to a response object for etag and cache\n    handling.  This mixin requires an object with at least a `headers`\n    object that implements a dict like interface similar to\n    :class:`~werkzeug.datastructures.Headers`.\n\n    If you want the :meth:`freeze` method to automatically add an etag, you\n    have to mixin this method before the response base class.  The default\n    response class does not do that.\n    '

    @property
    def cache_control(self):
        """The Cache-Control general-header field is used to specify
        directives that MUST be obeyed by all caching mechanisms along the
        request/response chain.
        """

        def on_update(cache_control):
            if not cache_control and 'cache-control' in self.headers:
                del self.headers['cache-control']
            elif cache_control:
                self.headers['Cache-Control'] = cache_control.to_header()

        return parse_cache_control_header(self.headers.get('cache-control'), on_update, ResponseCacheControl)

    def make_conditional(self, request_or_environ):
        """Make the response conditional to the request.  This method works
        best if an etag was defined for the response already.  The `add_etag`
        method can be used to do that.  If called without etag just the date
        header is set.

        This does nothing if the request method in the request or environ is
        anything but GET or HEAD.

        It does not remove the body of the response because that's something
        the :meth:`__call__` function does for us automatically.

        Returns self so that you can do ``return resp.make_conditional(req)``
        but modifies the object in-place.

        :param request_or_environ: a request object or WSGI environment to be
                                   used to make the response conditional
                                   against.
        """
        environ = _get_environ(request_or_environ)
        if environ['REQUEST_METHOD'] in ('GET', 'HEAD'):
            if 'date' not in self.headers:
                self.headers['Date'] = http_date()
            if 'content-length' not in self.headers:
                length = self.calculate_content_length()
                if length is not None:
                    self.headers['Content-Length'] = length
            if not is_resource_modified(environ, self.headers.get('etag'), None, self.headers.get('last-modified')):
                self.status_code = 304
        return self

    def add_etag(self, overwrite=False, weak=False):
        """Add an etag for the current response if there is none yet."""
        if overwrite or 'etag' not in self.headers:
            self.set_etag(generate_etag(self.get_data()), weak)

    def set_etag(self, etag, weak=False):
        """Set the etag, and override the old one if there was one."""
        self.headers['ETag'] = quote_etag(etag, weak)

    def get_etag(self):
        """Return a tuple in the form ``(etag, is_weak)``.  If there is no
        ETag the return value is ``(None, None)``.
        """
        return unquote_etag(self.headers.get('ETag'))

    def freeze(self, no_etag=False):
        """Call this method if you want to make your response object ready for
        pickeling.  This buffers the generator if there is one.  This also
        sets the etag unless `no_etag` is set to `True`.
        """
        if not no_etag:
            self.add_etag()
        super(ETagResponseMixin, self).freeze()

    accept_ranges = header_property('Accept-Ranges', doc="\n        The `Accept-Ranges` header.  Even though the name would indicate\n        that multiple values are supported, it must be one string token only.\n\n        The values ``'bytes'`` and ``'none'`` are common.\n\n        .. versionadded:: 0.7")

    def _get_content_range(self):

        def on_update(rng):
            if not rng:
                del self.headers['content-range']
            else:
                self.headers['Content-Range'] = rng.to_header()

        rv = parse_content_range_header(self.headers.get('content-range'), on_update)
        if rv is None:
            rv = ContentRange(None, None, None, on_update=on_update)
        return rv

    def _set_content_range(self, value):
        if not value:
            del self.headers['content-range']
        else:
            if isinstance(value, string_types):
                self.headers['Content-Range'] = value
            else:
                self.headers['Content-Range'] = value.to_header()

    content_range = property(_get_content_range, _set_content_range, doc='\n        The `Content-Range` header as\n        :class:`~werkzeug.datastructures.ContentRange` object.  Even if the\n        header is not set it wil provide such an object for easier\n        manipulation.\n\n        .. versionadded:: 0.7')
    del _get_content_range
    del _set_content_range


class ResponseStream(object):
    __doc__ = 'A file descriptor like object used by the :class:`ResponseStreamMixin` to\n    represent the body of the stream.  It directly pushes into the response\n    iterable of the response object.\n    '
    mode = 'wb+'

    def __init__(self, response):
        self.response = response
        self.closed = False

    def write(self, value):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        self.response._ensure_sequence(mutable=True)
        self.response.response.append(value)

    def writelines(self, seq):
        for item in seq:
            self.write(item)

    def close(self):
        self.closed = True

    def flush(self):
        if self.closed:
            raise ValueError('I/O operation on closed file')

    def isatty(self):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        return False

    @property
    def encoding(self):
        return self.response.charset


class ResponseStreamMixin(object):
    __doc__ = 'Mixin for :class:`BaseRequest` subclasses.  Classes that inherit from\n    this mixin will automatically get a :attr:`stream` property that provides\n    a write-only interface to the response iterable.\n    '

    @cached_property
    def stream(self):
        """The response iterable as write-only stream."""
        return ResponseStream(self)


class CommonRequestDescriptorsMixin(object):
    __doc__ = 'A mixin for :class:`BaseRequest` subclasses.  Request objects that\n    mix this class in will automatically get descriptors for a couple of\n    HTTP headers with automatic type conversion.\n\n    .. versionadded:: 0.5\n    '
    content_type = environ_property('CONTENT_TYPE', doc='\n        The Content-Type entity-header field indicates the media type of\n        the entity-body sent to the recipient or, in the case of the HEAD\n        method, the media type that would have been sent had the request\n        been a GET.')

    @cached_property
    def content_length(self):
        """The Content-Length entity-header field indicates the size of the
        entity-body in bytes or, in the case of the HEAD method, the size of
        the entity-body that would have been sent had the request been a
        GET.
        """
        return get_content_length(self.environ)

    content_encoding = environ_property('HTTP_CONTENT_ENCODING', doc='\n        The Content-Encoding entity-header field is used as a modifier to the\n        media-type.  When present, its value indicates what additional content\n        codings have been applied to the entity-body, and thus what decoding\n        mechanisms must be applied in order to obtain the media-type\n        referenced by the Content-Type header field.\n\n        .. versionadded:: 0.9')
    content_md5 = environ_property('HTTP_CONTENT_MD5', doc='\n         The Content-MD5 entity-header field, as defined in RFC 1864, is an\n         MD5 digest of the entity-body for the purpose of providing an\n         end-to-end message integrity check (MIC) of the entity-body.  (Note:\n         a MIC is good for detecting accidental modification of the\n         entity-body in transit, but is not proof against malicious attacks.)\n\n        .. versionadded:: 0.9')
    referrer = environ_property('HTTP_REFERER', doc='\n        The Referer[sic] request-header field allows the client to specify,\n        for the server\'s benefit, the address (URI) of the resource from which\n        the Request-URI was obtained (the "referrer", although the header\n        field is misspelled).')
    date = environ_property('HTTP_DATE', None, parse_date, doc='\n        The Date general-header field represents the date and time at which\n        the message was originated, having the same semantics as orig-date\n        in RFC 822.')
    max_forwards = environ_property('HTTP_MAX_FORWARDS', None, int, doc='\n         The Max-Forwards request-header field provides a mechanism with the\n         TRACE and OPTIONS methods to limit the number of proxies or gateways\n         that can forward the request to the next inbound server.')

    def _parse_content_type(self):
        if not hasattr(self, '_parsed_content_type'):
            self._parsed_content_type = parse_options_header(self.environ.get('CONTENT_TYPE', ''))

    @property
    def mimetype(self):
        """Like :attr:`content_type` but without parameters (eg, without
        charset, type etc.).  For example if the content
        type is ``text/html; charset=utf-8`` the mimetype would be
        ``'text/html'``.
        """
        self._parse_content_type()
        return self._parsed_content_type[0]

    @property
    def mimetype_params(self):
        """The mimetype parameters as dict.  For example if the content
        type is ``text/html; charset=utf-8`` the params would be
        ``{'charset': 'utf-8'}``.
        """
        self._parse_content_type()
        return self._parsed_content_type[1]

    @cached_property
    def pragma(self):
        """The Pragma general-header field is used to include
        implementation-specific directives that might apply to any recipient
        along the request/response chain.  All pragma directives specify
        optional behavior from the viewpoint of the protocol; however, some
        systems MAY require that behavior be consistent with the directives.
        """
        return parse_set_header(self.environ.get('HTTP_PRAGMA', ''))


class CommonResponseDescriptorsMixin(object):
    __doc__ = 'A mixin for :class:`BaseResponse` subclasses.  Response objects that\n    mix this class in will automatically get descriptors for a couple of\n    HTTP headers with automatic type conversion.\n    '

    def _get_mimetype(self):
        ct = self.headers.get('content-type')
        if ct:
            return ct.split(';')[0].strip()

    def _set_mimetype(self, value):
        self.headers['Content-Type'] = get_content_type(value, self.charset)

    def _get_mimetype_params(self):

        def on_update(d):
            self.headers['Content-Type'] = dump_options_header(self.mimetype, d)

        d = parse_options_header(self.headers.get('content-type', ''))[1]
        return CallbackDict(d, on_update)

    mimetype = property(_get_mimetype, _set_mimetype, doc='\n        The mimetype (content type without charset etc.)')
    mimetype_params = property(_get_mimetype_params, doc="\n        The mimetype parameters as dict.  For example if the content\n        type is ``text/html; charset=utf-8`` the params would be\n        ``{'charset': 'utf-8'}``.\n\n        .. versionadded:: 0.5\n        ")
    location = header_property('Location', doc='\n        The Location response-header field is used to redirect the recipient\n        to a location other than the Request-URI for completion of the request\n        or identification of a new resource.')
    age = header_property('Age', None, parse_date, http_date, doc="\n        The Age response-header field conveys the sender's estimate of the\n        amount of time since the response (or its revalidation) was\n        generated at the origin server.\n\n        Age values are non-negative decimal integers, representing time in\n        seconds.")
    content_type = header_property('Content-Type', doc='\n        The Content-Type entity-header field indicates the media type of the\n        entity-body sent to the recipient or, in the case of the HEAD method,\n        the media type that would have been sent had the request been a GET.\n    ')
    content_length = header_property('Content-Length', None, int, str, doc='\n        The Content-Length entity-header field indicates the size of the\n        entity-body, in decimal number of OCTETs, sent to the recipient or,\n        in the case of the HEAD method, the size of the entity-body that would\n        have been sent had the request been a GET.')
    content_location = header_property('Content-Location', doc="\n        The Content-Location entity-header field MAY be used to supply the\n        resource location for the entity enclosed in the message when that\n        entity is accessible from a location separate from the requested\n        resource's URI.")
    content_encoding = header_property('Content-Encoding', doc='\n        The Content-Encoding entity-header field is used as a modifier to the\n        media-type.  When present, its value indicates what additional content\n        codings have been applied to the entity-body, and thus what decoding\n        mechanisms must be applied in order to obtain the media-type\n        referenced by the Content-Type header field.')
    content_md5 = header_property('Content-MD5', doc='\n         The Content-MD5 entity-header field, as defined in RFC 1864, is an\n         MD5 digest of the entity-body for the purpose of providing an\n         end-to-end message integrity check (MIC) of the entity-body.  (Note:\n         a MIC is good for detecting accidental modification of the\n         entity-body in transit, but is not proof against malicious attacks.)\n        ')
    date = header_property('Date', None, parse_date, http_date, doc='\n        The Date general-header field represents the date and time at which\n        the message was originated, having the same semantics as orig-date\n        in RFC 822.')
    expires = header_property('Expires', None, parse_date, http_date, doc='\n        The Expires entity-header field gives the date/time after which the\n        response is considered stale. A stale cache entry may not normally be\n        returned by a cache.')
    last_modified = header_property('Last-Modified', None, parse_date, http_date, doc='\n        The Last-Modified entity-header field indicates the date and time at\n        which the origin server believes the variant was last modified.')

    def _get_retry_after(self):
        value = self.headers.get('retry-after')
        if value is None:
            return
        else:
            if value.isdigit():
                return datetime.utcnow() + timedelta(seconds=int(value))
            return parse_date(value)

    def _set_retry_after(self, value):
        if value is None:
            if 'retry-after' in self.headers:
                del self.headers['retry-after']
            return
        else:
            if isinstance(value, datetime):
                value = http_date(value)
            else:
                value = str(value)
            self.headers['Retry-After'] = value
            return

    retry_after = property(_get_retry_after, _set_retry_after, doc='\n        The Retry-After response-header field can be used with a 503 (Service\n        Unavailable) response to indicate how long the service is expected\n        to be unavailable to the requesting client.\n\n        Time in seconds until expiration or date.')

    def _set_property(name, doc=None):

        def fget(self):

            def on_update(header_set):
                if not header_set and name in self.headers:
                    del self.headers[name]
                elif header_set:
                    self.headers[name] = header_set.to_header()

            return parse_set_header(self.headers.get(name), on_update)

        def fset(self, value):
            if not value:
                del self.headers[name]
            else:
                if isinstance(value, string_types):
                    self.headers[name] = value
                else:
                    self.headers[name] = dump_header(value)

        return property(fget, fset, doc=doc)

    vary = _set_property('Vary', doc='\n         The Vary field value indicates the set of request-header fields that\n         fully determines, while the response is fresh, whether a cache is\n         permitted to use the response to reply to a subsequent request\n         without revalidation.')
    content_language = _set_property('Content-Language', doc='\n         The Content-Language entity-header field describes the natural\n         language(s) of the intended audience for the enclosed entity.  Note\n         that this might not be equivalent to all the languages used within\n         the entity-body.')
    allow = _set_property('Allow', doc='\n        The Allow entity-header field lists the set of methods supported\n        by the resource identified by the Request-URI. The purpose of this\n        field is strictly to inform the recipient of valid methods\n        associated with the resource. An Allow header field MUST be\n        present in a 405 (Method Not Allowed) response.')
    del _set_property
    del _get_mimetype
    del _set_mimetype
    del _get_retry_after
    del _set_retry_after


class WWWAuthenticateMixin(object):
    __doc__ = 'Adds a :attr:`www_authenticate` property to a response object.'

    @property
    def www_authenticate(self):
        """The `WWW-Authenticate` header in a parsed form."""

        def on_update(www_auth):
            if not www_auth and 'www-authenticate' in self.headers:
                del self.headers['www-authenticate']
            elif www_auth:
                self.headers['WWW-Authenticate'] = www_auth.to_header()

        header = self.headers.get('www-authenticate')
        return parse_www_authenticate_header(header, on_update)


class Request(BaseRequest, AcceptMixin, ETagRequestMixin, UserAgentMixin, AuthorizationMixin, CommonRequestDescriptorsMixin):
    __doc__ = 'Full featured request object implementing the following mixins:\n\n    - :class:`AcceptMixin` for accept header parsing\n    - :class:`ETagRequestMixin` for etag and cache control handling\n    - :class:`UserAgentMixin` for user agent introspection\n    - :class:`AuthorizationMixin` for http auth handling\n    - :class:`CommonRequestDescriptorsMixin` for common headers\n    '


class PlainRequest(StreamOnlyMixin, Request):
    __doc__ = 'A request object without special form parsing capabilities.\n\n    .. versionadded:: 0.9\n    '


class Response(BaseResponse, ETagResponseMixin, ResponseStreamMixin, CommonResponseDescriptorsMixin, WWWAuthenticateMixin):
    __doc__ = 'Full featured response object implementing the following mixins:\n\n    - :class:`ETagResponseMixin` for etag and cache control handling\n    - :class:`ResponseStreamMixin` to add support for the `stream` property\n    - :class:`CommonResponseDescriptorsMixin` for various HTTP descriptors\n    - :class:`WWWAuthenticateMixin` for HTTP authentication support\n    '