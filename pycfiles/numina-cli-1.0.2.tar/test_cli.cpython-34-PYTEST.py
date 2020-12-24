# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rafael/Programs/Numina/numina-cli/tests/test_cli.py
# Compiled at: 2017-06-16 16:44:53
# Size of source mod 2**32: 4034 bytes
"""Tests for our main numina CLI module."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from subprocess import PIPE, Popen as popen
from unittest import TestCase
from subprocess import check_output
import os, json
from numina import __version__ as VERSION
from numina.commands import utils
test_token = os.environ['TEST_TOKEN']

class TestHelp(TestCase):

    def test_returns_usage_information(self):
        output = popen(['numina', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)
        self.assertTrue('Options:' in output)
        self.assertTrue('Examples:' in output)
        output = popen(['numina', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)
        self.assertTrue('Options:' in output)
        self.assertTrue('Examples:' in output)


class TestVersion(TestCase):

    def test_returns_version_information(self):
        output = popen(['numina', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), VERSION)


class TestAuthenticate(TestCase):

    def test_authentication_no_token(self):
        try:
            output = check_output(['numina', 'authenticate'])
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_authentication_token(self):
        output = popen(['numina', 'authenticate', test_token], stdout=PIPE).communicate()[0]
        self.assertTrue(output.strip() == 'Authentication token has been saved for future use: "' + test_token + '"')
        token_in_file = utils.get_saved_token()
        self.assertTrue(test_token == token_in_file)


class TestUtils(TestCase):

    def test_get_saved_token(self):
        token_in_file = utils.get_saved_token()
        self.assertTrue(test_token == token_in_file)
        os.chdir('..')
        token_in_file = utils.get_saved_token()
        self.assertTrue(test_token == token_in_file)
        os.chdir('./numina-cli')
        token_in_file = utils.get_saved_token()
        self.assertTrue(test_token == token_in_file)

    def test_if_token_expired(self):
        mock_response = {'status': 'Token is expired'}
        is_expired = utils.check_if_expired(mock_response)
        self.assertTrue(is_expired)
        mock_response = {}
        is_expired = utils.check_if_expired(mock_response)
        self.assertTrue(is_expired)


class TestCounts(TestCase):

    def test_success_case(self):
        output = check_output(['numina', 'counts', '5840a3f6ffe95e4003030e34'])
        j_output = json.loads(output)
        self.assertTrue('result' in j_output)
        self.assertTrue('status' in j_output)
        self.assertTrue('code' in j_output)

    def test_fail_case(self):
        token_in_file = utils.get_saved_token()
        try:
            check_output(['numina', 'counts'])
            self.assertTrue(False)
        except:
            self.assertTrue(True)


class TestDevices(TestCase):

    def test_success_case(self):
        output = check_output(['numina', 'devices'])
        j_output = json.loads(output)
        self.assertTrue('result' in j_output)


class TestMovements(TestCase):

    def test_success_case(self):
        output = check_output(['numina', 'movements', '5840a3f6ffe95e4003030e34'])
        j_output = json.loads(output)
        self.assertTrue('result' in j_output)