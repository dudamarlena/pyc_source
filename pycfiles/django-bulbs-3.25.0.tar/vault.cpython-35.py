# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/utils/vault.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 845 bytes
import requests
from django.conf import settings
log = __import__('logging').getLogger(__name__)

def read(path):
    """Read a secret from Vault REST endpoint"""
    url = '{}/{}/{}'.format(settings.VAULT_BASE_URL.rstrip('/'), settings.VAULT_BASE_SECRET_PATH.strip('/'), path.lstrip('/'))
    headers = {'X-Vault-Token': settings.VAULT_ACCESS_TOKEN}
    resp = requests.get(url, headers=headers)
    if resp.ok:
        return resp.json()['data']
    log.error('Failed VAULT GET request: %s %s', resp.status_code, resp.text)
    raise Exception('Failed Vault GET request: {} {}'.format(resp.status_code, resp.text))