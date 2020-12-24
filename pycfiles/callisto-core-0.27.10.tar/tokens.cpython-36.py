# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/accounts/tokens.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 561 bytes
import logging
from django.core.signing import Signer
logger = logging.getLogger(__name__)

class StudentVerificationTokenGenerator(object):

    def make_token(self, user):
        """
        makes a verification token for a user

        Student account verification is spam prevention,
        rather than a security concern. So we can
        make the token the user's signed uuid
        """
        return Signer().sign(str(user.account.uuid)).split(':')[(-1)]

    def check_token(self, user, token):
        return bool(self.make_token(user) == token)