# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/meren/Desktop/MBL/Oligotyping/oligotyping/Unittests/_utils.py
# Compiled at: 2013-03-29 19:50:18
import os, shutil, unittest, collections
Compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
import Oligotyping.utils.utils
my_path = os.path.dirname(os.path.realpath(__file__))

class Tests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_Multiprocessing(self):
        m = Oligotyping.utils.utils.Multiprocessing(lambda x: x)
        m.num_thread = 3
        chunks_normal = m.get_data_chunks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.assertTrue(chunks_normal == [[1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11]])
        chunks_spiral = m.get_data_chunks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], spiral=True)
        self.assertTrue(chunks_spiral == [[1, 4, 7, 10], [2, 5, 8, 11], [3, 6, 9]])