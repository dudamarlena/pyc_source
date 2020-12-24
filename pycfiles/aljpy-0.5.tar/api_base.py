# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/apiclient/api_base.py
# Compiled at: 2015-12-07 06:43:57
import logging, requests
from six.moves.urllib.parse import urlencode
from opensearchsdk.apiclient import exceptions
from opensearchsdk.utils import prepare_url
USER_AGENT = 'ali-opensearch-python-client'
_logger = logging.getLogger(__name__)

class HTTPClient(object):
    """HTTP client for sending request to server"""

    def __init__(self, base_url):
        self.base_url = base_url

    def request(self, method, url, **kwargs):
        url = self.base_url + url
        kwargs.setdefault('headers', {})
        kwargs['headers']['User-Agent'] = USER_AGENT
        kwargs['headers']['Content-Type'] = 'application/x-www-form-urlencoded'
        resp = requests.request(method, url, **kwargs)
        try:
            resp.raise_for_status()
        except requests.RequestException as e:
            if resp.status_code == 404:
                exc_type = exceptions.NotFoundException
            else:
                exc_type = exceptions.HttpException
            raise exc_type(e, details=self._parse_error_resp(resp), status_code=resp.status_code)

        try:
            resp_body = resp.json()
        except ValueError:
            raise exceptions.InvalidResponse(response=resp)

        return resp_body

    def _parse_error_resp(self, resp):
        try:
            jresp = resp.json()
            return jresp
        except ValueError:
            pass

        return resp.text


class Manager(object):

    def __init__(self, api, resource_url):
        self.api = api
        self.resource_url = resource_url

    def send_request(self, method, spec_url, body):
        key = self.api.key
        key_id = self.api.key_id
        body['Signature'] = prepare_url.get_signature(method, body, key, key_id)
        final_url = self.resource_url + spec_url
        return self.api.http_client.request(method, final_url, data=body)

    def send_get(self, body, spec_url=''):
        key = self.api.key
        key_id = self.api.key_id
        body['Signature'] = prepare_url.get_signature('GET', body, key, key_id)
        encoded_url = urlencode(body)
        final_url = self.resource_url + spec_url + '?' + encoded_url
        return self.api.http_client.request('GET', final_url)

    def send_post(self, body, spec_url=''):
        return self.send_request('POST', spec_url, body)