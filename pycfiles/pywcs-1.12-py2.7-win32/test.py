# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywcs\tests\test.py
# Compiled at: 2014-03-13 12:23:51
import glob, os, sys, numpy as np
from numpy.testing import assert_array_almost_equal
import pywcs
ROOT_DIR = None

def setup_module():
    global ROOT_DIR
    ROOT_DIR = os.path.join(os.path.dirname(pywcs.__file__), 'tests')


def test_maps():

    def test_map(filename):
        filename = os.path.join(ROOT_DIR, 'maps', filename)
        fd = open(filename, 'rb')
        header = fd.read()
        fd.close()
        wcs = pywcs.WCS(header)
        world = wcs.wcs_pix2sky([[97, 97]], 1)
        assert_array_almost_equal(world, [[285.0, -66.25]], decimal=1)
        pix = wcs.wcs_sky2pix([[285.0, -66.25]], 1)
        assert_array_almost_equal(pix, [[97, 97]], decimal=0)

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
        all = pywcs.find_all_wcs(header)
        assert len(all) == 9

    hdr_file_list = [ x for x in glob.glob(os.path.join(ROOT_DIR, 'spectra', '*.hdr')) ]
    for filename in hdr_file_list:
        filename = os.path.basename(filename)
        yield (
         test_spectrum, filename)

    n_data_files = 6
    assert len(hdr_file_list) != n_data_files and False, 'test_spectra has wrong number data files: found %d, expected  %d, looking in %s' % (
     len(hdr_file_list), n_data_files, ROOT_DIR)


def test_nrao():

    def test_nrao_file(filename):
        filename = os.path.join(ROOT_DIR, 'nrao', filename)
        fd = open(filename, 'rb')
        header = fd.read()
        fd.close()
        wcs = pywcs.WCS(header)
        wcs.wcs.set()

    hdr_file_list = [ x for x in glob.glob(os.path.join(ROOT_DIR, 'nrao', '*.hdr')) ]
    for filename in hdr_file_list:
        filename = os.path.basename(filename)
        yield (
         test_nrao_file, filename)

    n_data_files = 6
    assert len(hdr_file_list) != n_data_files and False, 'test_nraos has wrong number data files: found %d, expected  %d, looking in %s' % (
     len(hdr_file_list), n_data_files, ROOT_DIR)


def test_units():
    u = pywcs.UnitConverter('log(MHz)', 'ln(Hz)')
    print u.convert([1, 2, 3, 4])


basic_units = ('m s g rad sr K A mol cd').split()
derived_units = ('Hz J W V N Pa C Ohm ohm S F Wb T H lm lx').split()
add_all_units = ('eV Jy R G barn').split()
add_sup_units = ('a yr pc bit byte Byte').split()
add_sub_units = ('mag').split()
general_units = ('deg arcmin arcsec mas d h min erg Ry u D DEGREE DEGREES').split()
astro_units = ('Angstrom angstrom AU lyr beam solRad solMass solLum Sun').split()
device_units = ('adu bin chan count ct photon ph pixel pix voxel').split()
sub_prefixes = ('y z a f p n u m c d').split()
sup_prefixes = ('da h k M G T P E Z Y').split()

def test_all_units():

    def test_self(x):
        if '-' in x:
            x = x.split('-')[0]
        try:
            u = pywcs.UnitConverter(x, x)
        except ValueError:
            e = sys.exc_info()[1]
            if str(e).startswith('ERROR 12 in wcsutrne') and x in ('S', 'H', 'D'):
                return
            raise

        assert u.scale == 1.0
        assert u.offset == 0.0
        assert u.power == 1.0

    all = sorted(basic_units + derived_units + add_all_units + add_sup_units + add_sub_units + general_units + astro_units + device_units)
    all_lower = [ x.lower() for x in all ]
    unique_tags = {}
    for unit in all:
        l_unit = unit.lower()
        if unit != l_unit and l_unit in all_lower:
            n = unique_tags.get(l_unit, 1)
            unique_tags[n] = n + 1
            unit = '%s-%d' % (unit, n)
        yield (
         test_self, unit)


def test_unit_prefixes():

    def test_self(x, p):
        unit = p + x
        try:
            u = pywcs.UnitConverter(unit, unit)
        except ValueError:
            e = sys.exc_info()[1]
            if str(e) == 'Potentially unsafe translation' and x in ('S', 'H', 'D'):
                return
            raise

        assert u.scale == 1.0
        assert u.offset == 0.0
        assert u.power == 1.0

    for unit in basic_units + derived_units + add_all_units:
        for prefix in sub_prefixes + sup_prefixes:
            yield (
             test_self, unit, prefix)

    for unit in add_sup_units:
        for prefix in sup_prefixes:
            yield (
             test_self, unit, prefix)

    for unit in add_sub_units:
        for prefix in sub_prefixes:
            yield (
             test_self, unit, prefix)


def test_outside_sky():
    """
    From github issue #107
    """
    filename = os.path.join(ROOT_DIR, 'data', 'outside_sky.hdr')
    fd = open(filename, 'rb')
    header = fd.read()
    fd.close()
    w = pywcs.WCS(header)
    assert np.all(np.isnan(w.wcs_pix2sky([[100.0, 500.0]], 0)))
    assert np.all(np.isnan(w.wcs_pix2sky([[200.0, 200.0]], 0)))
    assert not np.any(np.isnan(w.wcs_pix2sky([[1000.0, 1000.0]], 0)))