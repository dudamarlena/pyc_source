# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/network/http.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 5232 bytes
__doc__ = '\nHTTP module.\n'
import requests, urllib.parse

class HTTPResource:
    """HTTPResource"""

    def __init__(self, path, protocol, host, port, auth=None, headers=None):
        self._HTTPResource__path = path
        self._HTTPResource__protocol = protocol
        self._HTTPResource__host = host
        self._HTTPResource__port = port
        self._HTTPResource__auth = auth or HTTPNoneAuth()
        self._HTTPResource__headers = headers or {}

    def request(self, method_name):
        return HTTPRequest(method_name, self._HTTPResource__protocol, self._HTTPResource__host, self._HTTPResource__port, self._HTTPResource__path, self._HTTPResource__auth, self._HTTPResource__headers)

    def push(self, name):
        path = []
        path.extend(self._HTTPResource__path)
        path.append(name)
        return HTTPResource(path, self._HTTPResource__protocol, self._HTTPResource__host, self._HTTPResource__port, self._HTTPResource__auth, self._HTTPResource__headers)

    def ref(self, url):
        url_obj = urllib.parse.urlparse(url)
        return HTTPResource([url_comp for url_comp in url_obj.path.split('/') if len(url_comp) > 0], url_obj.scheme, url_obj.hostname, url_obj.port, self._HTTPResource__auth, self._HTTPResource__headers)


class HTTPRequest:

    def __init__(self, method, protocol, host, port, path, auth, headers):
        self._HTTPRequest__method = method
        self._HTTPRequest__path = '/'.join(path)
        self._HTTPRequest__url = '{}://{}:{}/{}'.format(protocol, host, port, self._HTTPRequest__path)
        self._HTTPRequest__requests_method = getattr(requests, self._HTTPRequest__method.lower())
        self._HTTPRequest__auth = auth.translate()
        self._HTTPRequest__headers = headers
        self._HTTPRequest__query = {}
        self._HTTPRequest__data = {}
        self._HTTPRequest__files = {}

    @property
    def method(self):
        return self._HTTPRequest__method

    @property
    def path(self):
        return '/{}'.format(self._HTTPRequest__path)

    def query_param(self, name, value):
        self._HTTPRequest__query[name] = value

    def data_param(self, name, value):
        self._HTTPRequest__data[name] = value

    def file_param(self, name, value):
        self._HTTPRequest__files[name] = value

    def perform(self):
        headers = {}
        headers.update(self._HTTPRequest__headers)
        headers.update({'Accept': [
                    'application/json']})
        resp = self._HTTPRequest__requests_method(url=self._HTTPRequest__url, auth=self._HTTPRequest__auth, headers={name:', '.join(value) for name, value in headers.items()}, params=self._HTTPRequest__query, data=self._HTTPRequest__data, files=self._HTTPRequest__files, verify=False)
        try:
            content = resp.json()
        except ValueError:
            content = None

        return HTTPResponse(resp.status_code, {name:value.split('\\s,') for name, value in resp.headers.items()}, content)


class HTTPResponse:
    """HTTPResponse"""

    def __init__(self, status_code, headers, content):
        self._HTTPResponse__status_code = status_code
        self._HTTPResponse__headers = headers
        self._HTTPResponse__content = content

    @property
    def status_code(self):
        """
                Response status code.
                
                :rtype:
                   int
                :return:
                   Status code value.
                """
        return self._HTTPResponse__status_code

    @property
    def headers(self):
        """
                Dictionary with lists of strings containing response headers.
                
                :rtype:
                   dict
                :return:
                   Headers dictionary.
                """
        return self._HTTPResponse__headers

    @property
    def content(self):
        """
                Dictionary that comes from decoding the JSON response body.
                
                :rtype:
                   dict
                :return:
                   Content dictionary.
                """
        return self._HTTPResponse__content


class HTTPNoneAuth:
    """HTTPNoneAuth"""

    def translate(self):
        """
                Translate it to the underlying implementation authentication.
                
                :return:
                   Translated authentication.
                """
        pass


class HTTPBasicAuth:
    """HTTPBasicAuth"""

    def __init__(self, user, password):
        self._HTTPBasicAuth__user = user
        self._HTTPBasicAuth__password = password

    def translate(self):
        """
                Translate it to the underlying implementation authentication.
                
                :return:
                   Translated authentication.
                """
        return requests.auth.HTTPBasicAuth(self._HTTPBasicAuth__user, self._HTTPBasicAuth__password)