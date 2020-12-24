# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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