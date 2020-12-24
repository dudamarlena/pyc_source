# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/git/lib/python2.5/site-packages/hive/tests/functional/test_users.py
# Compiled at: 2011-07-26 04:50:42
try:
    import json
except ImportError:
    import simplejson as json

import urllib
from hive.tests import *
from hive.tests.functional import constants
_ = urllib.quote

class TestUsersController(TestController):

    def test_index(self):
        response = self.app.get(url('users'))
        self.assertEqual(response.status, '200 OK')

    def test_create(self):
        response = self.app.post(url('users'), params=json.dumps({'name': 'user1@test.com', 'pubkey': constants.USER1_PUBLIC_KEY}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/users/user1@test.com')))

    def test_update(self):
        response = self.app.post(url('users'), params=json.dumps({'name': 'user2@test.com', 'pubkey': constants.USER2_PUBLIC_KEY}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/users/user2@test.com')))
        response = self.app.put(url('user', id='user2@test.com'), json.dumps(constants.TMP_PUBLIC_KEY), content_type='application/json')
        self.assertEqual(response.status, '200 OK')

    def test_delete(self):
        response = self.app.post(url('users'), params=json.dumps({'name': 'user3@test.com', 'pubkey': constants.USER3_PUBLIC_KEY}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/users/user3@test.com')))
        response = self.app.delete(url('user', id='user3@test.com'))
        self.assertEqual(response.status, '200 OK')
        response = self.app.get(url('users'))
        self.assertEqual(response.status, '200 OK')
        self.assertTrue(_('/users/user3@test.com') not in json.loads(response.body))

    def test_show(self):
        response = self.app.get(url('users'))
        if _('/users/user1@test.com') not in json.loads(response.body):
            response = self.app.post(url('users'), params=json.dumps({'name': 'user1@test.com', 'pubkey': constants.USER1_PUBLIC_KEY}), content_type='application/json')
        response = self.app.get(url('user', id='user1@test.com'))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(json.loads(response.body), {'name': 'user1@test.com', 'pubkey': constants.USER1_PUBLIC_KEY})