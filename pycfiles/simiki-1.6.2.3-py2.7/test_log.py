# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/tests/test_log.py
# Compiled at: 2017-06-02 11:17:28
from __future__ import print_function, with_statement, unicode_literals
import unittest, logging
try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

import nose
from simiki.utils import color_msg
from simiki.log import logging_init
from simiki.compat import is_py2, unicode

class TestLogInit(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.NOTSET)
        self.stream = StringIO()
        self.logger = logging.getLogger()
        self.handler = logging.StreamHandler(self.stream)
        for handler in self.logger.handlers:
            if not isinstance(handler, nose.plugins.logcapture.MyMemoryHandler):
                self.logger.removeHandler(handler)

        logging_init(level=logging.DEBUG, handler=self.handler)

    def test_logging_init(self):
        l2c = {b'debug': b'blue', 
           b'info': b'green', 
           b'warning': b'yellow', 
           b'error': b'red', 
           b'critical': b'bgred'}
        for level in l2c:
            self.stream.truncate(0)
            self.stream.seek(0)
            func = getattr(self.logger, level)
            func(level)
            expected_output = (b'[{0}]: {1}').format(color_msg(l2c[level], level.upper()), level)
            stream_output = self.stream.getvalue().strip()
            if is_py2:
                stream_output = unicode(stream_output)
            self.assertEqual(stream_output, expected_output)

    def tearDown(self):
        logging.disable(logging.CRITICAL)
        for handler in self.logger.handlers:
            if not isinstance(handler, nose.plugins.logcapture.MyMemoryHandler):
                self.logger.removeHandler(handler)


if __name__ == b'__main__':
    unittest.main()