# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/exedre/Dropbox/exedre@gmail.com/Dropbox/Work/GeCo-dev/infomedia-1.0/build/lib/infomedia/test/options.py
# Compiled at: 2012-07-21 15:44:01
from datetime import datetime
import unittest, infomedia
from infomedia.options import *

class OptionsTest(unittest.TestCase):

    def test_options_01(self):
        """DEFAULT_DEFINES['THISMONTH']"""
        options = Options(test=1)
        self.assertEqual(1, options.test)