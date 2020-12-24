# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/tests/test_projectcreator.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 1102 bytes
import unittest, os, sys, shutil
sys.path.append('.')
from reademptionlib.projectcreator import ProjectCreator

class TestProjectCreator(unittest.TestCase):

    def setUp(self):
        self.root_folder_name = 'a_test_project'
        self.projectcreator = ProjectCreator()

    def tearDown(self):
        if os.path.exists(self.root_folder_name):
            shutil.rmtree(self.root_folder_name)

    def test_create_root_folder(self):
        self.projectcreator.create_root_folder(self.root_folder_name)
        assert os.path.exists(self.root_folder_name)
        shutil.rmtree(self.root_folder_name)

    def test_create_subfolders(self):
        self.projectcreator.create_root_folder(self.root_folder_name)
        subfolders = ['test_a', 'test_b', 'test_c']
        subfolders = [self.root_folder_name + '/' + subfolder for subfolder in subfolders]
        self.projectcreator.create_subfolders(subfolders)
        for subfolder in subfolders:
            assert os.path.exists(subfolder)


if __name__ == '__main__':
    unittest.main()