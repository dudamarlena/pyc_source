# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alforbes/virtualenv/orloclien-py2/lib/python2.7/site-packages/tests/__init__.py
# Compiled at: 2017-04-04 11:21:48
from unittest import TestCase
import uuid
from orloclient import OrloClient
from orloclient import Release, Package
from orloclient.mock_orlo import MockOrloClient

class OrloClientTest(TestCase):
    """
    Parent method for Orlo client tests

    Constants in this class are test parameters for Orlo methods
    """
    NOTE = 'test note'
    PLATFORMS = ['test_platform']
    REFERENCES = ['test_reference']
    TEAM = 'test_team'
    URI = 'http://localhost:1337'
    USER = 'test_user'
    CLIENT = MockOrloClient('http://dummy.example.com')
    RELEASE = Release(CLIENT, str(uuid.uuid4()))
    PACKAGE = RELEASE.packages[0]

    def setUp(self):
        self.orlo = OrloClient(self.URI)