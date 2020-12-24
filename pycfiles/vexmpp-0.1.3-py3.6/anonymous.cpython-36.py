# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/suelta/mechanisms/anonymous.py
# Compiled at: 2017-02-05 18:43:13
# Size of source mod 2**32: 588 bytes
from ..sasl import Mechanism, register_mechanism

class ANONYMOUS(Mechanism):
    __doc__ = '\n    '

    def __init__(self, sasl, name):
        super(ANONYMOUS, self).__init__(sasl, name, 0)

    def get_values(self):
        """
        """
        return {}

    def process(self, challenge=None):
        """
        """
        return b'Anonymous, Suelta'

    def okay(self):
        """
        """
        return True

    def get_user(self):
        """
        """
        return 'anonymous'


register_mechanism('ANONYMOUS', 0, ANONYMOUS, use_hashes=False)