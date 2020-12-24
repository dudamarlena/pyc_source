# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/tests/base.py
# Compiled at: 2014-11-21 04:30:37
import os, seafileapi, unittest
from contextlib import contextmanager
from tests.utils import randstring
SERVER = os.environ.get('SEAFILE_TEST_SERVER_ADDRESS', 'http://127.0.0.1:8000')
USER = os.environ.get('SEAFILE_TEST_USERNAME', 'test@seafiletest.com')
PASSWORD = os.environ.get('SEAFILE_TEST_PASSWORD', 'testtest')
ADMIN_USER = os.environ.get('SEAFILE_TEST_ADMIN_USERNAME', 'admin@seafiletest.com')
ADMIN_PASSWORD = os.environ.get('SEAFILE_TEST_ADMIN_PASSWORD', 'adminadmin')

def _create_client():
    return seafileapi.connect(SERVER, USER, PASSWORD)


class SeafileApiTestCase(unittest.TestCase):
    """Base class for all python-seafile test cases"""
    client = _create_client()

    def assertHasLen(self, obj, expected_length):
        actuallen = len(obj)
        msg = 'Expected length is %s, but actual lenght is %s' % (expected_length, actuallen)
        self.assertEqual(actuallen, expected_length, msg)

    def assertEmpty(self, obj):
        self.assertHasLen(obj, 0)

    @contextmanager
    def create_tmp_repo(self):
        repos = self.client.repos
        repo_name = 'tmp-测试资料库-%s' % randstring()
        repo_desc = 'tmp, 一个测试资料库-%s' % randstring()
        repo = repos.create_repo(repo_name, repo_desc)
        try:
            yield repo
        finally:
            repo.delete()