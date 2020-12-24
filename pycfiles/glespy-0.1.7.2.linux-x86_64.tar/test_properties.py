# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/test/test_properties.py
# Compiled at: 2013-09-14 06:41:10
__author__ = 'yarnaid'
import unittest
try:
    import properties
except:
    import glespy.properties as properties

class MultipoledTests(unittest.TestCase):
    m = properties.Multipoled()

    def test_set_lmax_g_lmin(self):
        """
        if lmax > lmin
        """
        self.m.lmax = 2
        self.m.lmin = self.m.lmax - 1
        self.assertGreater(self.m.lmax, self.m.lmin)
        print 'test!'

    def test_set_lmax_e_lmin(self):
        """
        lmax == lmin
        """
        self.m.lmax = 2
        self.m.lmin = self.m.lmax
        self.assertEqual(self.m.lmax, self.m.lmin)

    def test_set_lmin_g_lmax(self):
        """
        lmin > lmax
        """
        self.m.lmin = 10
        self.m.lmax = 1
        self.assertGreaterEqual(self.m.lmax, self.m.lmin)

    def test_set_lmax_g_lmin(self):
        """
        lmax < lmin
        """
        self.m.lmax = 1
        self.m.lmin = 10
        self.assertGreaterEqual(self.m.lmax, self.m.lmin)


class RenderedTests(unittest.TestCase):
    data = properties.Rendered()

    def check_lmax_nx(self):
        self.assertGreaterEqual(self.data.nx, self.data.lmax * 2 + 1)

    def check_nx_np(self):
        self.assertGreaterEqual(self.data.np, self.data.nx * 2)

    def setUp(self):
        self.data.lmin = 1
        self.data.lmax = 10

    def test_np_l_nx(self):
        """
         np < nx
        """
        self.data.np = 3
        self.data.nx = 10
        self.check_nx_np()

    def test_np_e_nx(self):
        """
        np = nx
        """
        self.data.np = 5
        self.data.nx = 5
        self.check_nx_np()

    def test_np_g_nx(self):
        """
        np > nx
        """
        self.data.np = 234
        self.data.nx = 3
        self.check_nx_np()

    def test_nx_l_np(self):
        """
        nx < np
        """
        self.data.nx = 12
        self.data.np = 523
        self.check_nx_np()

    def test_nx_g_np(self):
        """
        nx > np
        """
        self.data.nx = 300
        self.data.np = 3
        self.check_nx_np()

    def test_lmax_l_nx(self):
        """
        lmax < nx
        """
        self.data.lmax = 1
        self.data.nx = 100
        self.check_lmax_nx()

    def test_lmax_e_nx(self):
        """
        lmax == nx
        """
        self.data.lmax = 100
        self.data.nx = 100
        self.check_lmax_nx()

    def test_lmax_g_nx(self):
        """
        lmax > nx
        """
        self.data.lmax = 100
        self.data.nx = 1
        self.check_lmax_nx()


if __name__ == '__main__':
    unittest.main()