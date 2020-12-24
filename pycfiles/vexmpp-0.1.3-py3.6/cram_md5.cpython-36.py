# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/suelta/mechanisms/cram_md5.py
# Compiled at: 2017-02-05 18:17:36
# Size of source mod 2**32: 1446 bytes
import hmac
from ..util import hash, bytes
from ..sasl import Mechanism, register_mechanism
from ..exceptions import SASLCancelled

class CRAM_MD5(Mechanism):
    __doc__ = '\n    '

    def __init__(self, sasl, name):
        super(CRAM_MD5, self).__init__(sasl, name, 2)
        self.hash = hash(name[5:])
        if self.hash is None:
            raise SASLCancelled(self.sasl, self)
        if not self.sasl.tls_active():
            if not self.sasl.sec_query(self, 'CRAM-MD5'):
                raise SASLCancelled(self.sasl, self)

    def prep(self):
        """
        """
        if 'savepass' not in self.values:
            if self.sasl.sec_query(self, 'CLEAR-PASSWORD'):
                self.values['savepass'] = True
        if 'savepass' not in self.values:
            del self.values['password']

    def process(self, challenge):
        """
        """
        if challenge is None:
            return
        else:
            self.check_values(['username', 'password'])
            username = bytes(self.values['username'])
            password = bytes(self.values['password'])
            mac = hmac.HMAC(key=password, digestmod=(self.hash))
            mac.update(challenge)
            return username + b' ' + bytes(mac.hexdigest())

    def okay(self):
        """
        """
        return True

    def get_user(self):
        """
        """
        return self.values['username']


register_mechanism('CRAM-', 20, CRAM_MD5)