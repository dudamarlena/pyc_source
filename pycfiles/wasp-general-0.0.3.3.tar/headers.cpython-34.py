# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/web/headers.py
# Compiled at: 2017-06-28 15:44:02
# Size of source mod 2**32: 9406 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import re
from io import StringIO
import email.message
from wasp_general.verify import verify_type, verify_value
from wasp_general.network.web.cookies import WHTTPCookieJar
from wasp_general.network.web.re_statements import http_header_name

class WHTTPHeaders:
    __doc__ = ' Represent HTTP Headers as they are described in RFC 1945. Call :meth:`.WHTTPHeaders.ro` method to create\n\tread-only copy (in this state no changes are allowed)\n\n\tCookies that are stored with :meth:`.WHTTPHeaders.set_cookie_jar` method have highest priority than cookies\n\tstored within constructor and/or :meth:`.WHTTPHeaders.add_header`. So in the conflict situation cookies saved\n\twithin :meth:`.WHTTPHeaders.set_cookie_jar` must be used.\n\n\tCookies that are stored in :meth:`.WHTTPHeaders.client_cookie_jar` are client cookies (i.e. read-only\n\tcookies).\n\t'
    header_name_re = re.compile(http_header_name)

    @staticmethod
    def header_name_check(header_name):
        """ Check header name for validity. Return True if name is valid

                :param header_name: name to check
                :return: bool
                """
        header_match = WHTTPHeaders.header_name_re.match(header_name.encode('us-ascii'))
        return len(header_name) > 0 and header_match is not None

    def __init__(self, **kwargs):
        """ Construct new headers collection

                :param kwargs: dictionary of header names and corresponding values
                """
        self._WHTTPHeaders__headers = {}
        self._WHTTPHeaders__ro_flag = False
        self._WHTTPHeaders__normalization_mode = '1.0'
        self._WHTTPHeaders__set_cookies = WHTTPCookieJar()
        for arg_name in kwargs.keys():
            self.add_headers(arg_name, kwargs[arg_name])

    def headers(self):
        """ Get specified header names

                :return: tuple of str
                """
        return tuple(self._WHTTPHeaders__headers.keys())

    @verify_type('paranoid', header_name=str)
    @verify_value('paranoid', header_name=lambda x: WHTTPHeaders.header_name_check(x))
    def remove_headers(self, header_name):
        """ Remove header by its name

                :param header_name: name of header to remove
                :return: None
                """
        if self._WHTTPHeaders__ro_flag:
            raise RuntimeError('ro')
        header_name = self.normalize_name(header_name)
        if header_name in self._WHTTPHeaders__headers.keys():
            self._WHTTPHeaders__headers.pop(header_name)

    @verify_type('paranoid', header_name=str)
    @verify_value('paranoid', header_name=lambda x: WHTTPHeaders.header_name_check(x))
    @verify_type(value=str, values=str)
    def add_headers(self, header_name, value, *values):
        """ Add new header

                :param header_name: name of the header to add
                :param value: header value
                :param values: additional header values (in a result request/response must be concatenated by the coma          or by the separate header string)
                :return: None
                """
        if self._WHTTPHeaders__ro_flag:
            raise RuntimeError('ro')
        header_name = self.normalize_name(header_name)
        if header_name not in self._WHTTPHeaders__headers.keys():
            self._WHTTPHeaders__headers[header_name] = [
             value]
        else:
            self._WHTTPHeaders__headers[header_name].append(value)
        for single_value in values:
            self._WHTTPHeaders__headers[header_name].append(single_value)

    @verify_type('paranoid', header_name=str, value=str, values=str)
    @verify_value('paranoid', header_name=lambda x: WHTTPHeaders.header_name_check(x))
    def replace_headers(self, header_name, value, *values):
        """ Replace header value with specified value and/or values

                :param header_name: target header
                :param value: new header value
                :param values: additional header values (in a result request/response must be concatenated by the coma          or by the separate header string)
                :return: None
                """
        if self._WHTTPHeaders__ro_flag:
            raise RuntimeError('ro')
        header_name = self.normalize_name(header_name)
        self.remove_headers(header_name)
        self.add_headers(header_name, value, *values)

    @verify_type('paranoid', header_name=str)
    @verify_value('paranoid', header_name=lambda x: WHTTPHeaders.header_name_check(x))
    def get_headers(self, header_name):
        """ Return header value by its name

                :param header_name: header name
                :return: tuple of str
                """
        header_name = self.normalize_name(header_name)
        if header_name in self._WHTTPHeaders__headers.keys():
            return tuple(self._WHTTPHeaders__headers[header_name])

    @verify_type('paranoid', item=str)
    @verify_value('paranoid', item=lambda x: WHTTPHeaders.header_name_check(x))
    def __getitem__(self, item):
        """ Return header value by its name

                :param item: header name
                :return: tuple of str
                """
        return self.get_headers(item)

    @verify_type(header_name=str)
    @verify_value(header_name=lambda x: WHTTPHeaders.header_name_check(x))
    def normalize_name(self, header_name):
        """ Return header name as it is recommended (required) by corresponding http protocol. For
                protocol switching use :meth:`.WHTTPHeaders.switch_name_style` method.

                All current available protocols (0.9-2) compare header names in a case-insensitive fashion. However,
                previous protocol versions (0.9-1.1) recommends to use camel-case names like Foo or Foo-Bar. But
                HTTP/2 (RFC 7540) strictly requires lowercase only header names.

                :param header_name: name to convert
                :return: str
                """
        if self._WHTTPHeaders__normalization_mode in ('0.9', '1.0', '1.1'):
            return '-'.join([x.capitalize() for x in header_name.split('-')])
        if self._WHTTPHeaders__normalization_mode == '2':
            return header_name.lower()
        raise RuntimeError('Internal error: unknown http protocol: %s' % self._WHTTPHeaders__normalization_mode)

    @verify_type(http_protocol_version=str)
    @verify_value(http_protocol_version=lambda x: x in ('0.9', '1.0', '1.1', '2'))
    def switch_name_style(self, http_protocol_version):
        """ Return object copy with header names saved as it is described in the given protocol version

                see :meth:`.WHTTPHeaders.normalize_name`

                :param http_protocol_version: target HTTP protocol version
                :return: WHTTPHeaders
                """
        new_headers = WHTTPHeaders()
        new_headers._WHTTPHeaders__normalization_mode = http_protocol_version
        names = self.headers()
        for name in names:
            new_headers.add_headers(name, *self.get_headers(name))

        for cookie_name in self._WHTTPHeaders__set_cookies.cookies():
            new_headers._WHTTPHeaders__set_cookies.add_cookie(self._WHTTPHeaders__set_cookies[cookie_name].copy())

        return new_headers

    def ro(self):
        """ Return read-only copy of this object

                :return: WHTTPHeaders
                """
        ro_headers = WHTTPHeaders()
        names = self.headers()
        for name in names:
            ro_headers.add_headers(name, *self.get_headers(name))

        ro_headers._WHTTPHeaders__cookies = self._WHTTPHeaders__set_cookies.ro()
        ro_headers._WHTTPHeaders__ro_flag = True
        return ro_headers

    @verify_type('paranoid', value=(str, None))
    def content_type(self, value=None):
        """ Set (replace) and or get "Content-Type" header value

                :param value: value to set (if specified)
                :return: None if header doesn't exist, otherwise - str
                """
        content_type = self.normalize_name('Content-Type')
        if value is not None:
            self.replace_headers(content_type, value)
        if content_type in self._WHTTPHeaders__headers.keys():
            return self._WHTTPHeaders__headers[content_type][0]

    def set_cookie_jar(self):
        """ Return internal cookie jar that must be used for HTTP-response

                see :class:`.WHTTPCookieJar`

                :return: WHTTPCookieJar
                """
        return self._WHTTPHeaders__set_cookies

    def client_cookie_jar(self):
        """ Return internal cookie jar that must be used as HTTP-request cookies

                see :class:`.WHTTPCookieJar`

                :return: WHTTPCookieJar
                """
        cookie_jar = WHTTPCookieJar()
        cookie_header = self.get_headers('Cookie')
        for cookie_string in cookie_header if cookie_header is not None else tuple():
            for single_cookie in WHTTPCookieJar.import_header_text(cookie_string):
                cookie_jar.add_cookie(single_cookie)

        return cookie_jar.ro()

    @classmethod
    @verify_type(http_code=str)
    def import_headers(cls, http_code):
        """ Create WHTTPHeaders by the given code. If code has 'Set-Cookie' headers, that headers are
                parsed, data are stored in internal cookie jar. At the end of parsing 'Set-Cookie' headers are
                removed from the result

                :param http_code: HTTP code to parse
                :return: WHTTPHeaders
                """
        headers = WHTTPHeaders()
        message = email.message_from_file(StringIO(http_code))
        for header_name, header_value in message.items():
            headers.add_headers(header_name, header_value)

        cookie_header = headers.get_headers('Set-Cookie')
        if cookie_header is not None:
            for cookie_string in cookie_header:
                for single_cookie in WHTTPCookieJar.import_header_text(cookie_string):
                    headers.set_cookie_jar().add_cookie(single_cookie)

            headers.remove_headers('Set-Cookie')
        return headers