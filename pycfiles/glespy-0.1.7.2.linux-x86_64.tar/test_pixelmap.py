# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/test/test_pixelmap.py
# Compiled at: 2013-09-14 06:41:14
__author__ = 'yarnaid'
import unittest
try:
    import pixelmap, test_data.data as data, pointsource
except:
    import glespy.pixelmap as pixelmap, glespy.test_data.data as data, glespy.pointsource as pointsource

class PixelMapTests(unittest.TestCase, data.WithTestData):

    def setUp(self):
        super(PixelMapTests, self).setUp()
        self.init_data()

    def check_params_with_lmax(self, pm, lmax):
        self.assertEqual(pm.lmax, 100)
        self.assertGreaterEqual(pm.lmax, pm.lmin)
        self.assertGreaterEqual(pm.nx, pm.lmax * 2 + 1)
        self.assertGreaterEqual(pm.np, pm.nx * 2)

    def test_creation(self):
        pm = pixelmap.gPixelMap(lmax=100)
        self.check_params_with_lmax(pm, 100)

    @unittest.expectedFailure
    def test_from_alm(self):
        self.check_exist('alm')

    def test_sum_with_ps(self):
        pm = pixelmap.gPixelMap(name=self.map_name, **self.attrs)
        ps = pointsource.PointSource(name=self.points_name).to_pixelmap(**self.attrs)
        pm.add_map(ps)
        self.check_exist(pm.name)