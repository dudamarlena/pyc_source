# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alforbes/virtualenv/orloclien-py2/lib/python2.7/site-packages/tests/test_command_line.py
# Compiled at: 2017-04-28 09:55:28
import unittest, uuid, orloclient
from test_mock import MockOrloClient
from mock import patch
import logging
logging.basicConfig(level=logging.DEBUG)

@patch('orloclient.__main__.OrloClient', MockOrloClient)
class TestCommandLine(unittest.TestCase):

    def setUp(self):
        self.client = MockOrloClient('http://localhost')

        class Args:
            release = self.client.example_release.id
            package = self.client.example_package.id
            user = 'bob'
            platforms = ['gumtree']
            team = 'adtech'
            references = ['GTEPICS-FOO']
            name = 'my_name'
            version = '1.0.0'
            note = 'blah blah'

        self.args = Args

    def test_action_get_release(self):
        orloclient.__main__.action_get_release(self.client, self.args)

    def test_action_get_package(self):
        orloclient.__main__.action_get_package(self.client, self.args)

    def test_action_create_release(self):
        orloclient.__main__.action_create_release(self.client, self.args)

    def test_action_create_package(self):
        orloclient.__main__.action_create_package(self.client, self.args)

    def test_action_start(self):
        orloclient.__main__.action_start(self.client, self.args)

    def test_action_stop(self):
        orloclient.__main__.action_stop(self.client, self.args)