# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/git/lib/python2.5/site-packages/hive/tests/functional/test_repos.py
# Compiled at: 2011-07-08 03:48:39
try:
    import json
except ImportError:
    import simplejson as json

import urllib
from hive.tests import *
from hive.tests.functional import constants
_ = urllib.quote

class TestReposController(TestController):

    def test_index(self):
        response = self.app.get(url('repos'))
        self.assertEqual(response.status, '200 OK')

    def test_create(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo1') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo1'}), content_type='application/json')
            self.assertEqual(response.status, '201 Created')
            self.assertTrue(response.headers['location'].endswith(_('/repos/repo1')))
        response = self.app.get(url('repos'))
        self.assertTrue(_('/repos/repo1') in json.loads(response.body))

    def test_delete(self):
        response = self.app.get(url('repos'))
        if _('/repos/repo2') not in json.loads(response.body):
            response = self.app.post(url('repos'), params=json.dumps({'name': 'repo2'}), content_type='application/json')
        self.assertEqual(response.status, '201 Created')
        self.assertTrue(response.headers['location'].endswith(_('/repos/repo2')))
        response = self.app.delete(url('repo', id='repo2'))
        self.assertEqual(response.status, '200 OK')
        response = self.app.get(url('repos'))
        self.assertEqual(response.status, '200 OK')
        self.assertTrue(_('/repos/repo2') not in json.loads(response.body))