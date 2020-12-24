# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/daniel_lamotte/sandbox/krankshaft/krankshaft/models.py
# Compiled at: 2013-11-05 14:36:36
from django.db import models

class APITokenBase(models.Model):
    """
    Use a token in place of user password to allow easy expiry.

    Example:

        class APIToken(APITokenBase):
            # required attributes
            #   - id (uniquely identifying the credential used)
            #   - user (either a user field or property returning the user)

            user = models.ForeignKey('auth.User')
            token = models.TextField()

            @classmethod
            def get(cls, owner, token):
                return cls.objects                     .select_related('user')                     .get(
                        user__username=owner,
                        token=token
                    )

            def is_valid(self):
                return self.user.is_active

            def save(self, *args, **kwargs):
                if not self.token:
                    self.token = ...

        from krankshaft import API as APIBase
        from krankshaft.auth import Auth as AuthBase
        from krankshaft.authn import AuthnDjangoAPIToken

        class Auth(AuthBase):
            authn = AuthnDjangoAPIToken(APIToken)

        class API(APIBase):
            Auth = Auth
    """

    class Meta:
        abstract = True

    @classmethod
    def get(cls, owner, token):
        raise NotImplementedError

    def is_valid(self):
        """is_valid() -> bool

        Test if token is still valid.
        """
        return True