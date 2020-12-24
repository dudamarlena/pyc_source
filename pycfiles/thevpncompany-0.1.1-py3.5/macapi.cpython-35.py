# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thevpncompany/components/macapi.py
# Compiled at: 2020-01-06 23:56:06
# Size of source mod 2**32: 3738 bytes
"""
ManageaCloud API partial implementation
"""
import logging, requests, json, time
__author__ = 'Ruben Rubio Rey'
__version__ = '0.1.0'
__license__ = 'MIT'
log = logging.getLogger(__name__)

class ManageacloudClient:
    __doc__ = ' A Client with a partial implementation of ManageaCloud API '

    def __init__(self, auth: str, env: str):
        self._api_auth = auth
        self.env = env

    def create_server(self, hardware: str, cookbook_tag: str, location: str, servername: str, provider: str, repository_conf: str, repository_private_key: str) -> str:
        url = 'https://manageacloud.com/api/v1/instance'
        if self.env == 'prod':
            deployment = 'production'
        else:
            deployment = 'testing'
        body = {'hardware': hardware, 
         'cookbook_tag': cookbook_tag, 
         'location': location, 
         'deployment': deployment, 
         'servername': servername, 
         'provider': provider, 
         'environments': [
                          {'PRIVATE_KEY': '"' + repository_private_key + '"'},
                          {'REPOSITORY': '"' + repository_conf + '"'}]}
        log.debug('POST to %s: data: %s' % (url, body))
        response = requests.post(url, data=json.dumps(body), headers=self._get_headers())
        log.debug('Response %s : data: %s' % (response.status_code, response.json()))
        if response.status_code == 202:
            return response.json()['id']
        log.error("Can't create server. HTTP Code: %s, Response: %s" % (response.status_code, response.json()))

    def wait(self, mac_id) -> bool:
        log.debug('[%s] Waiting server to be available' % mac_id)
        url = 'https://manageacloud.com/api/v1/instances'
        servers_response = requests.get(url, headers=self._get_headers())
        log.debug('Servers Code: %s, Response: %s' % (servers_response.status_code, servers_response.json()))
        servers = servers_response.json()
        max_loops = 60
        loop = 0
        while loop < max_loops:
            for server in servers:
                servers_response = requests.get(url, headers=self._get_headers())
                servers = servers_response.json()
                found = False
                if server['id'] == mac_id:
                    found = True
                    log.debug("[%s] server found, status '%s', waiting to be ready ..." % (mac_id, server['status']))
                    if server['status'].startswith('Ready'):
                        log.info('[%s] Server is ready' % mac_id)
                        return server
                    if server['status'] == 'Creation failed':
                        log.error('[%s] Server creation failed' % mac_id)
                        return
                    if not found:
                        log.error('[%s] Server not found')
                        return
                    time.sleep(10)
                    loop += 1

        log.error('[%s] Time Out')

    def _get_headers(self) -> {}:
        return {'content-type': 'application/json', 
         'Authorization': 'ApiKey ' + self._api_auth}