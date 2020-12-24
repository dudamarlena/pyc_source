# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-facebook-api/facebook_api/tests.py
# Compiled at: 2016-04-02 12:22:50
"""
Copyright 2011-2015 ramusus
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from social_api.testcase import SocialApiTestCase
from .api import api_call, FacebookApi
TOKEN = 'CAAGPdaGocPIBANyHk4GO3HJYhNalf78scXf5CprODAIYELOjW7DBkYG6uV5hip71fEv19jZBrQdN1nUhsrcvghxKtuxEIMgPqr4XUQMnvx8SApZBU3C6ccyknaNunFqgMbZB0VQFaYukP6NEGDfvcZBbRk6DdxnCZCO7z20KkBd3ZB5Rusgskxx0S2ARZCfN8KZAzgAq3F3KSgZDZD'

class FacebookApiTestCase(SocialApiTestCase):
    provider = 'facebook'
    token = TOKEN


class FacebookApiTest(FacebookApiTestCase):

    def test_api_instance_singleton(self):
        self.assertEqual(id(FacebookApi()), id(FacebookApi()))

    def test_request(self):
        response = api_call('me')
        self.assertEqual(response['id'], '100005428301237')
        self.assertEqual(response['last_name'], 'Djangov')
        self.assertEqual(response['first_name'], 'Travis')
        self.assertEqual(response['gender'], 'male')