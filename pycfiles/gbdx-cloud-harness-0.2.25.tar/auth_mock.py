# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/cloud-harness/gbdx_cloud_harness/test/auth_mock.py
# Compiled at: 2016-10-31 16:11:18
"""
Copied from gbdxtools.
This function returns a mock gbdx-auth requests session with a dummy token.  You can optionally pass in a real token
if you want to actually make requests.
"""
from future import standard_library
standard_library.install_aliases()
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

def get_mock_gbdx_session(token='dummytoken'):
    s = OAuth2Session(client=LegacyApplicationClient('asdf'), auto_refresh_url='fdsa', auto_refresh_kwargs={'client_id': 'asdf', 
       'client_secret': 'fdsa'})
    s.token = token
    s.access_token = token
    return s