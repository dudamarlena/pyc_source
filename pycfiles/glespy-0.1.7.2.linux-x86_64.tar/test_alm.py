# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/test/test_alm.py
# Compiled at: 2013-09-14 06:41:10
import os
__author__ = 'yarnaid'
import unittest
try:
    import test_data.data as Data, alm as Alm
except:
    import glespy.test_data.data as Data, glespy.alm as Alm

class AlmTests(unittest.TestCase, Data.WithTestData):

    def setUp(self):
        super(AlmTests, self).setUp()
        self.init_data()
        self.check_exist(self.alm_100_name)

    def check_exist(self, name):
        self.assertTrue(os.path.exists(name))
        self.assertGreater(os.path.getsize(name), 0)

    def test_to_map(self):
        alm = Alm.Alm(name=self.alm_100_name, lmax=100)
        pmap = alm.to_map(nx=30)
        self.check_exist(pmap.name)
        os.remove(pmap.name)