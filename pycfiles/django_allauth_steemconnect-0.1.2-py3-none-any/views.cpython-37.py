# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ohing/workspace/steempumpkin/api/steemconnect_provider/providers/steemconnect/views.py
# Compiled at: 2018-12-25 02:22:23
# Size of source mod 2**32: 1093 bytes
import json, requests
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter, OAuth2CallbackView, OAuth2LoginView
from steemconnect_provider.providers.steemconnect.provider import SteemConnectProvider

class SteemConnectOAuth2Adapter(OAuth2Adapter):
    provider_id = SteemConnectProvider.id
    access_token_url = 'https://steemconnect.com/api/oauth2/token'
    authorize_url = 'https://steemconnect.com/oauth2/authorize'
    revoke_url = 'https://steemconnect.com/api/oauth2/token/revoke'
    profile_url = 'https://steemconnect.com/api/me'
    scope_delimiter = ','

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get((self.profile_url), headers={'Authorization': token.token})
        extra_data = json.loads(resp.content)
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(SteemConnectOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(SteemConnectOAuth2Adapter)