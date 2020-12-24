# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/entity_statement/statement.py
# Compiled at: 2019-09-02 11:14:07
# Size of source mod 2**32: 1216 bytes
import logging
from cryptojwt.jwt import utc_time_sans_frac
__author__ = 'roland'
logger = logging.getLogger(__name__)

class Statement(object):
    __doc__ = '\n    Class in which to store the parse result from applying metadata policies on a\n    metadata statement.\n    '

    def __init__(self, exp=0, signing_keys=None, verified_chain=None):
        """
        :param exp: Expiration time
        """
        self.fo = ''
        self.iss_path = []
        self.err = {}
        self.metadata = {}
        self.exp = exp
        self.signing_keys = signing_keys
        self.verified_chain = verified_chain

    def keys(self):
        return self.metadata.keys()

    def items(self):
        return self.metadata.items()

    def __getitem__(self, item):
        return self.metadata[item]

    def __contains__(self, item):
        return item in self.metadata

    def claims(self):
        """
        The result after flattening the statements
        """
        return self.metadata

    def is_expired(self):
        now = utc_time_sans_frac()
        if self.exp < now:
            logger.debug('is_expired: {} < {}'.format(self.exp, now))
            return True
        return False