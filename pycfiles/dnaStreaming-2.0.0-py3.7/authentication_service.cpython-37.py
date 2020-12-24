# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dnaStreaming/services/authentication_service.py
# Compiled at: 2019-01-22 17:49:24
# Size of source mod 2**32: 262 bytes
from __future__ import absolute_import, division, print_function
from google.oauth2 import service_account

def get_authenticated_oauth_credentials(streaming_credentials):
    return service_account.Credentials.from_service_account_info(streaming_credentials)