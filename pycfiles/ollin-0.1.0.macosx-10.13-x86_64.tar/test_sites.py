# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/test/test_sites.py
# Compiled at: 2018-10-19 09:51:47
import unittest, numpy as np, sys
sys.path.append('../')
import ollin

class TestSites(unittest.TestCase):

    def test_range_inputs(self):
        random_niche = np.random.random(size=(20, 20))
        r = 10
        site = ollin.BaseSite(r, random_niche)
        self.assertTrue((site.range == np.array([float(r), float(r)])).all())
        self.assertTrue(site.range.dtype == np.float)
        r = 15.0
        site = ollin.BaseSite(r, random_niche)
        self.assertTrue((site.range == np.array([r, r])).all())
        self.assertTrue(site.range.dtype == np.float)
        r = (10, 20.0)
        site = ollin.BaseSite(r, random_niche)
        self.assertTrue((site.range == np.array(r)).all())
        self.assertTrue(site.range.dtype == np.float)
        r = [
         10, 20.0]
        site = ollin.BaseSite(r, random_niche)
        self.assertTrue((site.range == np.array(r)).all())
        self.assertTrue(site.range.dtype == np.float)
        r = np.array([10.0, 20.0])
        site = ollin.BaseSite(r, random_niche)
        self.assertTrue((site.range == r).all())
        self.assertTrue(site.range.dtype == np.float)