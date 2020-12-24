# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/git/lib/python2.5/site-packages/hive/tests/functional/test_rules.py
# Compiled at: 2011-07-26 04:50:42
try:
    import json
except ImportError:
    import simplejson as json

import urllib
from hive.tests import *
from hive.tests.functional import constants
_ = urllib.quote

class TestRulesController(TestController):

    def test_index(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo1') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo1'}), content_type='application/json')
        response = self.app.get(url('rules', repo_id='repo1'))
        self.assertEqual(response.status, '200 OK')

    def test_create(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo1') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo1'}), content_type='application/json')
        response = self.app.post(url('rules', repo_id='repo1'), params=json.dumps({'permission': 'RW', 'refex_list': [
                        'refex1', 'refex2'], 
           'member_list': [
                         'user1@test.com']}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/rules/refex1,refex2;user1@test.com')))

    def test_update(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo1') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo1'}), content_type='application/json')
        response = self.app.post(url('rules', repo_id='repo1'), params=json.dumps({'permission': 'RW', 'refex_list': [
                        'refex3'], 
           'member_list': [
                         'user2@test.com']}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/rules/refex3;user2@test.com')))
        response = self.app.put(url('rule', id='refex3;user2@test.com', repo_id='repo1'), params=json.dumps({'permission': 'RW+', 'refex_list': [
                        'refex3'], 
           'member_list': [
                         'user1@test.com', 'user2@test.com']}), content_type='application/json')
        self.assertEqual(response.status, '200 OK')

    def test_delete(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo1') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo1'}), content_type='application/json')
        response = self.app.post(url('rules', repo_id='repo1'), params=json.dumps({'permission': 'RW', 'refex_list': [
                        'refex4'], 
           'member_list': [
                         'user2@test.com']}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/rules/refex4;user2@test.com')))
        response = self.app.delete(url('rule', id='refex4;user2@test.com', repo_id='repo1'))
        self.assertEqual(response.status, '200 OK')
        response = self.app.get(url('rules', repo_id='repo1'))
        self.assertEqual(response.status, '200 OK')
        self.assertTrue(_('/rules/refex4;user2@test.com') not in json.loads(response.body))

    def test_show(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo1') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo1'}), content_type='application/json')
        response = self.app.post(url('rules', repo_id='repo1'), params=json.dumps({'permission': '-', 'refex_list': [
                        'refex5'], 
           'member_list': [
                         'user3@test.com']}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/rules/refex5;user3@test.com')))
        response = self.app.get(url('rule', id='refex5;user3@test.com', repo_id='repo1'))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(json.loads(response.body), {'permission': '-', 'refex_list': [
                        'refex5'], 
           'member_list': [
                         'user3@test.com']})