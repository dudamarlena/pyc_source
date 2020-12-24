# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddgen/utils/test__logging.py
# Compiled at: 2020-03-31 14:41:06
# Size of source mod 2**32: 1087 bytes
import logging, os, unittest
from pkg_resources import resource_filename
from ._logging import setup_logging

@unittest.skip('These tests are not meant to be run now')
class TestLogging(unittest.TestCase):

    def setUp(self) -> None:
        self.log_file = resource_filename(__name__, 'test_data/test.log')

    def tearDown(self) -> None:
        if os.path.isfile(self.log_file):
            os.remove(self.log_file)

    def test_logging_to_file(self):
        self.assertFalse(os.path.isfile(self.log_file))
        setup_logging(filename=(self.log_file))
        logger = logging.getLogger(__name__)
        logger.info('bla bla bla')
        self.assertTrue(os.path.isfile(self.log_file))
        with open(self.log_file) as (fh):
            bla = fh.read()
        self.assertTrue('bla bla bla' in bla)

    def test_logging_without_file(self):
        self.assertFalse(os.path.isfile(self.log_file))
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info('bla bla bla')
        self.assertFalse(os.path.isfile(self.log_file))