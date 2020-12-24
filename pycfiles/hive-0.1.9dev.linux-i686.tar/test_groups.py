# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/git/lib/python2.5/site-packages/hive/tests/functional/test_groups.py
# Compiled at: 2011-07-26 04:55:25
try:
    import json
except ImportError:
    import simplejson as json

import urllib
from hive.tests import *
from hive.tests.functional import constants
_ = urllib.quote

class TestGroupsController(TestController):

    def test_index(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo1') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo1'}), content_type='application/json')
        response = self.app.get(url('groups', repo_id='repo1'))
        self.assertEqual(response.status, '200 OK')

    def test_create(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo1') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo1'}), content_type='application/json')
        response = self.app.post(url('groups', repo_id='repo1'), params=json.dumps({'name': '@group1', 'member_list': [
                         'user1@test.com']}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/groups/@group1')))

    def test_update(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo1') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo1'}), content_type='application/json')
        response = self.app.post(url('groups', repo_id='repo1'), params=json.dumps({'name': '@group2', 'member_list': [
                         'user2@test.com']}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/groups/@group2')))
        response = self.app.put(url('group', id='@group2', repo_id='repo1'), params=json.dumps(['user2@test.com', 'user3@test.com']), content_type='application/json')
        self.assertEqual(response.status, '200 OK')

    def test_delete(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo1') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo1'}), content_type='application/json')
        response = self.app.post(url('groups', repo_id='repo1'), params=json.dumps({'name': '@group3', 'member_list': [
                         'user2@test.com']}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/groups/@group3')))
        response = self.app.delete(url('group', id='@group3', repo_id='repo1'))
        self.assertEqual(response.status, '200 OK')
        response = self.app.get(url('groups', repo_id='repo1'))
        self.assertEqual(response.status, '200 OK')
        self.assertTrue(_('/groups/@group3') not in json.loads(response.body))

    def test_show(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo1') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo1'}), content_type='application/json')
        response = self.app.post(url('groups', repo_id='repo1'), params=json.dumps({'name': '@group4', 'member_list': [
                         'user2@test.com']}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/groups/@group4')))
        response = self.app.get(url('group', id='@group4', repo_id='repo1'))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(json.loads(response.body), ['user2@test.com'])