# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pynosql/test/client_test.py
# Compiled at: 2019-03-09 18:37:41
import unittest
from pynosql.credentials.base_credentials import InvalidCredentials
from pynosql.credentials.aws import AWSCredentials
from pynosql.clients.aws import AWSClient

class TestSetup(unittest.TestCase):
    """ Credentials Test """

    def test_valid_aws_client(self):
        """ Test valid AWS Credentials """
        try:
            credentials = AWSCredentials('AKIAIOSFODNN7EXAMPLE', 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY')
            AWSClient(credentials, 'us-west-2')
        except InvalidCredentials:
            self.fail('Unexpected exception initializing AWSClient')

    def test_invalid_aws_client_credentials(self):
        """ Test invalid AWS client credentials """
        try:
            credentials = 'testing'
            AWSClient(credentials, 'us-west-2')
            self.fail('Expected InvalidCredentials exception did not ocurr.')
        except InvalidCredentials:
            pass