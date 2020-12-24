# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/tests/common/secrets.py
# Compiled at: 2019-08-14 11:41:29
# Size of source mod 2**32: 2624 bytes
"""Test Configuration variables"""
__OAUTH_TOKEN_URL = 'https://in.xfel.eu/dev_calibration/oauth/token'
__OAUTH_AUTHORIZE_URL = 'https://in.xfel.eu/dev_calibration/oauth/authorize'
__CLIENT_ID = 'karabo_test_201ed15ff071a63e76cb0b91a1ab17b36d5f92d24b6df4497aa646e39c46a324'
__CLIENT_SECRET = 'karabo_test_a8ae80f5e96531f19bf2d2b6102f5a537196aca44a673ad36533310e07529757'
__USER_EMAIL = 'karabo_test@example.com'
CLIENT_OAUTH2_INFO = {'EMAIL':__USER_EMAIL, 
 'CLIENT_ID':__CLIENT_ID, 
 'CLIENT_SECRET':__CLIENT_SECRET, 
 'AUTH_URL':__OAUTH_AUTHORIZE_URL, 
 'TOKEN_URL':__OAUTH_TOKEN_URL, 
 'REFRESH_URL':__OAUTH_TOKEN_URL, 
 'SCOPE':'', 
 'first_name':'Karabo', 
 'last_name':'Tester', 
 'name':'Karabo Tester', 
 'nickname':'', 
 'provider':'local', 
 'uid':''}
BASE_API_URL = 'https://in.xfel.eu/dev_calibration/api/'