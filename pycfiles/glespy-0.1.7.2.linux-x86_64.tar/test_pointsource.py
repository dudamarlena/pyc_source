# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/test/test_pointsource.py
# Compiled at: 2013-09-13 04:50:09
__author__ = 'yarnaid'
try:
    import glespy.pointsource as pointsource, glespy.test_data.data as data
except:
    import pointsource, test_data.data as data

import unittest

class PointSourceTest(unittest.TestCase, data.WithTestData):

    def setUp(self):
        super(PointSourceTest, self).setUp()
        self.init_data()

    def test_to_pixelmap_with_nx(self):
        psource = pointsource.PointSource(name=self.points_name)
        p_map = psource.to_pixelmap(nx=101)
        self.check_exist(p_map.name)