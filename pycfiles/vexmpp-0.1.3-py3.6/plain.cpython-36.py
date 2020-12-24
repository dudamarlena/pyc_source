# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/suelta/mechanisms/plain.py
# Compiled at: 2017-02-05 18:19:17
# Size of source mod 2**32: 1638 bytes
from ..util import bytes
from ..sasl import Mechanism, register_mechanism
from ..exceptions import SASLCancelled

class PLAIN(Mechanism):
    __doc__ = '\n    '

    def __init__(self, sasl, name):
        super(PLAIN, self).__init__(sasl, name)
        if not self.sasl.tls_active():
            if not self.sasl.sec_query(self, '-ENCRYPTION, PLAIN'):
                raise SASLCancelled(self.sasl, self)
        else:
            if not self.sasl.sec_query(self, '+ENCRYPTION, PLAIN'):
                raise SASLCancelled(self.sasl, self)
        self.check_values(['username', 'password'])

    def prep(self):
        """
        Prepare for processing by deleting the password if
        the user has not approved storing it in the clear.
        """
        if 'savepass' not in self.values:
            if self.sasl.sec_query(self, 'CLEAR-PASSWORD'):
                self.values['savepass'] = True
        if 'savepass' not in self.values:
            del self.values['password']
        return True

    def process(self, challenge=None):
        """
        Process a challenge request and return the response.

        :param challenge: A challenge issued by the server that
                          must be answered for authentication.
        """
        user = bytes(self.values['username'])
        password = bytes(self.values['password'])
        return b'\x00' + user + b'\x00' + password

    def okay(self):
        """
        Mutual authentication is not supported by PLAIN.

        :returns: ``True``
        """
        return True


register_mechanism('PLAIN', 1, PLAIN, use_hashes=False)