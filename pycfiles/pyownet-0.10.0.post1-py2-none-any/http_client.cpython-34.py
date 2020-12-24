# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/commons/http_client.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 9053 bytes
import requests, json
from pyowm.caches import nullcache
from pyowm.commons.enums import ImageTypeEnum
from pyowm.exceptions import api_call_error, api_response_error, parse_response_error
from pyowm.weatherapi25.configuration25 import API_AVAILABILITY_TIMEOUT, API_SUBSCRIPTION_SUBDOMAINS, VERIFY_SSL_CERTS

class HttpClient(object):

    def __init__(self, timeout=API_AVAILABILITY_TIMEOUT, cache=None, use_ssl=False, verify_ssl_certs=VERIFY_SSL_CERTS):
        self.timeout = timeout
        if cache is None:
            self.cache = nullcache.NullCache()
        else:
            self.cache = cache
        self.use_ssl = use_ssl
        self.verify_ssl_certs = verify_ssl_certs

    def get_json(self, uri, params=None, headers=None):
        try:
            resp = requests.get(uri, params=params, headers=headers, timeout=self.timeout, verify=self.verify_ssl_certs)
        except requests.exceptions.SSLError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise api_call_error.APICallTimeoutError('API call timeouted')

        HttpClient.check_status_code(resp.status_code, resp.text)
        try:
            return (resp.status_code, resp.json())
        except:
            raise parse_response_error.ParseResponseError('Impossible to parseAPI response data')

    def get_png(self, uri, params=None, headers=None):
        if headers is None:
            headers = {'Accept': ImageTypeEnum.PNG.mime_type}
        else:
            headers.update({'Accept': ImageTypeEnum.PNG.mime_type})
        try:
            resp = requests.get(uri, stream=True, params=params, headers=headers, timeout=self.timeout, verify=self.verify_ssl_certs)
        except requests.exceptions.SSLError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise api_call_error.APICallTimeoutError('API call timeouted')

        HttpClient.check_status_code(resp.status_code, resp.text)
        try:
            return (resp.status_code, resp.content)
        except:
            raise parse_response_error.ParseResponseError('Impossible to parseAPI response data')

    def get_geotiff(self, uri, params=None, headers=None):
        if headers is None:
            headers = {'Accept': ImageTypeEnum.GEOTIFF.mime_type}
        else:
            headers.update({'Accept': ImageTypeEnum.GEOTIFF.mime_type})
        try:
            resp = requests.get(uri, stream=True, params=params, headers=headers, timeout=self.timeout, verify=self.verify_ssl_certs)
        except requests.exceptions.SSLError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise api_call_error.APICallTimeoutError('API call timeouted')

        HttpClient.check_status_code(resp.status_code, resp.text)
        try:
            return (resp.status_code, resp.content)
        except:
            raise parse_response_error.ParseResponseError('Impossible to parseAPI response data')

    def cacheable_get_json(self, uri, params=None, headers=None):
        cached_url_key = requests.Request('GET', uri, params=params).prepare().url
        cached = self.cache.get(cached_url_key)
        if cached:
            return (200, cached)
        status_code, data = self.get_json(uri, params=params, headers=headers)
        json_string = json.dumps(data)
        self.cache.set(cached_url_key, json_string)
        return (
         status_code, json_string)

    def post(self, uri, params=None, data=None, headers=None):
        try:
            resp = requests.post(uri, params=params, json=data, headers=headers, timeout=self.timeout, verify=self.verify_ssl_certs)
        except requests.exceptions.SSLError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise api_call_error.APICallTimeoutError('API call timeouted')

        HttpClient.check_status_code(resp.status_code, resp.text)
        try:
            json_data = resp.json()
        except:
            json_data = {}

        return (
         resp.status_code, json_data)

    def put(self, uri, params=None, data=None, headers=None):
        try:
            resp = requests.put(uri, params=params, json=data, headers=headers, timeout=self.timeout, verify=self.verify_ssl_certs)
        except requests.exceptions.SSLError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise api_call_error.APICallTimeoutError('API call timeouted')

        HttpClient.check_status_code(resp.status_code, resp.text)
        try:
            json_data = resp.json()
        except:
            json_data = {}

        return (
         resp.status_code, json_data)

    def delete(self, uri, params=None, data=None, headers=None):
        try:
            resp = requests.delete(uri, params=params, json=data, headers=headers, timeout=self.timeout, verify=self.verify_ssl_certs)
        except requests.exceptions.SSLError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.ConnectionError as e:
            raise api_call_error.APIInvalidSSLCertificateError(str(e))
        except requests.exceptions.Timeout:
            raise api_call_error.APICallTimeoutError('API call timeouted')

        HttpClient.check_status_code(resp.status_code, resp.text)
        try:
            json_data = resp.json()
        except:
            json_data = None

        return (resp.status_code, json_data)

    @classmethod
    def check_status_code(cls, status_code, payload):
        if status_code < 400:
            return
        if status_code == 400:
            raise api_call_error.APICallError(payload)
        else:
            if status_code == 401:
                raise api_response_error.UnauthorizedError('Invalid API Key provided')
            else:
                if status_code == 404:
                    raise api_response_error.NotFoundError('Unable to find the resource')
                else:
                    if status_code == 502:
                        raise api_call_error.BadGatewayError('Unable to contact the upstream server')
                    else:
                        raise api_call_error.APICallError(payload)

    @classmethod
    def is_success(cls, status_code):
        if 200 <= status_code < 300:
            return True
        return False

    @classmethod
    def to_url(cls, API_endpoint_URL, API_key, subscription_type, use_ssl=False):
        params = dict()
        if API_key is not None:
            params['APPID'] = API_key
        escaped_url = HttpClient._escape_subdomain(API_endpoint_URL, subscription_type)
        url = HttpClient._fix_schema(escaped_url, use_ssl)
        r = requests.Request('GET', url, params=params).prepare()
        return r.url

    @classmethod
    def _fix_schema(cls, url, use_ssl):
        if use_ssl:
            return url.replace('http', 'https')
        return url

    @classmethod
    def _escape_subdomain(cls, API_endpoint_URL, subscription_type):
        if subscription_type is None:
            return API_endpoint_URL
        try:
            return API_endpoint_URL % (API_SUBSCRIPTION_SUBDOMAINS[subscription_type],)
        except KeyError:
            raise ValueError('Unexistent API subscription type')
        except TypeError:
            return API_endpoint_URL

    def __repr__(self):
        return '<%s.%s - timeout=%s - cache=%s>' % (
         __name__, self.__class__.__name__, repr(self.timeout),
         str(self.cache) if self.cache is not None else 'None')