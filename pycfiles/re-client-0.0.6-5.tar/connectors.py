# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbielawa/rhat/release-engine/re-client/src/reclient/connectors.py
# Compiled at: 2015-01-13 16:44:38
import base64, requests, logging
out = logging.getLogger('reclient')

class Connectors(object):

    def __init__(self, connect_params, format, reclient_version='0.0.6'):
        """
        connect_params.keys() = ['auth', 'baseurl']
        """
        self.baseurl = connect_params['baseurl']
        self.auth = connect_params['auth']
        self.headers = {'User-Agent': 'reclient/%s' % reclient_version}
        if format == 'json':
            self.headers['content-type'] = 'application/json'
        else:
            self.headers['content-type'] = 'text/yaml'
        self._format_get_str = '?format=%s' % format

    def delete(self, url=''):
        """
        Deletes a playbook.
        """
        url = self.baseurl + url + self._format_get_str
        out.debug('DELETE request send to: %s' % url)
        response = requests.delete(url, headers=self.headers, verify=False, auth=self.auth)
        out.debug('Response:')
        try:
            out.debug(response.content)
        except Exception:
            out.debug(str(response.text))

        return response

    def get(self, url=''):
        """
        Gets a playbook.
        """
        url = self.baseurl + url + self._format_get_str
        out.debug('GET request send to: %s' % url)
        response = requests.get(url, headers=self.headers, verify=False, auth=self.auth)
        out.debug('Response:')
        try:
            out.debug(response.content)
        except Exception:
            out.debug(str(response.text))

        return response

    def post(self, url='', data={}):
        """
        Modifies a playbook.
        """
        url = self.baseurl + url + self._format_get_str
        out.debug('POST request send to: %s' % url)
        out.debug('Data: %s' % str(data))
        response = requests.post(url, data, headers=self.headers, verify=False, auth=self.auth)
        out.debug('Response:')
        try:
            out.debug(response.content)
        except Exception:
            out.debug(str(response.text))

        return response

    def put(self, url='', data={}):
        """
        Creates a playbook/
        """
        url = self.baseurl + url + self._format_get_str
        out.debug('PUT request send to: %s' % url)
        out.debug('Data: %s' % str(data))
        response = requests.put(url, data, headers=self.headers, verify=False, auth=self.auth)
        out.debug('Response:')
        try:
            out.debug(response.content)
        except Exception:
            out.debug(str(response.text))

        return response