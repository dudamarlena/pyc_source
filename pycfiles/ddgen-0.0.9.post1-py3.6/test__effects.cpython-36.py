# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddgen/utils/test__effects.py
# Compiled at: 2020-03-24 14:57:35
# Size of source mod 2**32: 720 bytes
import unittest, ddgen.utils as u

class TestEffects(unittest.TestCase):

    def test_effect_ranks(self):
        self.assertEqual(u.VARIANT_EFFECT_PRIORITIES['CHROMOSOME_NUMBER_VARIATION'], 0)
        self.assertEqual(u.VARIANT_EFFECT_PRIORITIES['SEQUENCE_VARIANT'], 68)

    def test_get_priority(self):
        self.assertEqual(u.get_variant_effect_priority('EXON_LOSS_VARIANT'), 2)
        self.assertEqual(u.get_variant_effect_priority('TRANSLOCATION'), 5)
        self.assertEqual(u.get_variant_effect_priority('MISSENSE_VARIANT'), 21)
        self.assertEqual(u.get_variant_effect_priority('gibberish'), -1)
        self.assertEqual(u.get_variant_effect_priority(''), -1)