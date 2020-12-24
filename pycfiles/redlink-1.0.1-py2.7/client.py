# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redlink/client.py
# Compiled at: 2015-11-07 07:42:52
from . import __version__, __agent__
import requests, json
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

class RedlinkClient(object):
    """
    Redlink generic client, internally handling all details of the communication with the Redlink API.
    """
    endpoint = 'https://api.redlink.io'
    datahub = 'http://data.redlink.io'
    param_key = 'key'
    param_in = 'in'
    param_out = 'out'

    def __init__(self, key):
        """
        @param key: api key
        @return:
        """
        self.key = key
        self.version = self._get_api_version()
        self.user_agent = __agent__
        status = self.get_status()
        if not (status and status['accessible']):
            raise ValueError('invalid key')
        else:
            self.status = status

    def _build_url(self, endpoint='', params={}):
        if len(endpoint) > 0 and not endpoint.startswith('/'):
            endpoint = '/%' % endpoint
        url = '%s/%s%s?%s=%s' % (self.endpoint, self.version, endpoint, self.param_key, self.key)
        for k, v in params.items():
            url += '&%s=%s' % (k, quote_plus(v))

        return url

    def _get_api_version(self):
        versions = __version__.split('.')
        return '%s.%s' % (versions[0], versions[1])

    def get_status(self):
        """
        Get api status of the current key

        @rtype: dict
        @return: status
        """
        response = self._get(self._build_url(), accept='application/json')
        if response.status_code != 200:
            return
        else:
            return json.loads(response.text)
            return

    def _get(self, resource, accept=None):
        headers = {'User-Agent': self.user_agent}
        if accept:
            headers['Accept'] = accept
        return requests.get(resource, headers=headers)

    def _post(self, resource, payload=None, contentType=None, accept=None):
        headers = {'User-Agent': self.user_agent}
        if contentType:
            headers['Content-Type'] = contentType
        if accept:
            headers['Accept'] = accept
        return requests.post(resource, data=payload, headers=headers)

    def _put(self, resource, payload=None, contentType=None, accept=None):
        headers = {'User-Agent': self.user_agent}
        if contentType:
            headers['Content-Type'] = contentType
        if accept:
            headers['Accept'] = accept
        return requests.put(resource, data=payload, headers=headers)

    def _delete(self, resource):
        return requests.delete(resource)