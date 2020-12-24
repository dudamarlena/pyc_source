# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/web/request.py
# Compiled at: 2017-06-28 15:47:00
# Size of source mod 2**32: 4630 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import re
from wasp_general.verify import verify_type, verify_value
from wasp_general.network.web.proto import WWebSessionProto, WWebRequestProto
from wasp_general.network.web.headers import WHTTPHeaders
from wasp_general.network.web.re_statements import http_method_name, http_path, http_version

class WWebRequest(WWebRequestProto):
    __doc__ = ' :class:`.WWebRequestProto` implementation. Class represent HTTP-request descriptor.\n\tCall :meth:`.WWebRequest.ro` method to create unchangeable copy\n\t'
    request_line_re = re.compile('^(' + http_method_name + ') +(' + http_path + ')( +HTTP/(' + http_version + '))?$')

    @verify_type(session=WWebSessionProto, method=str, path=str, headers=(WHTTPHeaders, None))
    @verify_type(request_data=(bytes, None))
    @verify_value(method=lambda x: len(x) > 0)
    @verify_value(path=lambda x: len(x) > 0)
    def __init__(self, session, method, path, headers=None, request_data=None):
        """
                Create new request descriptor

                :param session: request origin
                :param method: called HTTP-method
                :param path: called HTTP-path
                """
        WWebRequestProto.__init__(self)
        self._WWebRequest__session = session
        self._WWebRequest__method = method.upper()
        self._WWebRequest__path = path
        self._WWebRequest__headers = headers
        self._WWebRequest__request_data = request_data
        self._WWebRequest__ro_flag = False

    def session(self):
        """ Return origin session

                :return: WWebSessionProto
                """
        return self._WWebRequest__session

    def method(self):
        """ Return requested method

                :return: str
                """
        return self._WWebRequest__method

    def path(self):
        """ Return requested path

                :return: str
                """
        return self._WWebRequest__path

    def headers(self):
        """ Return request headers

                :return: WHTTPHeaders
                """
        return self._WWebRequest__headers

    @verify_type(headers=WHTTPHeaders)
    def set_headers(self, headers):
        """ Set headers for request

                :param headers: headers to set
                :return: None
                """
        if self._WWebRequest__ro_flag:
            raise RuntimeError('Read-only object changing attempt')
        self._WWebRequest__headers = headers

    def request_data(self):
        """ Return request data

                :return: bytes
                """
        return self._WWebRequest__request_data

    @verify_type(request_data=bytes)
    def set_request_data(self, request_data):
        """ Set payload data for request

                :param request_data: data to set
                :return: None
                """
        if self._WWebRequest__ro_flag:
            raise RuntimeError('Read-only object changing attempt')
        self._WWebRequest__request_data = request_data

    @classmethod
    @verify_type('paranoid', session=WWebSessionProto)
    @verify_type(request_line=str)
    def parse_request_line(cls, session, request_line):
        """ Parse given request line like 'GET /foo' or 'POST /zzz HTTP/1.0'

                :param session: origin session
                :param request_line: line to parse
                :return: WWebRequest
                """
        r = cls.request_line_re.search(request_line)
        if r is not None:
            method, path, protocol_sentence, protocol_version = r.groups()
            return WWebRequest(session, method, path)
        raise ValueError('Invalid request line')

    @verify_type('paranoid', http_code=str)
    def parse_headers(self, http_code):
        """ Parse http-code (like 'Header-X: foo
Header-Y: bar
') and retrieve (save) HTTP-headers

                :param http_code: code to parse
                :return: None
                """
        if self._WWebRequest__ro_flag:
            raise RuntimeError('Read-only object changing attempt')
        self._WWebRequest__headers = WHTTPHeaders.import_headers(http_code)

    def ro(self):
        """ Create read-only copy

                :return: WWebRequest
                """
        request = WWebRequest(self.session(), self.method(), self.path(), headers=self.headers().ro(), request_data=self.request_data())
        request._WWebRequest__ro_flag = True
        return request