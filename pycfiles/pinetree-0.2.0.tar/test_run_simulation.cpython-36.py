# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/Box Sync/projects/2017/pinetree/tests/test_run_simulation.py
# Compiled at: 2018-01-26 16:22:56
# Size of source mod 2**32: 1635 bytes
import unittest, subprocess, tempfile, importlib

class MainTest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tempdir.cleanup()

    def run_test(self, prefix):
        test_mod = importlib.import_module('.params.' + prefix, 'tests')
        out_prefix = self.tempdir.name + '/' + prefix
        test_mod.execute(out_prefix)
        with open('tests/output/' + prefix + '_counts.tsv') as (f):
            text = f.read()
        with open(out_prefix + '_counts.tsv') as (results_file):
            results = results_file.read()
        self.assertEqual(results, text)

    def test_single_gene(self):
        self.run_test('single_gene')


if __name__ == '__main__':
    unittest.main()