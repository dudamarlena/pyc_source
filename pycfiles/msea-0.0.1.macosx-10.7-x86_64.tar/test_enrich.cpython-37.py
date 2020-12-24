# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zichen/Documents/Yan/MSEA_python_package/venv37/lib/python3.7/site-packages/tests/test_enrich.py
# Compiled at: 2020-03-28 13:18:10
# Size of source mod 2**32: 1747 bytes
from unittest import TestCase
import msea
from msea import SetLibrary

class TestEnrich(TestCase):

    def setUp(self):
        self.set_lib = SetLibrary.load(gmt_file='msea/data/human_genes_associated_microbes/set_library.gmt',
          rank_means_file='msea/data/human_genes_associated_microbes/rank_means.npy',
          rank_stds_file='msea/data/human_genes_associated_microbes/rank_stds.npy')
        self.microbe_set_input = set(['Colwellia',
         'Deinococcus',
         'Idiomarina',
         'Neisseria',
         'Pseudidiomarina',
         'Pseudoalteromonas'])

    def test_enrich(self):
        set_lib = self.set_lib
        enrich_results = msea.enrich(self.microbe_set_input, set_lib.d_gmt, set_lib.rank_means, set_lib.rank_stds)
        expected_columns = [
         'oddsratio',
         'pvalue',
         'qvalue',
         'zscore',
         'combined_score',
         'shared',
         'n_shared']
        self.assertSetEqual(set(enrich_results.columns), set(expected_columns))

    def test_enrich_no_adjustment(self):
        set_lib = self.set_lib
        enrich_results = msea.enrich(self.microbe_set_input, set_lib.d_gmt)
        expected_columns = ['oddsratio',
         'pvalue',
         'qvalue',
         'shared',
         'n_shared']
        self.assertSetEqual(set(enrich_results.columns), set(expected_columns))