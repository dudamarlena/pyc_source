# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ohing/workspace/steempumpkin/api/steemconnect_provider/providers/steemconnect/provider.py
# Compiled at: 2018-12-25 02:16:39
# Size of source mod 2**32: 1157 bytes
from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

class SteemConnectAccount(ProviderAccount):

    def get_profile_url(self):
        return self.account.extra_data.get('html_url')

    def get_avatar_url(self):
        return self.account.extra_data.get('avatar_url')

    def to_str(self):
        dflt = super(SteemConnectAccount, self).to_str()
        return next((value for value in (
         self.account.extra_data.get('name', None),
         self.account.extra_data.get('login', None),
         dflt) if value is not None))


class SteemConnectProvider(OAuth2Provider):
    id = 'steemconnect'
    name = 'SteemConnect'
    account_class = SteemConnectAccount

    def get_default_scope(self):
        return [
         'vote', 'comment', 'comment_options', 'custom_json']

    def extract_uid(self, data):
        return str(data['account']['id'])


provider_classes = [
 SteemConnectProvider]
providers.registry.register(SteemConnectProvider)