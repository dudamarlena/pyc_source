# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/project2_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 909 bytes
import copy, unittest
from bibliopixel.project import project
from bibliopixel.animation.sequence import Sequence
from bibliopixel.animation import matrix
from bibliopixel.layout.matrix import Matrix
from bibliopixel.project.data_maker import Maker

def classname(c):
    return (
     '%s.%s' % c.__module__, c.__name__)


class Project2Test(unittest.TestCase):

    def test_empty(self):
        project.project()

    def test_single(self):
        source = {'animation':'bibliopixel.animation.matrix.Matrix', 
         'shape':[
          23, 32]}
        pr = project.project(source)
        self.assertEqual([
         matrix.Matrix, 1, Matrix, Maker, 23, 32], [
         type(pr.animation),
         len(pr.drivers),
         type(pr.layout),
         type(pr.maker),
         pr.layout.width,
         pr.layout.height])