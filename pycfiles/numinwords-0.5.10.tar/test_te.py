# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_te.py
# Compiled at: 2020-04-17 01:14:34
from unittest import TestCase
from numinwords import numinwords

class numinwordsTETest(TestCase):

    def test_numbers(self):
        self.assertEqual(numinwords(66, lang='te'), 'అరవై ఆరు')
        self.assertEqual(numinwords(1734, lang='te'), 'ఒకటి వేయి ఏడు వందల ముప్పై నాలుగు')
        self.assertEqual(numinwords(134, lang='te'), 'ఒకటి వందల ముప్పై నాలుగు')
        self.assertEqual(numinwords(54411, lang='te'), 'యాభై నాలుగు వేయి నాలుగు వందల పదకొండు')
        self.assertEqual(numinwords(42, lang='te'), 'నలభై రెండు')
        self.assertEqual(numinwords(893, lang='te'), 'ఎనిమిది వందల తొంభై మూడు')
        self.assertEqual(numinwords(1729, lang='te'), 'ఒకటి వేయి ఏడు వందల ఇరవై తొమ్మిది')
        self.assertEqual(numinwords(123, lang='te'), 'ఒకటి వందల ఇరవై మూడు')
        self.assertEqual(numinwords(32211, lang='te'), 'ముప్పై రెండు వేయి రెండు వందల పదకొండు')

    def test_cardinal_for_float_number(self):
        self.assertEqual(numinwords(1.61803, lang='te'), 'ఒకటి బిందువు  ఆరు ఒకటి ఎనిమిది సున్న మూడు')
        self.assertEqual(numinwords(34.876, lang='te'), 'ముప్పై నాలుగు బిందువు  ఎనిమిది ఏడు ఆరు')
        self.assertEqual(numinwords(3.14, lang='te'), 'మూడు బిందువు  ఒకటి నాలుగు')

    def test_ordinal(self):
        self.assertEqual(numinwords(1, lang='te', to='ordinal'), 'ఒకటివ')
        self.assertEqual(numinwords(22, lang='te', to='ordinal'), 'ఇరవై రెండువ')
        self.assertEqual(numinwords(23, lang='te', to='ordinal'), 'ఇరవై మూడువ')
        self.assertEqual(numinwords(12, lang='te', to='ordinal'), 'పన్నెండువ')
        self.assertEqual(numinwords(130, lang='te', to='ordinal'), 'ఒకటి వందల ముప్పైవ')
        self.assertEqual(numinwords(1003, lang='te', to='ordinal'), 'ఒకటి వేయిల మూడువ')
        self.assertEqual(numinwords(4, lang='te', to='ordinal'), 'నాలుగువ')

    def test_ordinal_num(self):
        self.assertEqual(numinwords(2, lang='te', to='ordinal_num'), '2వ')
        self.assertEqual(numinwords(3, lang='te', to='ordinal_num'), '3వ')
        self.assertEqual(numinwords(5, lang='te', to='ordinal_num'), '5వ')
        self.assertEqual(numinwords(16, lang='te', to='ordinal_num'), '16వ')
        self.assertEqual(numinwords(113, lang='te', to='ordinal_num'), '113వ')