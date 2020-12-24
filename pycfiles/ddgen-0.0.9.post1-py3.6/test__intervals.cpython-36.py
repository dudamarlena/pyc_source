# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddgen/utils/test__intervals.py
# Compiled at: 2020-03-24 14:57:35
# Size of source mod 2**32: 1489 bytes
import unittest
from pkg_resources import resource_filename
from ddgen.utils import GenomeIntervalGenerator

class TestGenomeIntervalGenerator(unittest.TestCase):

    def setUp(self) -> None:
        self.test_dict_path = resource_filename(__name__, 'test_data/test.dict')

    def test_load_bundled_seq_dicts(self) -> None:
        import ddgen.test_utils as tu
        gig = GenomeIntervalGenerator('hg19')
        self.assertTupleEqual(gig.get_known_contigs(), tu.expected_hg19_contigs)
        gig = GenomeIntervalGenerator('hg38')
        self.assertTupleEqual(gig.get_known_contigs(), tu.expected_hg38_contigs)

    def test_load_other_seq_dict(self) -> None:
        gig = GenomeIntervalGenerator(self.test_dict_path)
        self.assertTupleEqual(gig.get_known_contigs(), ('chr1', 'chr2'))

    def test_interval_generator(self) -> None:
        gig = GenomeIntervalGenerator(self.test_dict_path)
        expected = [
         ('chr1', 1, 99), ('chr1', 100, 100), ('chr2', 1, 99), ('chr2', 100, 198), ('chr2', 199, 200)]
        actual = [x for x in gig.get_regions(99)]
        self.assertListEqual(actual, expected)

    def test_interval_generator_bad_contigs(self):
        gig = GenomeIntervalGenerator(self.test_dict_path)
        with self.assertRaises(ValueError) as (ctx):
            gig.get_regions(100, contigs='something')
        self.assertTrue("Expected list/set/tuple with contig names or 'all', got <class 'str'>" in str(ctx.exception))