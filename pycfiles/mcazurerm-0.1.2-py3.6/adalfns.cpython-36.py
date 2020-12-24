# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\adalfns.py
# Compiled at: 2017-08-11 23:27:04
# Size of source mod 2**32: 662 bytes
import adal

def get_access_token(tenant_id, application_id, application_secret, authentication_endpoint='https://login.chinacloudapi.cn/', resource='https://management.core.chinacloudapi.cn/'):
    context = adal.AuthenticationContext(authentication_endpoint + tenant_id)
    token_response = context.acquire_token_with_client_credentials(resource, application_id, application_secret)
    return token_response.get('accessToken')