# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thevpncompany/components/vpnapi.py
# Compiled at: 2020-01-05 04:37:40
# Size of source mod 2**32: 4259 bytes
"""
TheVPNCompany API implementation
"""
import logging, requests
__author__ = 'Ruben Rubio Rey'
__version__ = '0.1.0'
__license__ = 'MIT'
log = logging.getLogger(__name__)

class TheVPNCompanyClient:
    __doc__ = ' A Client implementing of TheVPNCompany API '

    def __init__(self, url: str, api_key: str):
        self._url = url
        self.api_key = api_key

    def action_server_requested(self, server_id) -> bool:
        url = self._url + '/api/v1/server/' + server_id + '/action'
        headers = {'apiKey': self.api_key}
        body = {'action': 'CreationRequest'}
        log.debug('POST to %s: data: %s' % (url, body))
        response = requests.post(url, data=body, headers=headers)
        log.debug('Response %s : data: %s' % (response.status_code, response.json()))
        if response.status_code == 200:
            return True
        else:
            log.error("Can't create server. HTTP Code: %s, Response: %s" % (response.status_code, response.json()))
            return False

    def action_server_failed(self, server_id) -> bool:
        url = self._url + '/api/v1/server/' + server_id + '/action'
        headers = {'apiKey': self.api_key}
        body = {'action': 'CreationFailed'}
        log.debug('POST to %s: data: %s' % (url, body))
        response = requests.post(url, data=body, headers=headers)
        log.debug('Response %s : data: %s' % (response.status_code, response.json()))
        if response.status_code == 200:
            return True
        else:
            log.error("Can't create server. HTTP Code: %s, Response: %s" % (response.status_code, response.json()))
            return False

    def action_server_completed(self, server_id, id_external, ipv4) -> bool:
        url = self._url + '/api/v1/server/' + server_id + '/action'
        headers = {'apiKey': self.api_key}
        body = {'action': 'CreationReady', 
         'id_external': id_external, 
         'ipv4': ipv4}
        log.debug('POST to %s: data: %s' % (url, body))
        response = requests.post(url, data=body, headers=headers)
        log.debug('Response %s : data: %s' % (response.status_code, response.json()))
        if response.status_code == 200:
            return True
        else:
            log.error("Can't create server. HTTP Code: %s, Response: %s" % (response.status_code, response.json()))
            return False

    def action_save_certificates(self, email, client_private, client_public, ca, static_key):
        headers = {'apiKey': self.api_key}
        body = {'client_private': client_private, 
         'client_public': client_public, 
         'ca': ca, 
         'static_key': static_key}
        url = self._url + '/api/v1/user/' + email + '/certs'
        log.debug('PUT to %s: data: %s' % (url, body))
        response = requests.put(url, data=body, headers=headers)
        log.debug('Response %s : data: %s' % (response.status_code, response.json()))
        if response.status_code == 200:
            return True
        else:
            log.error("Can't create server. HTTP Code: %s, Response: %s" % (response.status_code, response.json()))
            return False

    def is_user_valid(self, user_id):
        url = self._url + '/api/v1/user/' + user_id
        log.debug('GET %s' % url)
        response = requests.get(url)
        log.debug('Response %s : data: %s' % (response.status_code, response.json()))
        json_response = response.json()
        if json_response['access'] == 0:
            log.debug('Access granted')
            return True
        else:
            log.debug('Access prohibited')
            return False