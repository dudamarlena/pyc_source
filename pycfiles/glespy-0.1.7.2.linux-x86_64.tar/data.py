# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/test_data/data.py
# Compiled at: 2013-11-25 11:17:10
__author__ = 'yarnaid'
import os, inspect
map_name = 'test_map.fit'
alm_name = 'alm.fit'
alm_100_name = 'alm_100.fit'
mask_name = 'mask.fit'
points_name = 'points.dat'
cl_name = 'ilc_cl.txt'

class WithTestData(object):
    data_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    attrs = {'nx': 61, 
       'np': 122}

    def __init__(self):
        super().__init__()
        self.init_data()

    def check_exist(self, name):
        self.assertTrue(os.path.exists(name))
        self.assertGreater(os.path.getsize(name), 0)

    def init_data(self):
        self.map_name = os.path.join(self.data_path, map_name)
        self.alm_name = os.path.join(self.data_path, alm_name)
        self.alm_100_name = os.path.join(self.data_path, alm_100_name)
        self.mask_name = os.path.join(self.data_path, mask_name)
        self.points_name = os.path.join(self.data_path, points_name)
        self.cl_name = os.path.join(self.data_path, cl_name)