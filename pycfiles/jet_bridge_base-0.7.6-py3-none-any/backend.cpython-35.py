# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/utils/backend.py
# Compiled at: 2020-03-04 16:40:12
# Size of source mod 2**32: 1662 bytes
import requests
from jet_bridge_base import settings
from jet_bridge_base.configuration import configuration
from jet_bridge_base.logger import logger

def api_method_url(method):
    return '{}/{}'.format(settings.API_BASE_URL, method)


def is_token_activated(project_token):
    if not project_token:
        return False
    url = api_method_url('project_tokens/{}/'.format(project_token))
    headers = {'User-Agent': '{} v{}'.format(configuration.get_type(), configuration.get_version())}
    r = requests.request('GET', url, headers=headers)
    success = 200 <= r.status_code < 300
    if not success:
        return False
    result = r.json()
    return bool(result.get('activated'))


def project_auth(token, project_token, permission=None):
    if not project_token:
        return {'result': False}
    url = api_method_url('project_auth/')
    data = {'project_token': project_token, 
     'token': token}
    headers = {'User-Agent': '{} v{}'.format(configuration.get_type(), configuration.get_version())}
    if permission:
        data.update(permission)
    r = requests.request('POST', url, data=data, headers=headers)
    success = 200 <= r.status_code < 300
    if not success:
        logger.error('Project Auth request error: %d %s', r.status_code, r.reason)
        return {'result': False}
    result = r.json()
    if result.get('access_disabled'):
        return {'result': False, 
         'warning': result.get('warning')}
    return {'result': True, 
     'warning': result.get('warning')}