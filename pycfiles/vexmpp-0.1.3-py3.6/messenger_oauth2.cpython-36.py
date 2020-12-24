# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/suelta/mechanisms/messenger_oauth2.py
# Compiled at: 2017-02-05 18:38:24
# Size of source mod 2**32: 490 bytes
from ..util import bytes
from ..sasl import Mechanism, register_mechanism

class X_MESSENGER_OAUTH2(Mechanism):

    def __init__(self, sasl, name):
        super(X_MESSENGER_OAUTH2, self).__init__(sasl, name)
        self.check_values(['access_token'])

    def process(self, challenge=None):
        return bytes(self.values['access_token'])

    def okay(self):
        return True


register_mechanism('X-MESSENGER-OAUTH2', 10, X_MESSENGER_OAUTH2, use_hashes=False)