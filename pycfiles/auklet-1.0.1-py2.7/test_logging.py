# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_logging.py
# Compiled at: 2018-10-16 12:42:27
import unittest
from auklet.monitoring.logging import AukletLogging

class TestAukletLogging(unittest.TestCase):

    def setUp(self):
        self.auklet_logging = AukletLogging()

    def base_test_log(self, function):
        self.assertRaises(NotImplementedError, lambda : function(msg='', data_type=str))

    def test_log(self):
        self.base_test_log(self.auklet_logging.log)

    def test_debug(self):
        self.base_test_log(self.auklet_logging.debug)

    def test_info(self):
        self.base_test_log(self.auklet_logging.info)

    def test_warning(self):
        self.base_test_log(self.auklet_logging.warning)

    def test_error(self):
        self.base_test_log(self.auklet_logging.error)

    def test_critical(self):
        self.base_test_log(self.auklet_logging.critical)


if __name__ == '__main__':
    unittest.main()