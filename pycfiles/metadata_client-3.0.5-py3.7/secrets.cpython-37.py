# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/common/secrets.py
# Compiled at: 2019-08-16 07:56:46
# Size of source mod 2**32: 2667 bytes
"""Test Configuration variables"""
__OAUTH_TOKEN_URL = 'https://in.xfel.eu/test_metadata/oauth/token'
__OAUTH_AUTHORIZE_URL = 'https://in.xfel.eu/test_metadata/oauth/authorize'
__CLIENT_ID = '201ed15ff071a63e76cb0b91a1ab17b36d5f92d24b6df4497aa646e39c46a324'
__CLIENT_SECRET = 'a8ae80f5e96531f19bf2d2b6102f5a537196aca44a673ad36533310e07529757'
__USER_EMAIL = 'luis.maia@xfel.eu'
CLIENT_OAUTH2_INFO = {'EMAIL':__USER_EMAIL, 
 'CLIENT_ID':__CLIENT_ID, 
 'CLIENT_SECRET':__CLIENT_SECRET, 
 'AUTH_URL':__OAUTH_AUTHORIZE_URL, 
 'TOKEN_URL':__OAUTH_TOKEN_URL, 
 'REFRESH_URL':__OAUTH_TOKEN_URL, 
 'SCOPE':''}
USER_INFO = {'EMAIL':__USER_EMAIL, 
 'FIRST_NAME':'Luis', 
 'LAST_NAME':'Maia', 
 'NAME':'Luis Maia', 
 'NICKNAME':'maial', 
 'PROVIDER':'ldap', 
 'UID':'maial'}
BASE_API_URL = 'https://in.xfel.eu/test_metadata/api/'