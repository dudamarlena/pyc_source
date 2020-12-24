# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/suelta/mechanisms/facebook_platform.py
# Compiled at: 2017-02-05 18:38:31
# Size of source mod 2**32: 1076 bytes
from ..util import bytes
from ..sasl import Mechanism, register_mechanism

class X_FACEBOOK_PLATFORM(Mechanism):

    def __init__(self, sasl, name):
        super(X_FACEBOOK_PLATFORM, self).__init__(sasl, name)
        self.check_values(['access_token', 'api_key'])

    def process(self, challenge=None):
        if challenge is not None:
            values = {}
            for kv in challenge.split(b'&'):
                key, value = kv.split(b'=')
                values[key] = value

            resp_data = {b'method':values[b'method'], 
             b'v':b'1.0', 
             b'call_id':b'1.0', 
             b'nonce':values[b'nonce'], 
             b'access_token':self.values['access_token'], 
             b'api_key':self.values['api_key']}
            resp = '&'.join(['%s=%s' % (k, v) for k, v in resp_data.items()])
            return bytes(resp)
        else:
            return b''

    def okay(self):
        return True


register_mechanism('X-FACEBOOK-PLATFORM', 40, X_FACEBOOK_PLATFORM, use_hashes=False)