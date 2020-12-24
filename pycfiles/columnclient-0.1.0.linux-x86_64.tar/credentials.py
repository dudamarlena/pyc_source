# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/columnclient/credentials.py
# Compiled at: 2017-08-21 17:07:37
import json, urlparse

class CredentialsManager(object):

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = urlparse.urljoin(base_url, 'credentials')

    def vault_decrypt(self, value):
        creds_url = ('{0}?value={1}').format(self.base_url, value)
        response = self.session.get(creds_url)
        return json.loads(response.text)

    def vault_encrypt(self, value):
        data_in_json = json.dumps({'value': value})
        headers = {'content-type': 'application/json'}
        response = self.session.put(self.base_url, data=data_in_json, headers=headers)
        return json.loads(response.text)