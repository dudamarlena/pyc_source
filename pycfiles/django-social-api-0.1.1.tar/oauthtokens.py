# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-social-api/social_api/storages/oauthtokens.py
# Compiled at: 2016-02-11 14:39:48
import time
from oauth_tokens.models import AccessToken, UserCredentials, AccessTokenGettingError, AccessTokenRefreshingError
from ..lock import distributedlock, LockNotAcquiredError
from ..utils import limit_errored_calls
from .base import TokensStorageAbstractBase

class OAuthTokensStorage(TokensStorageAbstractBase):
    name = 'oauth_tokens'

    def __init__(self, *args, **kwargs):
        super(OAuthTokensStorage, self).__init__(*args, **kwargs)
        self.tag = self.get_from_context('tag')
        self.only_this = bool(self.tag)

    def get_tokens(self):
        queryset = AccessToken.objects.filter(provider=self.provider).order_by('-granted_at')
        if self.tag:
            queryset = queryset.filter(user_credentials__in=UserCredentials.objects.filter(tags__name=self.tag))
        return queryset.values_list('access_token', flat=True)

    @limit_errored_calls(AccessTokenGettingError, 5)
    def update_tokens(self):
        lock_name = 'update_tokens_for_%s' % self.provider
        try:
            with distributedlock(lock_name, blocking=False):
                AccessToken.objects.fetch(provider=self.provider)
                return True
        except LockNotAcquiredError:
            updated = False
            while not updated:
                try:
                    with distributedlock(lock_name, blocking=False):
                        updated = True
                except LockNotAcquiredError:
                    time.sleep(1)

            return True

    @limit_errored_calls(AccessTokenRefreshingError, 5)
    def refresh_tokens(self):
        return AccessToken.objects.refresh(self.provider)