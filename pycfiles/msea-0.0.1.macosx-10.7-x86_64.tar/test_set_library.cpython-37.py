# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zichen/Documents/Yan/MSEA_python_package/venv37/lib/python3.7/site-packages/tests/test_set_library.py
# Compiled at: 2020-03-28 13:18:03
# Size of source mod 2**32: 2840 bytes
from unittest import TestCase
import msea
from msea import SetLibrary

class TestSetLibrary(TestCase):

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
        self.bad_input_set = set(['foo', 'bar', 'baz'])

    def test_load(self):
        set_lib = self.set_lib
        self.assertEqual(len(set_lib.d_gmt), 1286)
        self.assertEqual(set_lib.rank_means.shape, (1286, ))
        self.assertEqual(set_lib.rank_stds.shape, (1286, ))
        self.assertEqual(len(set_lib.all_items), 566)

    def test_get_empirical_ranks(self):
        set_lib = self.set_lib
        set_lib.rank_means = None
        set_lib.rank_stds = None
        set_lib.get_empirical_ranks(n=10)
        self.assertEqual(set_lib.rank_means.shape, (1286, ))
        self.assertEqual(set_lib.rank_stds.shape, (1286, ))

    def test_enrich_exception(self):
        set_lib = self.set_lib
        self.assertRaises(ValueError, lambda : set_lib.enrich(self.bad_input_set))

    def test_enrich_warning(self):
        set_lib = self.set_lib
        self.assertWarns(RuntimeWarning, lambda : set_lib.enrich(self.bad_input_set | self.microbe_set_input))

    def test_enrich(self):
        set_lib = self.set_lib
        enrich_results = set_lib.enrich((self.microbe_set_input),
          adjust=True, universe=2000)
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
        enrich_results = set_lib.enrich((self.microbe_set_input),
          adjust=False, universe=2000)
        expected_columns = ['oddsratio',
         'pvalue',
         'qvalue',
         'shared',
         'n_shared']
        self.assertSetEqual(set(enrich_results.columns), set(expected_columns))