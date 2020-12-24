# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_errors.py
# Compiled at: 2018-10-16 12:42:27
import sys, unittest
from auklet.errors import AukletException, AukletConnectionError, AukletConfigurationError

class TestAukletException(unittest.TestCase):

    def test_auklet_exception(self):
        if sys.version_info < (3, ):
            self.assertEqual(str(AukletException(Exception)), "<type 'exceptions.Exception'>")
        else:
            self.assertEqual(str(AukletException(Exception)), "<class 'Exception'>")


class TestAukletConnectionError(unittest.TestCase):

    def test_auklet_connection_error(self):
        self.assertEqual(str(AukletConnectionError()), '')


class TestAukletConfigurationError(unittest.TestCase):

    def test_auklet_configuration_error(self):
        self.assertEqual(str(AukletConfigurationError()), '')


if __name__ == '__main__':
    unittest.main()