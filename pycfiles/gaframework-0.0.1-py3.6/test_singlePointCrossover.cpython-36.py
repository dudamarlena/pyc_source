# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/test_singlePointCrossover.py
# Compiled at: 2019-06-14 12:47:56
# Size of source mod 2**32: 1286 bytes
from unittest import TestCase
from GaPy.population import *
from GaPy.single_point_crossover import *

def fitness(chromosome):
    return 0.5


def create_parents():
    parents = Chromosome.create(16, 2)
    parents[0].genes = [
     1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    parents[1].genes = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    return parents


class TestSinglePointCrossover(TestCase):

    def test__crossover(self):
        parents = create_parents()
        crossover = SinglePointCrossover()
        children = crossover._crossover(parents, 2)
        self.assertEqual('1100000011111111', str(children[0]))
        self.assertEqual('0011111100000000', str(children[1]))
        crossover = SinglePointCrossover()
        children = crossover._crossover(parents, 0)
        self.assertEqual(str(parents[1]), str(children[0]))
        self.assertEqual(str(parents[0]), str(children[1]))
        crossover = SinglePointCrossover()
        children = crossover._crossover(parents, 16)
        self.assertEqual(str(parents[0]), str(children[0]))
        self.assertEqual(str(parents[1]), str(children[1]))