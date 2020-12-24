# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/yapyutils/components/yapyutils/tests/yapyutils_tests/libs/modules/loader/functions/load_module/Case000/CallCase.py
# Compiled at: 2019-06-17 11:56:51
from __future__ import absolute_import
from __future__ import print_function
__author__ = 'Arno-Can Uestuensoez'
__license__ = 'Artistic-License-2.0 + Forced-Fairplay-Constraints'
__copyright__ = 'Copyright (C) 2010-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
__version__ = '0.1.10'
__uuid__ = '60cac28d-efe6-4a8d-802f-fa4fc94fa741'
__docformat__ = 'restructuredtext en'
import unittest, os, sys
from testdata.yapyutils_testdata import mypath
from yapyutils.modules.loader import get_modulelocation, load_module

class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        sys.path.insert(0, mypath)
        self.maxDiff = None
        return

    def testCase010(self):
        impname, imppathname = get_modulelocation('module1', mypath, ('testpackage', ))
        self.assertEqual(impname, 'testpackage.module1')
        self.assertTrue(imppathname.endswith('testpackage/module1.py'))
        mod = load_module(impname, imppathname)
        res = mod.testcall()
        resx = 'testpackage.module1'
        self.assertEqual(res, resx)


if __name__ == '__main__':
    unittest.main()