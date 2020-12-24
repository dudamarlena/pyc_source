# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/wsgi.py
# Compiled at: 2018-06-01 16:44:30
__all__ = [
 'Request', 'Response']
__authors__ = ['Tim Chow']
from urllib import unquote, quote
from collections import namedtuple
import re
from datetime import datetime
from .exception import MissingArgumentError, InvalidRedirectURLError
from .constrant import HTTPStatus

def format_header_name(header_name):
    return ('-').join([ w.capitalize() for w in re.split('[\\-_]', header_name)
                      ])


class Attribute(object):

    def __init__(self):
        self._meta = {}

    def add_attribute(self, attr_name, attr_value):
        self._meta[attr_name] = attr_value

    def set_attribute(self, attr_name, attr_value):
        if attr_name in self._meta:
            self._meta[attr_name] = attr_value

    def remove_attribute(self, attr_name, default=None):
        return self._meta.pop(attr_name, default)

    def get_attribute(self, attr_name):
        return self._meta[attr_name]

    def get_attribute_or_default(self, attr_name, default=None):
        return self._meta.get(attr_name, default)


class Request(Attribute):

    def __init__(self, enviroment, application_context):
        Attribute.__init__(self)
        self._application_context = application_context
        self._content_length = int(enviroment.get('CONTENT_LENGTH') or 0)
        self._body = None
        if self._content_length:
            self._body = enviroment['wsgi.input'].read(self._content_length)
        content_type = (enviroment.get('CONTENT_TYPE') or 'application/octed-stream').split(';')
        self._content_type = content_type[0]
        self._content_type_attributes = {}
        for item in content_type[1:]:
            pair = item.strip().split('=', 1)
            if len(pair) == 2:
                self._content_type_attributes[pair[0]] = pair[1]

        self._uri = enviroment['PATH_INFO']
        self._request_method = enviroment['REQUEST_METHOD']
        self._query_string = self._parse_query_string(enviroment.get('QUERY_STRING', ''))
        self._user_agent = enviroment.get('HTTP_USER_AGENT', '')
        self._headers = self._parse_headers(enviroment)
        self._cookies = self._parse_cookies(self._headers.pop('Cookie', ''))
        self._remote_addr = enviroment.get('REMOTE_ADDR', '127.0.0.1')
        self._server_port = enviroment.get('SERVER_PORT', 80)
        protocol = namedtuple('protocol', ['scheme', 'version'])
        self._protocol = protocol(*enviroment.get('SERVER_PROTOCOL', 'HTTP/1.0').split('/', 1))
        self._wsgi_errors = enviroment['wsgi.errors']
        return

    @property
    def application_context(self):
        return self._application_context

    @property
    def content_length(self):
        return self._content_length

    @property
    def body(self):
        return self._body

    @property
    def content_type(self):
        return self._content_type

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if not uri.startswith('/'):
            raise InvalidRedirectURLError('invalid redirect uri: %s' % uri)
        self._uri = uri

    @property
    def request_method(self):
        return self._request_method

    def _parse_query_string(self, qrs):
        query_string = {}
        for item in qrs.split('&'):
            pair = item.split('=', 1)
            if len(pair) == 2:
                query_string.setdefault(unquote(pair[0]), []).append(unquote(pair[1]))

        return query_string

    def get_argument(self, argument):
        if argument not in self._query_string:
            raise MissingArgumentError('no argument: %s' % argument)
        return self._query_string[argument][0]

    def get_arguments(self, argument):
        if argument not in self._query_string:
            raise MissingArgumentError('no argument: %s' % argument)
        return self._query_string[argument]

    def add_argument(self, arg_name, arg_value):
        self._query_string.setdefault(arg_name, []).append(arg_value)

    @property
    def user_agent(self):
        return self._user_agent

    def _parse_headers(self, enviroment):
        headers = {}
        for key, value in enviroment.iteritems():
            if not key.startswith('HTTP_'):
                continue
            header_name = format_header_name(key[5:])
            headers[header_name] = value

        return headers

    def _parse_cookies(self, cookie_string):
        cookies = {}
        for item in cookie_string.split(';'):
            pair = item.strip().split('=', 1)
            if len(pair) == 1:
                cookies[unquote(pair[0].strip())] = ''
            else:
                cookies[unquote(pair[0].strip())] = unquote(pair[1].strip())

        return cookies

    @property
    def headers(self):
        return self._headers

    def get_header(self, header_name):
        return self.headers[format_header_name(header_name)]

    def get_header_or_default(self, header_name, default=None):
        return self.headers.get(format_header_name(header_name), default)

    @property
    def cookies(self):
        return self._cookies

    def get_cookie(self, cookie_name):
        return self.cookies[cookie_name]

    def get_cookie_or_default(self, cookie_name, default=None):
        return self.cookies.get(cookie_name, default)

    @property
    def remote_addr(self):
        return self._remote_addr

    @property
    def server_port(self):
        return self._server_port

    @property
    def protocol(self):
        return self._protocol

    @property
    def content_type_attributes(self):
        return self._content_type_attributes

    def log_error(self, msg):
        if isinstance(msg, str):
            self._wsgi_errors.write(msg)

    def close(self):
        del self._application_context
        del self._meta


class Response(object):

    def __init__(self, request):
        self._request = request
        self.__initialize()

    def __initialize(self):
        self._status_code = 200
        self._status_message = 'OK'
        self._headers = {}
        self._cookies = {}
        self._internal_redirect_to = None
        return

    def set_status(self, status_code, reason=None):
        self._status_code = status_code
        self._status_message = reason or HTTPStatus.get_message(status_code)

    def add_header(self, header_name, header_value):
        self._headers[format_header_name(header_name)] = header_value

    def redirect(self, url, permanently=True):
        if url.startswith('http://') or url.startswith('https://'):
            self.add_header('Location', url)
            if permanently:
                self.set_status(HTTPStatus.MovedPermanently)
            else:
                self.set_status(HTTPStatus.MovedTemporarily)
        elif url.startswith('/'):
            self._internal_redirect_to = url
        else:
            raise InvalidRedirectURLError('invalid url: %s' % url)

    def set_cookie(self, key, value, path=None, domain=None, expires=None, secure=False, httponly=False):
        cookie = [
         '%s=%s' % (quote(key), quote(value))]
        if path is not None:
            cookie.append('Path=%s' % path)
        if domain is not None:
            cookie.append('Domain=%s' % domain)
        if isinstance(expires, datetime):
            cookie.append('Expires=%s' % expires.strftime('%a, %d %b %Y %H:%M:%S GMT'))
        if secure:
            cookie.append('Secure')
        if httponly:
            cookie.append('HttpOnly')
        self._cookies[key] = ('; ').join(cookie)
        return

    def get_headline(self):
        return '%d %s' % (self._status_code, self._status_message)

    def get_headers(self):
        headers = self._headers.items()
        for key in self._cookies:
            headers.append(('Set-Cookie', self._cookies[key]))

        return headers

    @property
    def status_code(self):
        return self._status_code

    def get_header(self, header_name):
        header_name = format_header_name(header_name)
        return self._headers.get(header_name, None)

    def remove_header(self, header_name):
        header_name = format_header_name(header_name)
        self._headers.pop(header_name, None)
        return

    def remove_headers(self, *header_names):
        for header_name in header_names:
            self.remove_header(header_name)

    def log_error(self, msg):
        self._request.log_error(msg)

    def close(self):
        del self._request

    @property
    def internal_redirect_to(self):
        return self._internal_redirect_to

    def clear(self):
        self.__initialize()