# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/clients/http.py
# Compiled at: 2020-04-14 15:37:55
# Size of source mod 2**32: 11755 bytes
from typing import *
from typing import BinaryIO
from enum import Enum
import os
from datalogue.utils import Json
from datalogue.errors import DtlError
import logging, requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests import Response
from datalogue.models.organization import _users_from_payload
from pathlib import Path
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logger = logging.getLogger('_HttpClient')

class HttpMethod(Enum):
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'


class MultiPartFile:

    def __init__(self, name: str, file: BinaryIO):
        self.name = name
        self.file = file


class MultiPartData:

    def __init__(self, name: str, data: str):
        self.name = name
        self.data = data


class _HttpClient:
    __doc__ = '\n    Class that Abstracts aways requests and makes it use type safe.\n    It also prepares all the requests to be used authenticated to the API\n    '

    def __init__(self, uri: str, verify_certificate: bool=True):
        self.uri = uri
        self.http_session = requests.Session()
        self.verify_certificate = verify_certificate
        if not verify_certificate:
            logger.info('SSL Certification verification is disabled.')

    def get_csrf(self):
        public_url = self.uri
        if os.environ.get('DTL_PUBLIC_URL') is not None:
            public_url = os.environ.get('DTL_PUBLIC_URL')
        self.http_session.headers.update({'Origin': public_url.strip('/api')})
        url = self.uri + '/health'
        res = self.http_session.get(url, verify=(self.verify_certificate))
        if 'csrf-token' in res.headers:
            self.http_session.cookies.set('csrf-token', res.headers['csrf-token'])
            self.http_session.headers.update({'X-Csrf-Token': res.headers['csrf-token']})

    def login(self, username: str, password: str) -> Union[(DtlError, None)]:
        """
        Sets the cookie for the client to use

        :param username: Username of user to login
        :param password: Password of user to login
        :return: Nothing
        """
        self.get_csrf()
        url = self.uri + '/signin'
        try:
            res = self.http_session.post(url,
              json={'email':username, 
             'password':password},
              allow_redirects=False,
              verify=(self.verify_certificate))
        except requests.ConnectionError:
            return DtlError('There was a connection error trying to reach: %s' % self.uri)
        except requests.HTTPError:
            return DtlError('There was an HTTP error trying to reach: %s' % self.uri)
        except requests.URLRequired:
            return DtlError('%s is not a valid endpoint.' % self.uri)
        except requests.Timeout:
            return DtlError('The request timed out')
        else:
            if res.status_code != 201:
                if res.status_code != 302:
                    if res.status_code != 200:
                        return DtlError('Authentication failed - %s : %s' % (str(res.status_code), res.text))
            if res.status_code == 503 or res.status_code == 504:
                return DtlError('The service is not available. StatusCode: %s, Body: %s' % (str(res.status_code), res.text))
            else:
                return

    def signup(self, first_name, last_name, email, password, accept_terms):
        """
        Allows
        :param first_name: First name of user to be registered
        :param last_name: Last name of user to be registered
        :param email: Email of user to be registered
        :param password: Password of user to be registered
        :param accept_terms: Whether user accepts the term of service here : https://assets.website-files.com/5c980fa2de94e8f79f047ded/5cd0e4d60880b51cb361ae7a_Terms%20of%20Service.pdf
        :return: A User object
        """
        print("By calling this action, you've agreed to the terms of service as set forth here : https://assets.website-files.com/5c980fa2de94e8f79f047ded/5cd0e4d60880b51cb361ae7a_Terms%20of%20Service.pdf")
        if not accept_terms:
            return DtlError('Terms & Conditions for registration are not accepted')
        url = self.uri + '/signup'
        self.get_csrf()
        try:
            res = self.http_session.post(url, json={'email':email, 
             'firstName':first_name, 
             'lastName':last_name, 
             'password':password},
              verify=(self.verify_certificate))
        except requests.ConnectionError:
            return DtlError('There was a connection error trying to reach: %s' % self.uri)
        except requests.HTTPError:
            return DtlError('There was an HTTP error trying to reach: %s' % self.uri)
        except requests.URLRequired:
            return DtlError('%s is not a valid endpoint.' % self.uri)
        except requests.Timeout:
            return DtlError('The request timed out')
        else:
            if res.status_code == 200:
                if res.headers.get('content-type') == 'application/json':
                    return _users_from_payload(res.json())
                else:
                    return DtlError('Cannot parse response, unknown type')
            else:
                if res.status_code == 503:
                    return DtlError('The service is not available')
                else:
                    if res.status_code == 504:
                        return DtlError('The service is not available: Gateway Timeout!')
                    return DtlError(res.text)

    @staticmethod
    def _handle_status_code(request_uri: str, res: Response) -> Union[(DtlError, None)]:
        """
        Return a proper DtlError depending on the status code of the Response

        :param request_uri: uri of th request that was made
        :param res: Response received to the request
        :return: an Error or None if the status doesn't warrant returning an error
        """
        if res.status_code == 400:
            return DtlError('Invalid Request to %s returned 400, body res: %s' % (request_uri, res.text))
        else:
            if res.status_code == 401:
                return DtlError('It looks like you are not logged in, please login')
            else:
                if res.status_code == 403:
                    return DtlError(f"Authorization error. Make sure you're authorized to do this operation. Msg: {res.text}")
                else:
                    if res.status_code == 404:
                        return DtlError('Route not found %s' % request_uri)
                    if res.status_code == 413:
                        return DtlError('Body is too big, please limit uploads to 1 Go')
                    if res.status_code == 500:
                        return res.text or DtlError('Internal Server error')
                    else:
                        return DtlError(res.text)
                if res.status_code == 503:
                    return DtlError('The service is not available')
            if res.status_code == 504:
                return DtlError('The service is not available: Gateway timeout!')

    def post_multipart_data(self, path: str, files: List[MultiPartFile], data: List[MultiPartData]) -> Union[(DtlError, Response)]:
        headers = {'content-type': 'multipart/form-data'}
        files_payload = {}
        for f in files:
            files_payload[f.name] = f.file

        data_payload = {}
        for d in data:
            data_payload[d.name] = d.data

        request_uri = self.uri + path
        req = requests.Request((HttpMethod.POST.value),
          request_uri,
          files=files_payload,
          data=data_payload)
        prepped = self.http_session.prepare_request(req)
        res = self.http_session.send(prepped, verify=(self.verify_certificate))
        e = self._handle_status_code(request_uri, res)
        if isinstance(e, DtlError):
            return e
        else:
            content_type_header = res.headers.get('content-type')
            if len(res.text) > 0:
                if content_type_header == 'application/json':
                    return res.json()
            return res.text

    def post_binary(self, path: str, file: BinaryIO, params: Optional[dict]=None) -> Union[(DtlError, Response)]:
        """
        Makes a post request with the content being a binary file that will be uploaded chunk by chunk

        :param path: path uri to the datastore
        :param file: iterator that is going to generate the binary data
        :param params: parameters to be used in the request
        :return:
        """
        request_uri = self.uri + path
        req = requests.Request((HttpMethod.POST.value), request_uri, data=file, params=params)
        prepped = self.http_session.prepare_request(req)
        prepped.headers['Content-Type'] = 'application/octet-stream'
        res = self.http_session.send(prepped, verify=(self.verify_certificate))
        e = _HttpClient._handle_status_code(request_uri, res)
        if isinstance(e, DtlError):
            return e
        else:
            return res

    def make_authed_request(self, path: str, method: HttpMethod, body: Optional[dict]=None, params: Optional[dict]=None, stream=False) -> Union[(DtlError, Json, Response)]:
        res = self.execute_authed_request(path, method, body, params, stream)
        request_uri = self.uri + path
        e = self._handle_status_code(request_uri, res)
        if isinstance(e, DtlError):
            return e
        content_type_header = res.headers.get('content-type')
        if stream:
            return res
        else:
            if len(res.text) > 0:
                if content_type_header == 'application/json':
                    return res.json()
            return res.text

    def execute_authed_request(self, path: str, method: HttpMethod, body: Optional[dict]=None, params: Optional[dict]=None, stream=False) -> Union[(DtlError, Response)]:
        """
        Makes a request to the API give the url

        :param path: path to access the datastore below the host
        :param method: parameter to indicate HTTP Method to be used in the request
        :param body: body to be sent along with the request
        :param params: query parameters, to be fed with a dictionary
        :param stream: boolean to activate streaming the content of the response, this will delay the retrieval of
        the body until .content is called.
        :return: Request response in raw format
        """
        self.get_csrf()
        request_uri = self.uri + path
        req = requests.Request((method.value), request_uri, json=body, params=params)
        prepped = self.http_session.prepare_request(req)
        res = self.http_session.send(prepped, stream=stream, verify=(self.verify_certificate))
        return res

    def put_binary(self, path: str, file: BinaryIO, params: Optional[dict]=None) -> Union[(DtlError, Response)]:
        """
        Makes a put request with the content being a binary file that will be uploaded chunk by chunk

        :param path: path uri to the datastore
        :param file: iterator that is going to generate the binary data
        :param params: parameters to be used in the request
        :return:
        """
        self.get_csrf()
        request_uri = self.uri + path
        req = requests.Request((HttpMethod.PUT.value), request_uri, data=file, params=params)
        prepped = self.http_session.prepare_request(req)
        prepped.headers['Content-Type'] = 'application/octet-stream'
        res = self.http_session.send(prepped, verify=(self.verify_certificate))
        e = _HttpClient._handle_status_code(request_uri, res)
        if isinstance(e, DtlError):
            return e
        else:
            return res