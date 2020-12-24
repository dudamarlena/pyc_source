# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/Box Sync/projects/2018/pinetree/tests/reaction_test.py
# Compiled at: 2018-05-28 14:59:44
# Size of source mod 2**32: 546 bytes
import unittest, pinetree as pt

class TestSpeciesReactionMethods(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(ValueError):
            rxn = pt.SpeciesReaction(-1.0, 1.0, ['x'], ['y'])
        with self.assertRaises(ValueError):
            rxn = pt.SpeciesReaction(1.0, -1.0, ['x'], ['y'])
        with self.assertRaises(ValueError):
            rxn = pt.SpeciesReaction(1.0, 1.0, ['x', 'z', 'm'], ['y'])
        with self.assertRaises(ValueError):
            rxn = pt.SpeciesReaction(1.0, 1.0, [], [])