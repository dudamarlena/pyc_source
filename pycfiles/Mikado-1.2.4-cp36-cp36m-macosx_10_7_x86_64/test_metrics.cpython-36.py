# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/venturil/workspace/mikado/Mikado/tests/test_metrics.py
# Compiled at: 2018-05-23 17:14:36
# Size of source mod 2**32: 8857 bytes
__author__ = 'Luca Venturini'
import unittest
from Mikado.loci import Transcript
from Mikado.utilities.log_utils import create_default_logger

class TestMetricsEndDistances(unittest.TestCase):
    logger = create_default_logger('End')
    logger.setLevel('ERROR')

    def setUp(self):
        self.tr = Transcript()
        self.tr.logger = self.logger
        self.tr.start = 101
        self.tr.end = 10000
        self.tr.add_exons([(101, 300),
         (501, 800),
         (1001, 1200),
         (1301, 2000),
         (3501, 5000),
         (5501, 6000),
         (6201, 7000),
         (7301, 7700),
         (8201, 9000),
         (9101, 9300),
         (9501, 9700),
         (9801, 10000)])
        self.tr.id = 'test1'
        self.tr.parent = 'test1.gene'

    def test_end_positive(self):
        self.tr.strand = '+'
        cds = [
         (1161, 1200),
         (1301, 2000),
         (3501, 5000),
         (5501, 6000),
         (6201, 7000),
         (7301, 7700),
         (8201, 9000),
         (9101, 9130)]
        self.tr.add_exons(cds, features='CDS')
        self.tr.finalize()
        self.assertEqual(self.tr.selected_cds_end, self.tr.combined_cds_end)
        self.assertEqual(self.tr.selected_cds_end, 9130)
        self.assertEqual(self.tr.end_distance_from_junction, 370)
        self.assertEqual(self.tr.end_distance_from_tes, 570)
        self.tr.strip_cds()
        self.assertEqual(len(self.tr.internal_orfs), 0, self.tr.internal_orfs)
        self.tr.finalized = False
        cds = [(1161, 1200),
         (1301, 2000),
         (3501, 5000),
         (5501, 6000),
         (6201, 7000),
         (7301, 7700),
         (8201, 9000),
         (9101, 9300),
         (9501, 9690)]
        self.tr.add_exons(cds, features='CDS')
        self.tr.finalize()
        self.assertEqual(self.tr.combined_cds_end, 9690)
        self.assertEqual(self.tr.selected_cds_end, self.tr.combined_cds_end)
        self.assertEqual(self.tr.end_distance_from_junction, 10)
        self.assertEqual(self.tr.end_distance_from_tes, 210)
        self.tr.strip_cds()
        self.assertEqual(self.tr.combined_cds_end, self.tr.selected_cds_end, self.tr.combined_cds)
        self.assertEqual(self.tr.combined_cds_end, None, self.tr.combined_cds_end)
        self.tr.finalized = False
        cds = [(1161, 1200),
         (1301, 2000),
         (3501, 5000),
         (5501, 6000),
         (6201, 7000),
         (7301, 7700),
         (8201, 9000),
         (9101, 9300),
         (9501, 9700),
         (9801, 9820)]
        self.tr.add_exons(cds, features='CDS')
        self.tr.finalize()
        self.assertEqual(self.tr.combined_cds_end, 9820)
        self.assertEqual(self.tr.selected_cds_end, self.tr.combined_cds_end)
        self.assertEqual(self.tr.end_distance_from_tes, 180)
        self.assertEqual(self.tr.end_distance_from_junction, 0)

    def test_end_negative(self):
        self.tr.strand = '-'
        cds = [
         (1161, 1200),
         (1301, 2000),
         (3501, 5000),
         (5501, 6000),
         (6201, 7000),
         (7301, 7700),
         (8201, 9000),
         (9101, 9130)]
        self.assertEqual(sum(x[1] - x[0] + 1 for x in cds) % 3, 0)
        self.tr.add_exons(cds, features='CDS')
        self.tr.finalize()
        self.assertTrue(self.tr.is_coding)
        self.assertEqual(self.tr.selected_cds_end, self.tr.combined_cds_end)
        self.assertEqual(self.tr.selected_cds_end, 1161)
        self.assertEqual(self.tr.end_distance_from_junction, 460, (
         self.tr.end_distance_from_junction,
         460))
        self.assertEqual(self.tr.end_distance_from_tes, self.tr.end_distance_from_junction + 200, (
         self.tr.end_distance_from_tes,
         self.tr.end_distance_from_junction + 200))
        self.tr.strip_cds()
        self.assertEqual(len(self.tr.internal_orfs), 0, self.tr.internal_orfs)
        self.tr.finalized = False
        cds = [(721, 800),
         (1001, 1200),
         (1301, 2000),
         (3501, 5000),
         (5501, 6000),
         (6201, 7000),
         (7301, 7700),
         (8201, 9000),
         (9101, 9130)]
        self.tr.add_exons(cds, features='CDS')
        self.tr.finalize()
        self.assertEqual(self.tr.combined_cds_end, 721)
        self.assertEqual(self.tr.selected_cds_end, self.tr.combined_cds_end)
        self.assertEqual(self.tr.end_distance_from_junction, 220, (
         self.tr.end_distance_from_junction, 220))
        self.assertEqual(self.tr.end_distance_from_tes, self.tr.end_distance_from_junction + 200, (
         self.tr.end_distance_from_tes,
         self.tr.end_distance_from_junction + 200))
        self.tr.strip_cds()
        self.assertEqual(self.tr.combined_cds_end, self.tr.selected_cds_end, self.tr.combined_cds)
        self.assertEqual(self.tr.combined_cds_end, None, self.tr.combined_cds_end)
        self.tr.finalized = False
        cds = [(161, 300),
         (501, 800),
         (1001, 1200),
         (1301, 2000),
         (3501, 5000),
         (5501, 6000),
         (6201, 7000),
         (7301, 7700),
         (8201, 9000),
         (9101, 9130)]
        self.assertEqual(sum((_[1] - _[0] + 1) % 3 for _ in cds) % 3, 0)
        self.tr.logger = self.logger
        self.tr.add_exons(cds, features='CDS')
        self.tr.finalize()
        self.assertEqual(self.tr.combined_cds_end, 161)
        self.assertEqual(self.tr.selected_cds_end, self.tr.combined_cds_end)
        self.assertEqual(self.tr.end_distance_from_tes, 60)
        self.assertEqual(self.tr.end_distance_from_junction, 0)


if __name__ == '__main__':
    unittest.main()