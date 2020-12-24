# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seb/git/kipartman/kipartman/rest.py
# Compiled at: 2017-08-10 04:30:16
# Size of source mod 2**32: 586 bytes
import swagger_client
base_url = 'http://localhost:8200/api'
client_id = ''
client_secret = ''
unauthenticated_client = swagger_client.ApiClient(base_url)
client = swagger_client.ApiClient(base_url)
api = swagger_client.DefaultApi(client)
model = swagger_client