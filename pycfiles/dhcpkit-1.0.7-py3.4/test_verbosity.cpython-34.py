# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/common/logging/test_verbosity.py
# Compiled at: 2017-06-24 11:43:40
# Size of source mod 2**32: 5362 bytes
"""
Test whether the common logging verbosity functions work as intended
"""
import logging, unittest
from dhcpkit.common.logging.verbosity import set_verbosity_logger
from dhcpkit.common.server.logging import DEBUG_HANDLING, DEBUG_PACKETS

class VerbosityLoggerTestCase(unittest.TestCase):

    def test_logger_level(self):
        logger = logging.Logger('test_logger_level', logging.ERROR)
        self.assertEqual(logger.level, logging.ERROR)
        set_verbosity_logger(logger=logger, verbosity=0)
        self.assertEqual(logger.level, logging.NOTSET)

    def test_existing_handler(self):
        tests = [
         (
          logging.CRITICAL, 0, logging.CRITICAL),
         (
          logging.CRITICAL, 1, logging.WARNING),
         (
          logging.CRITICAL, 2, logging.INFO),
         (
          logging.CRITICAL, 3, logging.DEBUG),
         (
          logging.CRITICAL, 4, DEBUG_HANDLING),
         (
          logging.CRITICAL, 5, DEBUG_PACKETS),
         (
          logging.ERROR, 0, logging.ERROR),
         (
          logging.ERROR, 1, logging.WARNING),
         (
          logging.ERROR, 2, logging.INFO),
         (
          logging.ERROR, 3, logging.DEBUG),
         (
          logging.ERROR, 4, DEBUG_HANDLING),
         (
          logging.ERROR, 5, DEBUG_PACKETS),
         (
          logging.WARNING, 0, logging.WARNING),
         (
          logging.WARNING, 1, logging.WARNING),
         (
          logging.WARNING, 2, logging.INFO),
         (
          logging.WARNING, 3, logging.DEBUG),
         (
          logging.WARNING, 4, DEBUG_HANDLING),
         (
          logging.WARNING, 5, DEBUG_PACKETS),
         (
          logging.INFO, 0, logging.INFO),
         (
          logging.INFO, 1, logging.INFO),
         (
          logging.INFO, 2, logging.INFO),
         (
          logging.INFO, 3, logging.DEBUG),
         (
          logging.INFO, 4, DEBUG_HANDLING),
         (
          logging.INFO, 5, DEBUG_PACKETS),
         (
          logging.DEBUG, 0, logging.DEBUG),
         (
          logging.DEBUG, 1, logging.DEBUG),
         (
          logging.DEBUG, 2, logging.DEBUG),
         (
          logging.DEBUG, 3, logging.DEBUG),
         (
          logging.DEBUG, 4, DEBUG_HANDLING),
         (
          logging.DEBUG, 5, DEBUG_PACKETS),
         (
          DEBUG_HANDLING, 0, DEBUG_HANDLING),
         (
          DEBUG_HANDLING, 1, DEBUG_HANDLING),
         (
          DEBUG_HANDLING, 2, DEBUG_HANDLING),
         (
          DEBUG_HANDLING, 3, DEBUG_HANDLING),
         (
          DEBUG_HANDLING, 4, DEBUG_HANDLING),
         (
          DEBUG_HANDLING, 5, DEBUG_PACKETS),
         (
          DEBUG_PACKETS, 0, DEBUG_PACKETS),
         (
          DEBUG_PACKETS, 1, DEBUG_PACKETS),
         (
          DEBUG_PACKETS, 2, DEBUG_PACKETS),
         (
          DEBUG_PACKETS, 3, DEBUG_PACKETS),
         (
          DEBUG_PACKETS, 4, DEBUG_PACKETS),
         (
          DEBUG_PACKETS, 5, DEBUG_PACKETS),
         (
          logging.NOTSET, 0, logging.NOTSET),
         (
          logging.NOTSET, 1, logging.NOTSET),
         (
          logging.NOTSET, 2, logging.NOTSET),
         (
          logging.NOTSET, 3, logging.NOTSET),
         (
          logging.NOTSET, 4, logging.NOTSET),
         (
          logging.NOTSET, 5, logging.NOTSET)]
        for original_level, verbosity, expected_level in tests:
            name = '{} & {} = {}'.format(original_level, verbosity, expected_level)
            with self.subTest(test=name):
                logger = logging.Logger(name=name, level=logging.ERROR)
                handler = logging.Handler(level=original_level)
                logger.addHandler(handler)
                self.assertEqual(logger.level, logging.ERROR)
                self.assertEqual(handler.level, original_level)
                set_verbosity_logger(logger=logger, verbosity=verbosity, existing_console=handler)
                self.assertEqual(logger.level, logging.NOTSET)
                self.assertEqual(handler.level, expected_level)

    def test_create_handler(self):
        tests = [
         (
          logging.ERROR, 0, logging.ERROR),
         (
          logging.ERROR, 1, logging.WARNING),
         (
          logging.ERROR, 2, logging.INFO),
         (
          logging.ERROR, 3, logging.DEBUG),
         (
          logging.ERROR, 4, DEBUG_HANDLING),
         (
          logging.ERROR, 5, DEBUG_PACKETS)]
        for original_level, verbosity, expected_level in tests:
            name = '{} & {} = {}'.format(original_level, verbosity, expected_level)
            with self.subTest(test=name):
                logger = logging.Logger(name=name, level=logging.ERROR)
                self.assertEqual(logger.level, logging.ERROR)
                set_verbosity_logger(logger=logger, verbosity=verbosity)
                self.assertEqual(logger.level, logging.NOTSET)
                handler = logger.handlers[0]
                self.assertEqual(handler.level, expected_level)


if __name__ == '__main__':
    unittest.main()