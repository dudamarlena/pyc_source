# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/exedre/Dropbox/exedre@gmail.com/Dropbox/Work/GeCo-dev/infomedia-1.0/build/lib/infomedia/hash2cfg/test/defines.py
# Compiled at: 2012-07-21 14:40:18
from datetime import datetime
import unittest, infomedia
from infomedia.hash2cfg.defines import *

class DefinesTest(unittest.TestCase):

    def setUp(self):
        self._date = datetime.now()

    def test_defines(self):
        """DEFAULT_DEFINES['THISMONTH']"""
        self.assertEqual(str(self._date.month), DEFAULT_DEFINES['THISMONTH'])