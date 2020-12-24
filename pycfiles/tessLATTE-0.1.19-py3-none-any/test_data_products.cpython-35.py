# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Nora/Documents/research/TESS/planethunters/code/LATTE/tests/test_data_products.py
# Compiled at: 2020-02-05 04:49:10
# Size of source mod 2**32: 5037 bytes
"""
This code makes sure that everytime that the returned data is what it is expected to be. 

This test case is carried out with a pre-downloaded lighcurve file from TIC 55525572 Sector 5.

run using: python -m unittest tests/test_data_products.py

"""
import os, mock, unittest, requests, argparse
from argparse import ArgumentParser
import warnings
warnings.filterwarnings('ignore')
import sys, LATTE.LATTEutils as utils
syspath = str(os.path.abspath(utils.__file__))[0:-14]
indir = './output'
tic = '55525572'
sector = '5'
sectors = [5]
transit_list = [1454.7]
transit_sec = '5'

class TestDataImport_LC(unittest.TestCase):
    __doc__ = '\n    Test the extraction of the information from the LC file (which is already on the system)\n    '

    def test_LC_request_response(self):
        alltime, allflux, allflux_err, all_md, alltimebinned, allfluxbinned, allx1, allx2, ally1, ally2, alltime12, allfbkg, start_sec, end_sec, in_sec, tessmag, teff, srad = utils.download_data(indir, sector, tic, binfac=5, test='./tests/tic55525572_lc.fits')
        self.assertEqual(float(alltime[100]), float(1438.1174094083246), 'LC data is not what it should be.')
        self.assertEqual(float(allflux[100]), float(1.0003796815872192))
        self.assertEqual(float(allflux_err[100]), float(0.0011117355898022652))
        self.assertEqual(float(all_md[0]), float(1441.0243360822994))
        self.assertEqual(float(alltimebinned[100]), float(1438.6757392292352))
        self.assertEqual(float(allfluxbinned[100]), float(0.9995232224464417))
        self.assertEqual(float(allx1[100]), float(-0.010814569022272735))
        self.assertEqual(float(allx2[100]), float(-0.011804798617959023))
        self.assertEqual(float(ally1[100]), float(-0.024266568269581512))
        self.assertEqual(float(ally2[100]), float(-0.02981671877205372))
        self.assertEqual(float(alltime12[100]), float(1438.1312982026025))


class TestDataImport_TP(unittest.TestCase):
    __doc__ = '\n    Test the extraction of the information from the TP file (which is already on the system)\n    '

    def test_LC_request_response(self):
        X1_list, X4_list, oot_list, intr_list, bkg_list, apmask_list, arrshape_list, t_list, T0_list, tpf_filt_list = utils.download_tpf_mast(indir, transit_sec, transit_list, tic, test='./tests/tic55525572_tp.fits')
        self.assertEqual(float(X1_list[0][0][0]), float(23.402481079101562), 'TP data is not what it should be.')
        self.assertEqual(float(oot_list[0][0]), float(0.0))
        self.assertEqual(float(intr_list[0][0]), float(0.0))
        self.assertEqual(float(bkg_list[0][0][0]), float(29.239688873291016))
        self.assertEqual(float(apmask_list[0][0][0]), float(0.0))
        self.assertEqual(float(arrshape_list[0][0]), float(18944.0))
        self.assertEqual(float(t_list[0][0]), float(1437.9924102871835))
        self.assertEqual(float(T0_list[0]), float(1454.7))


class TestDataImport_TP_lighkurve(unittest.TestCase):
    __doc__ = '\n    Test the extraction of the information from the TP file (which is already on the system)\n    '

    def test_LC_request_response(self):
        TESS_unbinned_t_l, TESS_binned_t_l, small_binned_t_l, TESS_unbinned_l, TESS_binned_l, small_binned_l, tpf_list = utils.download_tpf_lightkurve(indir, transit_list, sectors, tic, test='./tests/tic55525572_tp.fits')
        print(float(TESS_unbinned_t_l[0]))
        print(float(TESS_binned_t_l[0]))
        print(float(small_binned_t_l[0]))
        print(float(TESS_unbinned_l[0]))
        print(float(TESS_binned_l[0]))
        print(float(small_binned_l[0]))
        self.assertEqual(float(TESS_unbinned_t_l[0]), float(1437.9924102871835), 'TP lighkurve data is not what it should be.')
        self.assertEqual(float(TESS_binned_t_l[0]), float(1437.9972713631325))
        self.assertEqual(float(small_binned_t_l[0]), float(1437.9972713631325))
        self.assertEqual(float(TESS_unbinned_l[0]), float(0.9975904130977179))
        self.assertEqual(float(TESS_binned_l[0]), float(0.9986087992155438))
        self.assertEqual(float(small_binned_l[0]), float(0.9971978343909532))


if __name__ == '__main__':
    unittest.main()