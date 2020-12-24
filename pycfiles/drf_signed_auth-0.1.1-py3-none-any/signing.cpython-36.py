# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marcgibbons/projects/drf_signed_auth/drf_signed_auth/signing.py
# Compiled at: 2017-10-08 11:15:44
# Size of source mod 2**32: 1205 bytes
"""
Contains cryptographic signing of the user model
"""
from django.contrib.auth import get_user_model
from django.core import signing
from . import settings

class UserSigner:
    __doc__ = '\n    Signs/unsigns user object with an expiry.\n    '
    signer_class = signing.TimestampSigner

    def sign(self, user):
        """
        Creates signatures for user object.
        """
        signer = self.signer_class()
        data = {'user_id':user.pk, 
         'username':user.get_username()}
        return signer.sign(signing.dumps(data))

    def unsign(self, signature, max_age=settings.SIGNED_URL_TTL):
        """
        Returns fresh user object for a valid signature.
        """
        User = get_user_model()
        signer = self.signer_class()
        data = signing.loads(signer.unsign(signature, max_age))
        if not isinstance(data, dict):
            raise signing.BadSignature()
        try:
            return (User.objects.get)(**{'pk': data.get('user_id'), 
             User.USERNAME_FIELD: data.get('username')})
        except User.DoesNotExist:
            raise signing.BadSignature()