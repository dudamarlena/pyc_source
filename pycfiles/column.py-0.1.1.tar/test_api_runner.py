# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tests/test_api_runner.py
# Compiled at: 2017-08-02 01:06:09
from testtools import TestCase
from column import APIRunner

class TestAPIRunner(TestCase):

    def setUp(self):
        super(TestAPIRunner, self).setUp()

    def test_run_module_on_localhost(self):
        api_runner = APIRunner()
        api_runner.run_module('localhost', remote_user=None)
        return

    def test_run_playbook_on_localhost(self):
        api_runner = APIRunner()
        pb_path = './tests/fixtures/playbooks/hello_world.yml'
        result = api_runner.run_playbook(pb_path, 'localhost,', remote_user=None, connection='local')
        self.assertEqual('', result['error_msg'])
        self.assertEqual(0, len(result['unreachable_hosts']))
        self.assertEqual(0, len(result['failed_hosts']))
        return

    def test_run_playbook_with_fail(self):
        api_runner = APIRunner()
        pb_path = './tests/fixtures/playbooks/hello_world_with_fail.yml'
        result = api_runner.run_playbook(pb_path, 'localhost,', remote_user=None, connection='local')
        self.assertIsNot('', result['error_msg'])
        self.assertEqual(0, len(result['unreachable_hosts']))
        self.assertEqual(1, len(result['failed_hosts']))
        self.assertEqual(1, len(result['failed_tasks']))
        self.assertEqual('This task will fail', result['failed_tasks'][0])
        return