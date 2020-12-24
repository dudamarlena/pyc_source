# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/request.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from __future__ import print_function
from ..elements import Attribute
from ..interface import AttributeExposer
from ..tags.context import DataSetter
import requests, logging
log = logging.getLogger(b'moya.runtime')

class ResponseProxy(AttributeExposer):
    """Proxy for a request object"""
    __moya_exposed_attributes__ = [
     b'url',
     b'text',
     b'status_code',
     b'headers',
     b'cookies',
     b'history',
     b'content',
     b'json',
     b'encoding']

    def __init__(self, req, url, method):
        self._req = req
        self._url = url
        self._method = method

    def __repr__(self):
        return (b'<httpresponse {} "{}">').format(self._method, self._url)

    @property
    def url(self):
        return self._req.url

    @property
    def text(self):
        return self._req.text

    @property
    def status_code(self):
        return self._req.status_code

    @property
    def headers(self):
        return dict(self._req.headers)

    @property
    def cookies(self):
        return dict(self._req.cookies)

    @property
    def history(self):
        self._req.history

    @property
    def content(self):
        return self._req.content

    @property
    def json(self):
        try:
            return self._req.json()
        except:
            return

        return

    @property
    def encoding(self):
        return self._req.encoding


class RequestTag(DataSetter):
    """
    Make HTTP requests.

    """

    class Meta:
        tag_name = b'request'

    class Help:
        synopsis = b'make an http request'

    url = Attribute(b'URL to request', required=True)
    method = Attribute(b'Method to use', choices=[b'get', b'post', b'delete', b'put', b'trace', b'head', b'options'], default=None)
    params = Attribute(b'Request parameters', type=b'dict', required=False, default=None)
    headers = Attribute(b'Additional headers', type=b'dict', required=False, default=None)
    data = Attribute(b'Data to be form encoded', type=b'dict', required=False, default=None)
    timeout = Attribute(b'Timeout in seconds', type=b'number', required=False, default=None)
    username = Attribute(b'Username for basic auth', required=False, default=None)
    password = Attribute(b'Password for basic auth', required=False, default=None)

    def _get_method(self):
        return b'get'

    def logic(self, context):
        params = self.get_parameters(context)
        method = params.method or self._get_method()
        request_maker = getattr(requests, method)
        if not self.has_parameter(b'params'):
            request_params = self.get_let_map(context)
        else:
            request_params = params.params
        if params.username is not None:
            auth = (
             params.username, params.password or b'')
        else:
            auth = None
        try:
            log.debug(b'requesting %s %s', method, params.url)
            response = request_maker(params.url, auth=auth, timeout=params.timeout, params=request_params, headers=params.headers, data=params.data)
        except requests.exceptions.Timeout:
            self.throw(b'requests.timeout', b'the server did not response in time', diagnosos=b'Try raising the timeout attribute')
        except requests.exceptions.HTTPError:
            self.throw(b'requests.http-error', b'the server response was not invalid')
        except requests.exceptions.TooManyRedirects:
            self.throw(b'requests.too-many-redirects', b'too may redirect responses')
        except requests.exceptions.RequestException as e:
            self.throw(b'requests.error', (b'unable to make request ({})').format(e))

        response_proxy = ResponseProxy(response, params.url, method)
        self.set_context(context, params.dst, response_proxy)
        return


class RequestGetTag(RequestTag):
    """
    Make a GET request (see [tag]request[/tag]).

    """

    class Help:
        synopsis = b'make a get requests'

    class Meta:
        tag_name = b'request-get'

    def _get_method(self):
        return b'get'


class RequestPostTag(RequestTag):
    """
    Make a POST request (see [tag]request[/tag]).

    """

    class Help:
        synopsis = b'make a post request'

    class Meta:
        tag_name = b'request-post'

    def _get_method(self):
        return b'post'