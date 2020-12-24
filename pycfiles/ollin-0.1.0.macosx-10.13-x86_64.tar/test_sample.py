# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/test/test_sample.py
# Compiled at: 2018-10-19 09:51:47
import unittest, random, sys
sys.path.append('../')
import ollin

class TestSample(unittest.TestCase):

    def test_sample(self):
        self.assertTrue(True)

    def test_site_creation(self):
        niche_size = random.random()
        site = ollin.Site.make_random(niche_size)
        self.assertTrue(abs(site.niche_size - niche_size) < 0.1)