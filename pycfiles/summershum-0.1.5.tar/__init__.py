# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/threebean/devel/summershum/tests/__init__.py
# Compiled at: 2014-02-08 03:51:04
"""
Unit-tests.
"""
import unittest, shutil, sys, os
from datetime import date
from datetime import timedelta
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import summershum.utils

class UtilsTest(unittest.TestCase):
    """ summershum.utils tests. """

    def setUp(self):
        """ Set up the environnment, ran before every tests. """
        if os.path.exists('root'):
            shutil.rmtree('root')

    def test_walk_directory(self):
        """ Test the walk_directory function. """
        os.makedirs('root/fold1/fold2/fold3')
        os.makedirs('root/fold1/fold2/fold4')
        os.makedirs('root/fold1/fold2.5')
        open('root/file1', 'w').close()
        open('root/fold1/file2', 'w').close()
        open('root/fold1/file3', 'w').close()
        open('root/fold1/fold2/file4', 'w').close()
        open('root/fold1/fold2/fold3/file5', 'w').close()
        open('root/fold1/fold2/fold4/file6', 'w').close()
        open('root/fold1/fold2.5/file6', 'w').close()
        exp_list = [
         ('root/file1', 'da39a3ee5e6b4b0d3255bfef95601890afd80709'),
         ('root/fold1/file3', 'da39a3ee5e6b4b0d3255bfef95601890afd80709'),
         ('root/fold1/file2', 'da39a3ee5e6b4b0d3255bfef95601890afd80709'),
         ('root/fold1/fold2.5/file6', 'da39a3ee5e6b4b0d3255bfef95601890afd80709'),
         ('root/fold1/fold2/file4', 'da39a3ee5e6b4b0d3255bfef95601890afd80709'),
         ('root/fold1/fold2/fold4/file6', 'da39a3ee5e6b4b0d3255bfef95601890afd80709'),
         ('root/fold1/fold2/fold3/file5', 'da39a3ee5e6b4b0d3255bfef95601890afd80709')]
        obs_list = list(summershum.utils.walk_directory('root'))
        self.assertTrue(exp_list, obs_list)
        shutil.rmtree('root')


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(UtilsTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)