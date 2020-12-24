# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_loggingconf.py
# Compiled at: 2016-10-11 17:48:36
from __future__ import unicode_literals
from moya import loggingconf
from fs.osfs import OSFS
import os.path
from os.path import join

class TestLoggingConf(object):

    def setUp(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), b'loggingconf')
        print self.path

    def tearDown(self):
        pass

    def test_init(self):
        """Test reading logging conf"""
        loggingconf.init_logging(join(self.path, b'logging.ini'))
        loggingconf.init_logging(join(self.path, b'extend.ini'))

    def test_fs(self):
        """test reading logging from fs"""
        fs = OSFS(self.path)
        loggingconf.init_logging_fs(fs, b'logging.ini')
        loggingconf.init_logging_fs(fs, b'extend.ini')