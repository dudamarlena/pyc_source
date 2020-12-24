# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/yapydata/components/yapydata/tests/yapydata_tests/libs/datatree/single/DataTreeYAML/readfile/basic/core/true/Case016/CallCase.py
# Compiled at: 2019-11-27 17:39:03
from __future__ import absolute_import
from __future__ import print_function
__author__ = 'Arno-Can Uestuensoez'
__license__ = 'Artistic-License-2.0 + Forced-Fairplay-Constraints'
__copyright__ = 'Copyright (C) 2010-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
__version__ = '0.1.10'
__uuid__ = '60cac28d-efe6-4a8d-802f-fa4fc94fa741'
__docformat__ = 'restructuredtext en'
import unittest, os, sys
from yapydata.datatree.synyaml import DataTreeYAML, YapyDataYAMLError

class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.maxDiff = None
        return

    def testCase010(self):
        _cap = DataTreeYAML(None)
        _cap.readfile(os.path.dirname(__file__) + os.sep + 'data')
        self.assertEqual(_cap.data, True)
        return


if __name__ == '__main__':
    unittest.main()