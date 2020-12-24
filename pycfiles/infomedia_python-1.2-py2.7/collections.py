# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/exedre/Dropbox/exedre@gmail.com/Dropbox/Work/GeCo-dev/infomedia-1.0/build/lib/infomedia/test/collections.py
# Compiled at: 2012-07-22 03:15:17
from datetime import datetime
import unittest, infomedia
from infomedia.collections import *

class CollectionTest(unittest.TestCase):

    def test_needed_01(self):
        """needed('A','B','C')"""
        self.assertRaises(ValueError, needed, {}, 'A', 'B', 'C')