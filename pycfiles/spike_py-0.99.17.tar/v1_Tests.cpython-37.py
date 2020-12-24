# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/v2/v1_Tests.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 1018 bytes
"""
Tests for v1 compatibility

Created by Marc-André on 2012-10-09.
Copyright (c) 2012 IGBMC. All rights reserved.
"""
from __future__ import print_function
import unittest
from v1.Kore import *

class v1Tests(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print(self.shortDescription())

    def test_BrukerImport(self):
        """tests Bruker 2D Import"""
        from ..v1 import Bruker
        from ..Tests import filename
        name2D = filename('Lasalocid-Tocsy/dataset/ser')
        self.announce()
        rep = Bruker.Import_2D(name2D)
        self.assertTrue(rep == (328, 2048))
        d = get_Kore_2D()
        self.assertAlmostEqual(d.axis1.specwidth, 5201.560468, 6)
        self.assertAlmostEqual(d[(100, 100)], 80)
        self.assertAlmostEqual(d[(4, 400)], -3186.0)


if __name__ == '__main__':
    unittest.main()