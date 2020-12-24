# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskills/utils/auth.py
# Compiled at: 2017-09-27 06:00:05
""" Downloader for Snips assistants. """
from http_helpers import post_request_json

class Auth:
    AUTH_URL = 'https://external-gateway.snips.ai/v1/user/auth'

    @staticmethod
    def retrieve_token(email, password):
        data = {'email': email, 'password': password}
        response, response_headers = post_request_json(Auth.AUTH_URL, data)
        token = response_headers.getheader('Authorization')
        return token