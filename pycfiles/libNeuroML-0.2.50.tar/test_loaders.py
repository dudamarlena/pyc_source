# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/padraig/libNeuroML/neuroml/test/test_loaders.py
# Compiled at: 2019-11-06 05:47:09
"""
Unit tests for loaders

"""
import neuroml
from neuroml import loaders
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestNeuroMLLoader(unittest.TestCase):

    def test_load_neuroml(self):
        root_dir = os.path.dirname(neuroml.__file__)
        print 'root dir is:'
        print root_dir
        test_file_path = os.path.join(root_dir, 'examples/test_files/Purk2M9s.nml')
        print 'test file path is:'
        print test_file_path
        f = open(test_file_path, 'r')
        doc = loaders.NeuroMLLoader.load(test_file_path)
        self.assertEqual(doc.id, 'Purk2M9s')