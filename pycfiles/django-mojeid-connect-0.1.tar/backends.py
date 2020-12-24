# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: django_mojeid_connect/backends.py
# Compiled at: 2018-07-09 07:54:11
"""Backend for django_mojeid_connect with pairing capability."""
from __future__ import unicode_literals
from django_oidc_sub.backends import OidcSubBackend
from django_oidc_sub.models import OidcUserSub

class MojeidOidcBackend(OidcSubBackend):
    """Backend that pairs mojeid users to currently logged user."""

    def filter_users_by_claims(self, claims):
        """Retrieve and pair user."""
        query = super(MojeidOidcBackend, self).filter_users_by_claims(claims)
        self.request.session[b'oidc_claims'] = claims
        if query.exists():
            return query
        if self.request.user.is_authenticated:
            OidcUserSub.objects.create(sub=claims[b'sub'], user=self.request.user)
            return super(MojeidOidcBackend, self).filter_users_by_claims(claims)
        return query