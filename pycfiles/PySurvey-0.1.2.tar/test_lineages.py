# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathanfriedman/Dropbox/python_dev_library/PySurvey/pysurvey/tests/test_lineages.py
# Compiled at: 2013-04-02 22:18:51
"""
Created on Dec 20, 2011

@author: jonathanfriedman
"""
import unittest, numpy as np, pysurvey.core.Lineages as lin

class TestLineages(unittest.TestCase):

    def setUp(self):
        self.qiime_lines = [
         'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Veillonellaceae;g__;s__',
         'k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__;f__;g__;s__k__Bacteria;p__Proteobacteria;c__Betaproteobacteria;o__;f__;g__;s__']
        self.hmp_lines = [
         'Root(100);Bacteria(100);"Firmicutes"(100);"Bacilli"(100);Bacillales(100);Bacillaceae(99);Bacillus(99);',
         'Root(100);Bacteria(100);"Firmicutes"(100);"Clostridia"(100);Clostridiales(100);']
        self.rdp_lines = ['Bacteria\tdomain\t1.0\t"Proteobacteria"\tphylum\t1.0\tBetaproteobacteria\tclass\t0.98\tBurkholderiales\torder\t0.97\tComamonadaceae\tfamily\t0.85\tAcidovorax\tgenus\t0.69',
         'Bacteria\tdomain\t0.98\tOD1\tphylum\t0.47\t\t\t\t\t\t\t\t\t\tOD1_genera_incertae_sedis\tgenus\t0.47']

    def test_qiime_parsing(self):
        l = lin.Lineage(lin_str=self.qiime_lines[0])
        assert l.lin['k'] == 'Bacteria'
        assert l.lin['f'] == 'Veillonellaceae'
        assert l.lin['s'] == lin._unassigned_str
        assert l.conf['k'] == lin._unassigned_str
        assert l.conf['s'] == lin._unassigned_str

    def test_hmp_parsing(self):
        l = lin.Lineage(lin_str=self.hmp_lines[1], format='hmp')
        assert l.lin['k'] == 'Bacteria'
        assert l.lin['o'] == 'Clostridiales'
        assert l.lin['s'] == lin._unassigned_str
        assert l.conf['k'] == 100
        assert l.conf['s'] == 0

    def test_rdp_parsing(self):
        l = lin.Lineage(lin_str=self.rdp_lines[1], format='rdp')
        assert l.lin['k'] == 'Bacteria'
        assert l.lin['f'] == lin._unassigned_str
        assert l.lin['g'] == 'OD1_genera_incertae_sedis'
        assert l.lin['s'] == lin._unassigned_str
        assert l.conf['k'] == 0.98
        assert l.conf['f'] == 0
        assert l.conf['g'] == 0.47
        assert l.conf['s'] == 0


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x'], exit=False)