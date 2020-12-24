# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/test/info_source_manager_test.py
# Compiled at: 2012-02-12 09:07:46
import unittest
from linseed import InfoSourceManager

class Test(unittest.TestCase):

    def setUp(self):
        self.mgr = InfoSourceManager()

    def test_api(self):
        self.mgr.keys()
        self.mgr.items()
        self.mgr.values()
        len(self.mgr)
        for k in self.mgr:
            self.mgr[k]