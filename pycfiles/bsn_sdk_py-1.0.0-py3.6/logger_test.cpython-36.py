# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\until\logger_test.py
# Compiled at: 2020-04-23 02:49:06
# Size of source mod 2**32: 414 bytes
import unittest, logging
from bsn_sdk_py.until.bsn_logger import log_info

class TestLogger(unittest.TestCase):

    def setUp(self):
        FORMAT = '%(asctime)s %(thread)d %(message)s'
        logging.basicConfig(level=(logging.INFO), format=FORMAT, datefmt='[%Y-%m-%d %H:%M:%S]')

    def test_log_info(self):
        log_info('1111111111')


if __name__ == '__main__':
    unittest.main()