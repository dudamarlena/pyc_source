# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/tests/framework.py
# Compiled at: 2013-12-18 08:08:21
import os, sys
from six import print_
from six.moves import input, reduce
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(TEST_DIR)
sys.path.insert(0, ROOT_DIR)
from unittest import main, TestCase
from douban_client import DoubanClient
from douban_client.api.error import DoubanAPIError
try:
    from local_config import KEY, SECRET, CALLBACK, SCOPE, TOKEN
except ImportError:
    KEY = ''
    SECRET = ''
    CALLBACK = ''
    SCOPE_MAP = {'basic': ['douban_basic_common', 'community_basic_user']}
    SCOPE = (',').join(reduce(lambda x, y: x + y, SCOPE_MAP.values()))
    TOKEN = ''

def get_client():
    client = DoubanClient(KEY, SECRET, CALLBACK, SCOPE)
    token = TOKEN
    if token:
        client.auth_with_token(token)
    else:
        print_('Go to the following link in your browser:')
        print_(client.authorize_url)
        code = input("Enter the verification code and hit ENTER when you're done:")
        client.auth_with_code(code)
        print_('token code:', client.token_code)
        print_('refresh token code:', client.refresh_token_code)
    return client


client = get_client()

class DoubanClientTestBase(TestCase):

    def setUp(self):
        pass

    @property
    def client(self):
        return client