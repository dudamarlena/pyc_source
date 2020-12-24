# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/macroeco/empirical/test_empirical.py
# Compiled at: 2015-10-07 18:42:13
from __future__ import division
import os
from configparser import ConfigParser
import unittest
from numpy.testing import TestCase, assert_equal, assert_array_equal, assert_almost_equal, assert_array_almost_equal, assert_allclose, assert_, assert_raises
from pandas.util.testing import assert_frame_equal
import macroeco.empirical as emp, macroeco.empirical._empirical as _emp, numpy as np, pandas as pd, scipy.stats as stats
try:
    import shapely.geometry as geo
    shapely_missing = False
except:
    shapely_missing = True

class Patches(TestCase):

    def setUp(self):
        local_path = os.path.dirname(os.path.abspath(__file__))
        self.meta1_path = os.path.join(local_path, 'test_meta1.txt')
        self.meta2_path = os.path.join(local_path, 'test_meta2.txt')
        self.table1_path = os.path.join(local_path, 'test_table1.csv')
        self.table1 = pd.DataFrame.from_csv(self.table1_path, index_col=False)
        self.meta1 = ConfigParser()
        self.meta1.read(self.meta1_path)
        self.pat1 = emp.Patch(self.meta1_path)
        self.pat2 = emp.Patch(self.meta2_path)
        self.cols1 = 'spp_col:spp; count_col:count; x_col:x; y_col:y'
        self.cols2 = 'spp_col:spp; count_col:count; x_col:mean; y_col:y'
        self.A1 = 0.06


class TestPatch(Patches):

    def test_load_data_meta(self):
        assert_array_equal(self.pat1.table, self.table1)
        assert_equal(self.pat1.meta, self.meta1)

    def test_subset_numeric(self):
        pat1 = emp.Patch(self.meta1_path, 'x>=0.2')
        assert_array_equal(pat1.table, self.table1[(self.table1.x >= 0.2)])
        self.meta1['x']['min'] = '0.2'
        assert_equal(pat1.meta, self.meta1)

    def test_subset_categorical(self):
        pat1 = emp.Patch(self.meta1_path, "spp=='b'")
        assert_array_equal(pat1.table, self.table1[(self.table1['spp'] == 'b')])
        assert_equal(pat1.meta, self.meta1)

    def test_multiple_subset(self):
        pat1 = emp.Patch(self.meta1_path, "spp=='a' ; y < 0.2")
        assert_array_equal(pat1.table.iloc[0], self.table1.iloc[0])
        assert_equal(len(pat1.table), 1)
        self.meta1['y']['max'] = '0.1'
        assert_equal(pat1.meta, self.meta1)

    def test_subset_count(self):
        pat1 = emp.Patch(self.meta1_path, subset='count > 2')
        assert_equal(pat1.table['count'].iloc[0], 3)
        assert_equal(len(pat1.table), 1)


class TestSAD(Patches):

    def test_simple(self):
        sad = emp.sad(self.pat1, None, None)
        assert_array_equal(sad[0][1]['y'], [3, 2])
        return

    def test_simple_with_cols(self):
        sad = emp.sad(self.pat1, self.cols1, None)
        assert_array_equal(sad[0][1]['y'], [4, 4])
        return

    def test_two_way_split(self):
        sad = emp.sad(self.pat1, self.cols1, 'x:2; y:3')
        assert_equal(len(sad), 6)
        assert_equal(sad[0][1]['spp'].values, 'a')
        assert_equal(sad[0][1]['y'].values, 2)
        assert_equal(sad[1][1]['y'].values, [1, 1])
        assert_equal(sad[5][1]['spp'].values, 'b')
        assert_equal(sad[0][1]['y'].values, 2)

    def test_one_way_uneven_split(self):
        sad = emp.sad(self.pat1, self.cols1, 'y:2')
        assert_equal(len(sad), 2)
        assert_equal(sad[0][1]['spp'].values, ['a'])
        assert_equal(sad[0][1]['y'].values, [2])
        assert_equal(sad[1][1]['spp'].values, ['a', 'b'])
        assert_equal(sad[1][1]['y'].values, [2, 4])

    def test_split_categorical(self):
        sad = emp.sad(self.pat1, self.cols1, 'year:split; x:2')
        assert_equal(sad[0][1]['y'].values, 3)
        assert_equal(sad[1][1]['y'].values, [])
        assert_equal(sad[2][1]['y'].values, [1, 1])
        assert_equal(sad[3][1]['y'].values, [3])

    def test_clean(self):
        sad = emp.sad(self.pat1, self.cols1, 'x:2', clean=False)
        assert_equal(len(sad[1][1]), 2)
        sad = emp.sad(self.pat1, self.cols1, 'x:2', clean=True)
        assert_equal(len(sad[1][1]), 1)

    def test_split_panda_default_column_names(self):
        sad = emp.sad(self.pat2, self.cols2, splits='mean:2', clean=False)
        assert_equal(len(sad[1][1]), 2)
        sad = emp.sad(self.pat2, self.cols2, splits='mean:2; y:3', clean=True)
        assert_equal(len(sad[1][1]), 2)


