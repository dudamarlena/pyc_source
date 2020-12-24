# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/pythonids/components/pypythonids/tests/pythonids_tests/shared/libs/pythonids/PYVxyz/Case000/CallCase.py
# Compiled at: 2019-01-07 06:36:09
from __future__ import absolute_import
from __future__ import print_function
__author__ = 'Arno-Can Uestuensoez'
__license__ = 'Artistic-License-2.0 + Forced-Fairplay-Constraints'
__copyright__ = 'Copyright (C) 2010-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
__version__ = '0.1.10'
__uuid__ = '5624dc41-775a-4d17-ac42-14a0d5c41d1a'
__docformat__ = 'restructuredtext en'
import unittest, sys, pythonids

class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.maxDiff = None
        return

    def testCase010(self):
        pvx = pythonids.encode_pysyntax_to_16bit(*sys.version_info[:3])
        self.assertEqual(pythonids.PYVxyz, pvx)


if __name__ == '__main__':
    unittest.main()