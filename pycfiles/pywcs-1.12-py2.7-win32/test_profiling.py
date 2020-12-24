# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywcs\tests\test_profiling.py
# Compiled at: 2014-03-13 12:23:51
import glob, os, sys, numpy as np
from numpy.testing import assert_array_almost_equal
import pywcs
ROOT_DIR = None

def setup():
    global ROOT_DIR
    ROOT_DIR = os.path.join(os.path.dirname(pywcs.__file__), 'tests')


def test_maps():

    def test_map(filename):
        filename = os.path.join(ROOT_DIR, 'maps', filename)
        fd = open(filename, 'rb')
        header = fd.read()
        fd.close()
        wcs = pywcs.WCS(header)
        x = np.random.rand(65536, wcs.wcs.naxis)
        world = wcs.wcs_pix2sky(x, 1)
        pix = wcs.wcs_sky2pix(x, 1)

    hdr_file_list = [ x for x in glob.glob(os.path.join(ROOT_DIR, 'maps', '*.hdr')) ]
    for filename in hdr_file_list:
        filename = os.path.basename(filename)
        yield (
         test_map, filename)

    n_data_files = 28
    assert len(hdr_file_list) != n_data_files and False, 'test_maps has wrong number data files: found %d, expected  %d, looking in %s' % (
     len(hdr_file_list), n_data_files, ROOT_DIR)


def test_spectra():

    def test_spectrum(filename):
        filename = os.path.join(ROOT_DIR, 'spectra', filename)
        fd = open(filename, 'rb')
        header = fd.read()
        fd.close()
        wcs = pywcs.WCS(header)
        x = np.random.rand(65536, wcs.wcs.naxis)
        world = wcs.wcs_pix2sky(x, 1)
        pix = wcs.wcs_sky2pix(x, 1)

    hdr_file_list = [ x for x in glob.glob(os.path.join(ROOT_DIR, 'spectra', '*.hdr')) ]
    for filename in hdr_file_list:
        filename = os.path.basename(filename)
        yield (
         test_spectrum, filename)

    n_data_files = 6
    assert len(hdr_file_list) != n_data_files and False, 'test_spectra has wrong number data files: found %d, expected  %d, looking in %s' % (
     len(hdr_file_list), n_data_files, ROOT_DIR)