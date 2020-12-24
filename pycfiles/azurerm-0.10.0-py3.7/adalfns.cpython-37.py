# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\azurerm\adalfns.py
# Compiled at: 2018-11-08 13:09:11
# Size of source mod 2**32: 4505 bytes
"""adalfns - place to store azurerm functions which call adal routines"""
import json, codecs, os, requests
from datetime import datetime as dt
import adal
from .settings import get_auth_endpoint, get_resource_endpoint

def get_access_token(tenant_id, application_id, application_secret):
    """get an Azure access token using the adal library.

    Args:
        tenant_id (str): Tenant id of the user's account.
        application_id (str): Application id of a Service Principal account.
        application_secret (str): Application secret (password) of the Service Principal account.

    Returns:
        An Azure authentication token string.
    """
    context = adal.AuthenticationContext((get_auth_endpoint() + tenant_id),
      api_version=None)
    token_response = context.acquire_token_with_client_credentials(get_resource_endpoint(), application_id, application_secret)
    return token_response.get('accessToken')


def get_access_token_from_cli():
    """Get an Azure authentication token from CLI's cache.

    Will only work if CLI local cache has an unexpired auth token (i.e. you ran 'az login'
        recently), or if you are running in Azure Cloud Shell (aka cloud console)

    Returns:
        An Azure authentication token string.
    """
    if 'ACC_CLOUD' in os.environ:
        if 'MSI_ENDPOINT' in os.environ:
            endpoint = os.environ['MSI_ENDPOINT']
            headers = {'Metadata': 'true'}
            body = {'resource': 'https://management.azure.com/'}
            ret = requests.post(endpoint, headers=headers, data=body)
            return ret.json()['access_token']
    home = os.path.expanduser('~')
    sub_username = ''
    azure_profile_path = home + os.sep + '.azure' + os.sep + 'azureProfile.json'
    if os.path.isfile(azure_profile_path) is False:
        print('Error from get_access_token_from_cli(): Cannot find ' + azure_profile_path)
        return
    with codecs.open(azure_profile_path, 'r', 'utf-8-sig') as (azure_profile_fd):
        subs = json.load(azure_profile_fd)
    for sub in subs['subscriptions']:
        if sub['isDefault'] == True:
            sub_username = sub['user']['name']

    if sub_username == '':
        print('Error from get_access_token_from_cli(): Default subscription not found in ' + azure_profile_path)
        return
    access_keys_path = home + os.sep + '.azure' + os.sep + 'accessTokens.json'
    if os.path.isfile(access_keys_path) is False:
        print('Error from get_access_token_from_cli(): Cannot find ' + access_keys_path)
        return
    with open(access_keys_path, 'r') as (access_keys_fd):
        keys = json.load(access_keys_fd)
    for key in keys:
        if key['userId'] == sub_username:
            if 'accessToken' not in keys[0]:
                print('Error from get_access_token_from_cli(): accessToken not found in ' + access_keys_path)
                return
                if 'tokenType' not in keys[0]:
                    print('Error from get_access_token_from_cli(): tokenType not found in ' + access_keys_path)
                    return
                elif 'expiresOn' not in keys[0]:
                    print('Error from get_access_token_from_cli(): expiresOn not found in ' + access_keys_path)
                    return
                    expiry_date_str = key['expiresOn']
                    if 'T' in expiry_date_str:
                        exp_date = dt.strptime(key['expiresOn'], '%Y-%m-%dT%H:%M:%S.%fZ')
                else:
                    exp_date = dt.strptime(key['expiresOn'], '%Y-%m-%d %H:%M:%S.%f')
                if exp_date < dt.now():
                    continue
            else:
                return key['accessToken']

    print("Error from get_access_token_from_cli(): token expired. Run 'az login'")
    return