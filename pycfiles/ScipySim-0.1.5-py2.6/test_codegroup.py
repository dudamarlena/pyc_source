# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/gui/test_codegroup.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on 9/02/2010

@author: brian
"""
import unittest
from codegroup import make_tree, fill_tree
import os
from Tkinter import Tk

class TestCodeGroup(unittest.TestCase):

    def setUp(self):
        src_dir = os.path.normpath(__file__ + '../../../')
        self.actor_dir = os.path.join(src_dir, 'actors')
        self.model_dir = os.path.join(src_dir, 'models')
        self.fakeroot = Tk()

    def tearDown(self):
        pass

    def testParsingAllActors(self):
        """Parse the actors directory and create code group """
        make_tree(self.fakeroot, self.actor_dir)

    def testParsingAllModels(self):
        """Parse all the models"""
        make_tree(self.fakeroot, self.model_dir)


if __name__ == '__main__':
    unittest.main()