class TestSSAD(Patches):

    def test_no_splits(self):
        ssad = emp.ssad(self.pat1, self.cols1, None)
        assert_array_equal(ssad[0][1]['y'], [4])
        assert_array_equal(ssad[1][1]['y'], [4])
        return

    def test_with_split(self):
        ssad = emp.ssad(self.pat1, self.cols1, 'x:2')
        assert_array_equal(ssad[0][1]['y'], [4, 0])
        assert_array_equal(ssad[1][1]['y'], [1, 3])


class TestSAR(Patches):

    def test_no_splits(self):
        sar = emp.sar(self.pat1, self.cols1, None, '1,1; 2,1; 2,3')
        assert_array_almost_equal(sar[0][1]['x'], [
         1 * self.A1, 0.5 * self.A1, 0.16666666666666666 * self.A1])
        assert_array_equal(sar[0][1]['y'], [2, 1.5, 0.8333333333333334])
        return

    def test_with_split(self):
        sar = emp.sar(self.pat1, self.cols1, 'year:split', '2,1; 1,3')
        assert_array_almost_equal(sar[0][1]['x'], [0.5 * self.A1, 0.3333333333333333 * self.A1])
        assert_array_almost_equal(sar[1][1]['x'], [0.5 * self.A1, 0.3333333333333333 * self.A1])
        assert_array_equal(sar[0][1]['y'], [0.5, 0.6666666666666666])
        assert_array_equal(sar[1][1]['y'], [1.5, 1])

    def test_single_division(self):
        sar = emp.sar(self.pat1, self.cols1, None, '2,1')
        assert_array_almost_equal(sar[0][1]['x'], [0.5 * self.A1])
        assert_array_equal(sar[0][1]['y'], [1.5])
        return

    def test_empty_equals_split_subset(self):
        sar_empty = emp.sar(self.pat1, self.cols1, '', '1,1')
        sar_split = emp.sar(self.pat1, self.cols1, 'x:1; y:1', '1,1')
        print sar_empty
        print sar_split
        assert_frame_equal(sar_empty[0][1].sort(axis=1), sar_split[0][1].sort(axis=1))


class TestEAR(Patches):

    def test_no_splits(self):
        sar = emp.sar(self.pat1, self.cols1, None, '1,1; 2,1; 2,3', ear=True)
        assert_array_equal(sar[0][1]['y'], [2, 0.5, 0])
        return

    def test_with_split(self):
        sar = emp.sar(self.pat1, self.cols1, 'year:split', '2,1;1,3', ear=True)
        assert_array_equal(sar[0][1]['y'], [0.5, 0])
        assert_array_equal(sar[1][1]['y'], [0.5, 0.3333333333333333])


class TestCommGrid(Patches):

    def test_no_splits_Sorensen(self):
        comm = emp.comm_grid(self.pat1, self.cols1, None, '2,1')
        assert_almost_equal(comm[0][1]['x'], [0.1])
        assert_array_equal(comm[0][1]['y'], [2.0 / 3])
        return

    def test_no_splits_Jaccard(self):
        comm = emp.comm_grid(self.pat1, self.cols1, None, '2,1', metric='Jaccard')
        assert_almost_equal(comm[0][1]['x'], [0.1])
        assert_array_equal(comm[0][1]['y'], [0.5])
        return

    def test_with_split(self):
        comm = emp.comm_grid(self.pat1, self.cols1, 'year:split', '2,1')
        assert_array_equal(comm[0][1]['y'], [0])
        assert_array_equal(comm[1][1]['y'], [0.6666666666666666])

    def test_y_division_even(self):
        comm = emp.comm_grid(self.pat1, self.cols1, '', '1,3')
        assert_array_equal(comm[0][1]['pair'], ['(0.15 0.1) - (0.15 0.2)',
         '(0.15 0.1) - (0.15 0.3)',
         '(0.15 0.2) - (0.15 0.3)'])
        assert_array_almost_equal(comm[0][1]['x'], [0.1, 0.2, 0.1])
        assert_array_equal(comm[0][1]['y'], [0.6666666666666666, 0.6666666666666666, 1.0])

    def test_x_y_division_uneven_y(self):
        comm = emp.comm_grid(self.pat1, self.cols1, '', '2,2')
        print comm
        assert_array_equal(comm[0][1]['pair'], ['(0.1 0.125) - (0.1 0.275)',
         '(0.1 0.125) - (0.2 0.125)',
         '(0.1 0.125) - (0.2 0.275)',
         '(0.1 0.275) - (0.2 0.125)',
         '(0.1 0.275) - (0.2 0.275)',
         '(0.2 0.125) - (0.2 0.275)'])
        assert_array_almost_equal(comm[0][1]['x'], [0.15, 0.1, 0.180278, 0.180278,
         0.1, 0.15], 6)
        assert_array_equal(comm[0][1]['y'], [0.6666666666666666, 0, 0, 0, 0.6666666666666666, 0])

    def test_x_y_division_uneven_y_jaccard(self):
        comm = emp.comm_grid(self.pat1, self.cols1, '', '2,2', metric='Jaccard')
        assert_array_equal(comm[0][1]['y'], [0.5, 0, 0, 0, 0.5, 0])


