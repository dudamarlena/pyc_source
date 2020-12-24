# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/silent/client.py
# Compiled at: 2018-03-03 08:58:58
# Size of source mod 2**32: 774 bytes
from .wrapper import Network
import json

class Client:

    def __init__(self, args):
        self._args = args
        self._payload = {}
        self._response = None

    def _api_request(self):
        self._response = Network.post_request(self._payload)

    def run(self):
        self._payload['filename'] = self._args.file
        self._payload['expiry'] = self._args.expiry
        self._api_request()
        print('\n {0}'.format(self._response.status_code))
        print(self._response.reason)
        res = json.loads(self._response.text)
        if res['success']:
            print('Your link to share : {0}'.format(res['link']))
            print('Expires in {0}'.format(res['expiry']))
        else:
            print('Upload failed, try again :(')