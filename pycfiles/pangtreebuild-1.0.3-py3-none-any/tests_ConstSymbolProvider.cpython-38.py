# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paulina/pangtree/pangtreebuild/tests/tests_pangenome/fasta_providers/tests_ConstSymbolProvider.py
# Compiled at: 2019-12-30 15:48:57
# Size of source mod 2**32: 1184 bytes
import unittest
from pangtreebuild.pangenome import graph
from pangtreebuild.pangenome.parameters import missings, msa

class ConstSymbolProviderTests(unittest.TestCase):

    def test_1_no_symbol_provided(self):
        missing_symbol = missings.MissingBase()
        const_symbol_provider = missings.ConstBaseProvider(missing_symbol)
        expected_symbol = graph.Base('?')
        actual_symbol = const_symbol_provider.get_base(msa.SequenceID('s'), 0)
        self.assertEqual(expected_symbol, actual_symbol)

    def test_2_symbol_provided(self):
        const_symbol_provider = missings.ConstBaseProvider(missings.MissingBase('*'))
        expected_symbol = graph.Base('*')
        actual_symbol = const_symbol_provider.get_base(msa.SequenceID('s'), 0)
        self.assertEqual(expected_symbol, actual_symbol)

    def test_3_incorrect_missing_symbol(self):
        with self.assertRaises(ValueError) as (e):
            _ = missings.MissingBase('**')
        expected_message = 'Missing symbol must be a single character.'
        actual_message = str(e.exception)
        self.assertEqual(expected_message, actual_message)


if __name__ == '__main__':
    unittest.main()