@unittest.skipIf(shapely_missing, 'shapely not present, skipping O-ring test')
class TestORing(Patches):

    def test_spp_no_present_returns_empty_df(self):
        o_ring = emp.o_ring(self.pat1, self.cols1, '', 'nothere', [0, 0.1, 0.2])
        assert_frame_equal(o_ring[0][1], pd.DataFrame(columns=['x', 'y']))

    def test_one_individual_returns_zeros(self):
        self.pat1.table = self.pat1.table[2:4]
        o_ring = emp.o_ring(self.pat1, self.cols1, '', 'a', [0, 0.1, 0.2])
        assert_array_equal(o_ring[0][1]['y'], [0, 0])

    def test_no_density_a(self):
        o_ring = emp.o_ring(self.pat1, self.cols1, '', 'a', [0, 0.101, 0.201, 0.301], density=False)
        assert_array_almost_equal(o_ring[0][1]['x'], [0.0505, 0.151, 0.251])
        assert_array_almost_equal(o_ring[0][1]['y'], [8, 4, 0])

    def test_no_density_b(self):
        o_ring = emp.o_ring(self.pat1, self.cols1, '', 'b', [0, 0.1, 0.2, 0.3], density=False)
        assert_array_almost_equal(o_ring[0][1]['x'], [0.05, 0.15, 0.25])
        assert_array_almost_equal(o_ring[0][1]['y'], [6, 6, 0])

    def test_with_split_a(self):
        o_ring = emp.o_ring(self.pat1, self.cols1, 'y:2', 'a', [0, 0.1, 0.2], density=False)
        assert_array_equal(o_ring[0][1]['y'], [2, 0])
        assert_array_equal(o_ring[1][1]['y'], [2, 0])

    def test_with_split_b(self):
        o_ring = emp.o_ring(self.pat1, self.cols1, 'y:2', 'b', [0, 0.1, 0.2], density=False)
        assert_array_equal(o_ring[0][1]['y'], [])
        assert_array_equal(o_ring[1][1]['y'], [6, 6])

    def test_density_a(self):
        o_ring = emp.o_ring(self.pat1, self.cols1, '', 'a', [0, 0.10000001])
        assert_array_almost_equal(o_ring[0][1]['y'], [
         8 / (1.25 * np.pi * 0.010000000000000002)], 3)

    def test_density_b(self):
        o_ring = emp.o_ring(self.pat1, self.cols1, '', 'b', [0, 0.10000001, 0.1828427])
        assert_array_almost_equal(o_ring[0][1]['y'], [
         6 / (1.25 * np.pi * 0.010000000000000002),
         6 / (0.375 * np.pi * (0.03343145294329 - 0.010000000000000002))], 3)


class TestProduct:

    def test_product_with_order(self):
        expected = [
         [
          1, 5], [1, 6], [1, 7], [2, 5], [2, 6], [2, 7]]
        assert_equal(_emp._product([1, 2], [5, 6, 7]), expected)


class TestDistance:

    def test_cartesian_distance(self):
        assert_equal(_emp._distance((0, 0), (2, 2)), np.sqrt(8))


class TestDecDegDistance:

    def test_ucberkeley_to_sf(self):
        berkeley = (37.87133, -122.259293)
        sf = (37.780213, -122.419968)
        assert_almost_equal(_emp._decdeg_distance(berkeley, sf), 17.37, 1)


class TestEmpiricalCDF:

    def test_sorted_data(self):
        test_data = [
         1, 1, 1, 1, 2, 3, 4, 5, 6, 6]
        ans = [0.4, 0.4, 0.4, 0.4, 0.5, 0.6, 0.7, 0.8, 1, 1]
        res = emp.empirical_cdf(test_data)
        assert_array_equal(ans, res['ecdf'])

    def test_unsorted_data(self):
        test_data = [
         6, 6, 1, 1, 5, 1, 1, 2, 3, 4]
        ans = [0.4, 0.4, 0.4, 0.4, 0.5, 0.6, 0.7, 0.8, 1, 1]
        res = emp.empirical_cdf(test_data)
        assert_array_equal(ans, res['ecdf'])
        assert_array_equal(np.sort(test_data), res['data'])

    def test_all_data_same(self):
        test_data = [
         3, 3, 3, 3]
        ans = [1, 1, 1, 1]
        res = emp.empirical_cdf(test_data)
        assert_array_equal(ans, res['ecdf'])