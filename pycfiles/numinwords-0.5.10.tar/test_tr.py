# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_tr.py
# Compiled at: 2020-04-17 01:14:39
from unittest import TestCase
from numinwords import numinwords

class numinwordsTRTest(TestCase):

    def test_tr(self):
        testlang = 'tr'
        testcases = [{'test': 0, 'to': 'currency', 'expected': 'bedelsiz'}, {'test': 1.1, 'to': 'currency', 'expected': 'birliraonkuruş'}, {'test': 2000, 'to': 'currency', 'expected': 'ikibinlira'}, {'test': 110000, 'to': 'currency', 'expected': 'yüzonbinlira'},
         {'test': 1002000, 'to': 'currency', 'expected': 'birmilyonikibinlira'},
         {'test': 1002001, 'to': 'currency', 'expected': 'birmilyonikibinbirlira'},
         {'test': 1100000, 'to': 'currency', 'expected': 'birmilyonyüzbinlira'}, {'test': 1, 'to': 'ordinal', 'expected': 'birinci'}, {'test': 2, 'to': 'ordinal', 'expected': 'ikinci'}, {'test': 9, 'to': 'ordinal', 'expected': 'dokuzuncu'}, {'test': 10, 'to': 'ordinal', 'expected': 'onuncu'}, {'test': 11, 'to': 'ordinal', 'expected': 'onbirinci'}, {'test': 44, 'to': 'ordinal', 'expected': 'kırkdördüncü'}, {'test': 100, 'to': 'ordinal', 'expected': 'yüzüncü'}, {'test': 101, 'to': 'ordinal', 'expected': 'yüzbirinci'}, {'test': 103, 'to': 'ordinal', 'expected': 'yüzüçüncü'}, {'test': 110, 'to': 'ordinal', 'expected': 'yüzonuncu'}, {'test': 111, 'to': 'ordinal', 'expected': 'yüzonbirinci'}, {'test': 1000, 'to': 'ordinal', 'expected': 'bininci'}, {'test': 1001, 'to': 'ordinal', 'expected': 'binbirinci'}, {'test': 1010, 'to': 'ordinal', 'expected': 'binonuncu'}, {'test': 1011, 'to': 'ordinal', 'expected': 'binonbirinci'}, {'test': 1100, 'to': 'ordinal', 'expected': 'binyüzüncü'}, {'test': 1110, 'to': 'ordinal', 'expected': 'binyüzonuncu'},
         {'test': 2341, 'to': 'ordinal', 'expected': 'ikibinüçyüzkırkbirinci'}, {'test': 10000, 'to': 'ordinal', 'expected': 'onbininci'}, {'test': 10010, 'to': 'ordinal', 'expected': 'onbinonuncu'}, {'test': 10100, 'to': 'ordinal', 'expected': 'onbinyüzüncü'}, {'test': 10110, 'to': 'ordinal', 'expected': 'onbinyüzonuncu'}, {'test': 11000, 'to': 'ordinal', 'expected': 'onbirbininci'}, {'test': 35000, 'to': 'ordinal', 'expected': 'otuzbeşbininci'},
         {'test': 116331, 'to': 'ordinal', 'expected': 'yüzonaltıbinüçyüzotuzbirinci'},
         {'test': 116330, 'to': 'ordinal', 'expected': 'yüzonaltıbinüçyüzotuzuncu'}, {'test': 100000, 'to': 'ordinal', 'expected': 'yüzbininci'},
         {'test': 501000, 'to': 'ordinal', 'expected': 'beşyüzbirbininci'},
         {'test': 1000111, 'to': 'ordinal', 'expected': 'birmilyonyüzonbirinci'},
         {'test': 111000111, 'to': 'ordinal', 'expected': 'yüzonbirmilyonyüzonbirinci'},
         {'test': 111001111, 'to': 'ordinal', 'expected': 'yüzonbirmilyonbinyüzonbirinci'},
         {'test': 111111111, 'to': 'ordinal', 'expected': 'yüzonbirmilyonyüzonbirbinyüzonbirinci'},
         {'test': 100001000, 'to': 'ordinal', 'expected': 'yüzmilyonbininci'},
         {'test': 100001001, 'to': 'ordinal', 'expected': 'yüzmilyonbinbirinci'},
         {'test': 100010000, 'to': 'ordinal', 'expected': 'yüzmilyononbininci'},
         {'test': 100010001, 'to': 'ordinal', 'expected': 'yüzmilyononbinbirinci'},
         {'test': 100011000, 'to': 'ordinal', 'expected': 'yüzmilyononbirbininci'},
         {'test': 100011001, 'to': 'ordinal', 'expected': 'yüzmilyononbirbinbirinci'},
         {'test': 101011001, 'to': 'ordinal', 'expected': 'yüzbirmilyononbirbinbirinci'},
         {'test': 101011010, 'to': 'ordinal', 'expected': 'yüzbirmilyononbirbinonuncu'},
         {'test': 1101011010, 'to': 'ordinal', 'expected': 'birmilyaryüzbirmilyononbirbinonuncu'},
         {'test': 101101011010, 'to': 'ordinal', 'expected': 'yüzbirmilyaryüzbirmilyononbirbinonuncu'},
         {'test': 1000000000001, 'to': 'ordinal', 'expected': 'birtrilyonbirinci'}, {'test': 1.2, 'to': 'ordinal', 'expected': ''}, {'test': 1.3, 'to': 'ordinal', 'expected': ''}, {'test': 3000, 'to': 'ordinal', 'expected': 'üçbininci'}, {'test': 120000, 'to': 'ordinal', 'expected': 'yüzyirmibininci'},
         {'test': 1002002, 'to': 'ordinal', 'expected': 'birmilyonikibinikinci'},
         {'test': 1003000, 'to': 'ordinal', 'expected': 'birmilyonüçbininci'},
         {'test': 1200000, 'to': 'ordinal', 'expected': 'birmilyonikiyüzbininci'}, {'test': 1, 'to': 'cardinal', 'expected': 'bir'}, {'test': 2, 'to': 'cardinal', 'expected': 'iki'}, {'test': 9, 'to': 'cardinal', 'expected': 'dokuz'}, {'test': 10, 'to': 'cardinal', 'expected': 'on'}, {'test': 11, 'to': 'cardinal', 'expected': 'onbir'}, {'test': 44, 'to': 'cardinal', 'expected': 'kırkdört'}, {'test': 100, 'to': 'cardinal', 'expected': 'yüz'}, {'test': 101, 'to': 'cardinal', 'expected': 'yüzbir'}, {'test': 103, 'to': 'cardinal', 'expected': 'yüzüç'}, {'test': 110, 'to': 'cardinal', 'expected': 'yüzon'}, {'test': 111, 'to': 'cardinal', 'expected': 'yüzonbir'}, {'test': 1000, 'to': 'cardinal', 'expected': 'bin'}, {'test': 1001, 'to': 'cardinal', 'expected': 'binbir'}, {'test': 1010, 'to': 'cardinal', 'expected': 'binon'}, {'test': 1011, 'to': 'cardinal', 'expected': 'binonbir'}, {'test': 1100, 'to': 'cardinal', 'expected': 'binyüz'}, {'test': 1110, 'to': 'cardinal', 'expected': 'binyüzon'},
         {'test': 2341, 'to': 'cardinal', 'expected': 'ikibinüçyüzkırkbir'}, {'test': 10000, 'to': 'cardinal', 'expected': 'onbin'}, {'test': 10010, 'to': 'cardinal', 'expected': 'onbinon'}, {'test': 10100, 'to': 'cardinal', 'expected': 'onbinyüz'}, {'test': 10110, 'to': 'cardinal', 'expected': 'onbinyüzon'}, {'test': 11000, 'to': 'cardinal', 'expected': 'onbirbin'}, {'test': 35000, 'to': 'cardinal', 'expected': 'otuzbeşbin'},
         {'test': 116331, 'to': 'cardinal', 'expected': 'yüzonaltıbinüçyüzotuzbir'},
         {'test': 116330, 'to': 'cardinal', 'expected': 'yüzonaltıbinüçyüzotuz'}, {'test': 500000, 'to': 'cardinal', 'expected': 'beşyüzbin'}, {'test': 501000, 'to': 'cardinal', 'expected': 'beşyüzbirbin'},
         {'test': 1000111, 'to': 'cardinal', 'expected': 'birmilyonyüzonbir'},
         {'test': 111000111, 'to': 'cardinal', 'expected': 'yüzonbirmilyonyüzonbir'},
         {'test': 111001111, 'to': 'cardinal', 'expected': 'yüzonbirmilyonbinyüzonbir'},
         {'test': 111111111, 'to': 'cardinal', 'expected': 'yüzonbirmilyonyüzonbirbinyüzonbir'},
         {'test': 100001000, 'to': 'cardinal', 'expected': 'yüzmilyonbin'},
         {'test': 100001001, 'to': 'cardinal', 'expected': 'yüzmilyonbinbir'},
         {'test': 100010000, 'to': 'cardinal', 'expected': 'yüzmilyononbin'},
         {'test': 100010001, 'to': 'cardinal', 'expected': 'yüzmilyononbinbir'},
         {'test': 100011000, 'to': 'cardinal', 'expected': 'yüzmilyononbirbin'},
         {'test': 100011001, 'to': 'cardinal', 'expected': 'yüzmilyononbirbinbir'},
         {'test': 101011001, 'to': 'cardinal', 'expected': 'yüzbirmilyononbirbinbir'},
         {'test': 101011010, 'to': 'cardinal', 'expected': 'yüzbirmilyononbirbinon'},
         {'test': 1101011010, 'to': 'cardinal', 'expected': 'birmilyaryüzbirmilyononbirbinon'},
         {'test': 101101011010, 'to': 'cardinal', 'expected': 'yüzbirmilyaryüzbirmilyononbirbinon'},
         {'test': 1000000000001, 'to': 'cardinal', 'expected': 'birtrilyonbir'}, {'test': 0.01, 'to': 'cardinal', 'expected': 'sıfırvirgülbir'},
         {'test': 0.21, 'to': 'cardinal', 'expected': 'sıfırvirgülyirmibir'}, {'test': 0.1, 'to': 'cardinal', 'expected': 'sıfırvirgülon'}, {'test': 1.01, 'to': 'cardinal', 'expected': 'birvirgülbir'}, {'test': 1.1, 'to': 'cardinal', 'expected': 'birvirgülon'},
         {'test': 1.21, 'to': 'cardinal', 'expected': 'birvirgülyirmibir'},
         {'test': 101101011010.02, 'to': 'cardinal', 'expected': 'yüzbirmilyaryüzbirmilyononbirbinonvirgüliki'},
         {'test': 101101011010.2, 'to': 'cardinal', 'expected': 'yüzbirmilyaryüzbirmilyononbirbinonvirgülyirmi'}]
        for casedata in testcases:
            self.assertEqual(numinwords(casedata['test'], lang=testlang, to=casedata['to']), casedata['expected'])