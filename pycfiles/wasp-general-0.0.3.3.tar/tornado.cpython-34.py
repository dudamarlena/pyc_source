# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/web/tornado.py
# Compiled at: 2017-05-01 18:11:43
# Size of source mod 2**32: 5475 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import weakref
from tornado.web import RequestHandler
from wasp_general.network.web.proto import WWebResponseProto
from wasp_general.verify import verify_type
from wasp_general.network.web.headers import WHTTPHeaders
from wasp_general.network.web.session import WWebSessionAdapter
from wasp_general.network.web.request import WWebRequest
from wasp_general.network.web.cookies import WHTTPCookieJar

class WTornadoRequestHandler(RequestHandler):
    __doc__ = '\n\tAccording to http://www.tornadoweb.org/en/stable/web.html, requesthandlers are not thread safe\n\n\t'

    def __init__(self, wasp_web_service, application, request, **kwargs):
        RequestHandler.__init__(self, application, request, **kwargs)
        self._WTornadoRequestHandler__sessions = {}
        self._WTornadoRequestHandler__wasp_web_service = wasp_web_service

    def compute_etag(self):
        pass

    def __handle_request(self):
        fileno = self.request.connection.stream.socket.fileno()

        def close_session():
            if fileno in self._WTornadoRequestHandler__sessions.keys():
                del self._WTornadoRequestHandler__sessions[fileno]

        if fileno in self._WTornadoRequestHandler__sessions.keys():
            session = self._WTornadoRequestHandler__sessions[fileno]
        else:
            session = WTornadoSessionAdapter(self, close_session)
            self._WTornadoRequestHandler__sessions[fileno] = session
        self._WTornadoRequestHandler__wasp_web_service.process_request(session)

    def get(self, *args, **kwargs):
        self._WTornadoRequestHandler__handle_request()

    def head(self, *args, **kwargs):
        self._WTornadoRequestHandler__handle_request()

    def post(self, *args, **kwargs):
        self._WTornadoRequestHandler__handle_request()

    def delete(self, *args, **kwargs):
        self._WTornadoRequestHandler__handle_request()

    def patch(self, *args, **kwargs):
        self._WTornadoRequestHandler__handle_request()

    def put(self, *args, **kwargs):
        self._WTornadoRequestHandler__handle_request()

    def options(self, *args, **kwargs):
        self._WTornadoRequestHandler__handle_request()

    @classmethod
    def __handler__(self, wasp_web_service):

        class Hanlder(WTornadoRequestHandler):

            def __init__(self, application, request, **kwargs):
                WTornadoRequestHandler.__init__(self, wasp_web_service, application, request, **kwargs)

        return Hanlder


class WTornadoSessionAdapter(WWebSessionAdapter):

    def __init__(self, request_handler, cleanup_handler):

        def weakref_handler(socket_ref):
            self.session_close()

        self._WTornadoSessionAdapter__request_handler = request_handler
        self._WTornadoSessionAdapter__socket_ref = weakref.ref(request_handler.request.connection.stream.socket, weakref_handler)
        self._WTornadoSessionAdapter__protocol_version = request_handler.request.version[len('HTTP/'):]
        self._WTornadoSessionAdapter__protocol = request_handler.request.protocol
        self._WTornadoSessionAdapter__cleanup_handler = cleanup_handler

    def accepted_socket(self):
        return self._WTornadoSessionAdapter__socket_ref()

    def protocol_version(self):
        return self._WTornadoSessionAdapter__protocol_version

    def protocol(self):
        return self._WTornadoSessionAdapter__protocol

    def read_request(self):
        handler_headers = self._WTornadoSessionAdapter__request_handler.request.headers
        headers = WHTTPHeaders()
        for header_name in handler_headers.keys():
            headers.add_headers(header_name, *handler_headers.get_list(header_name))

        for cookie in WHTTPCookieJar.import_simple_cookie(self._WTornadoSessionAdapter__request_handler.cookies):
            headers.set_cookie_jar().add_cookie(cookie)

        request = WWebRequest(self, self._WTornadoSessionAdapter__request_handler.request.method, self._WTornadoSessionAdapter__request_handler.request.path, headers=headers.ro())
        return request

    @verify_type(request=WWebRequest, reponse=WWebResponseProto, pushed_responses=WWebResponseProto)
    def write_response(self, request, response, *pushed_responses):
        status = response.status()
        headers = response.headers()
        response_data = response.response_data()
        if status is not None:
            self._WTornadoSessionAdapter__request_handler.set_status(status)
        if headers is not None:
            headers = headers.switch_name_style(self.protocol_version())
            for header_name in headers.headers():
                for header_value in headers[header_name]:
                    self._WTornadoSessionAdapter__request_handler.add_header(header_name, header_value)

            content_type = headers.content_type()
            if content_type is not None:
                self._WTornadoSessionAdapter__request_handler.set_header(headers.normalize_name('Content-Type'), content_type)
            elif response_data is not None:
                self._WTornadoSessionAdapter__request_handler.set_header(headers.normalize_name('Content-Type'), 'application/octet-stream')
            for cookie in headers.set_cookie_jar():
                self._WTornadoSessionAdapter__request_handler.set_cookie(cookie.name(), cookie.value(), **cookie.attrs_as_dict())

        if response_data is not None:
            self._WTornadoSessionAdapter__request_handler.write(response_data)

    def session_close(self):
        self._WTornadoSessionAdapter__cleanup_handler()