# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/io/tests/test_read_esri_ascii.py
# Compiled at: 2015-03-08 15:34:29
"""
Unit tests for landlab.io.esri_ascii module.
"""
import os, numpy as np
from StringIO import StringIO
from numpy.testing import assert_array_equal, assert_array_almost_equal
from nose.tools import assert_equal, assert_true, assert_raises
try:
    from nose.tools import assert_is_instance, assert_list_equal, assert_is
except ImportError:
    from landlab.testing.tools import assert_is_instance, assert_list_equal, assert_is

from landlab.io import read_esri_ascii, read_asc_header
from landlab.io import MissingRequiredKeyError, KeyTypeError, DataSizeError, BadHeaderLineError, KeyValueError
from landlab import RasterModelGrid
_TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def test_hugo_read_file_name():
    grid, field = read_esri_ascii(os.path.join(_TEST_DATA_DIR, 'hugo_site.asc'))
    assert_is_instance(grid, RasterModelGrid)
    assert_equal(field.size, 4180)
    assert_equal(field.shape, (4180, ))


def test_hugo_read_file_like():
    with open(os.path.join(_TEST_DATA_DIR, 'hugo_site.asc')) as (asc_file):
        grid, field = read_esri_ascii(asc_file)
    assert_is_instance(grid, RasterModelGrid)
    assert_equal(field.size, 4180)
    assert_equal(field.shape, (4180, ))


def test_hugo_reshape():
    with open(os.path.join(_TEST_DATA_DIR, 'hugo_site.asc')) as (asc_file):
        grid, field = read_esri_ascii(asc_file, reshape=True)
    assert_is_instance(grid, RasterModelGrid)
    assert_true(field.shape, (55, 76))


def test_4x3_read_file_name():
    grid, field = read_esri_ascii(os.path.join(_TEST_DATA_DIR, '4_x_3.asc'))
    assert_is_instance(grid, RasterModelGrid)
    assert_is_instance(field, np.ndarray)
    assert_array_equal(field, np.array([9.0, 10.0, 11.0,
     6.0, 7.0, 8.0,
     3.0, 4.0, 5.0,
     0.0, 1.0, 2.0]))


def test_4x3_read_file_like():
    with open(os.path.join(_TEST_DATA_DIR, '4_x_3.asc')) as (asc_file):
        grid, field = read_esri_ascii(asc_file)
    assert_is_instance(grid, RasterModelGrid)
    assert_array_equal(field, np.array([9.0, 10.0, 11.0,
     6.0, 7.0, 8.0,
     3.0, 4.0, 5.0,
     0.0, 1.0, 2.0]))


def test_4x3_shape_mismatch():
    asc_file = StringIO('\nnrows         4\nncols         3\nxllcorner     1.\nyllcorner     2.\ncellsize      10.\nNODATA_value  -9999\n1. 2. 3. 4.\n5. 6. 7. 8.\n9. 10. 11. 12.\n        ')
    grid, field = read_esri_ascii(asc_file)
    assert_equal(field.size, 12)
    asc_file = StringIO('\nnrows         4\nncols         3\nxllcorner     1.\nyllcorner     2.\ncellsize      10.\nNODATA_value  -9999\n1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12.\n        ')
    grid, field = read_esri_ascii(asc_file)
    assert_equal(field.size, 12)


def test_4x3_size_mismatch():
    asc_file = StringIO('\nnrows         4\nncols         3\nxllcorner     1.\nyllcorner     2.\ncellsize      10.\nNODATA_value  -9999\n1. 2. 3. 4. 5. 6. 7. 8. 9. 10.\n        ')
    assert_raises(DataSizeError, read_esri_ascii, asc_file)


def test_header_missing_required_key():
    asc_file = StringIO('\nnrows         4\nxllcorner     1.\nyllcorner     2.\ncellsize      10.\nNODATA_value  -9999\n        ')
    assert_raises(MissingRequiredKeyError, read_asc_header, asc_file)


def test_header_unknown_key():
    asc_file = StringIO('\nnrows         4\nncols         3\nxllcorner     1.\nyllcorner     2.\ncellsize      10.\nNODATA_value  -9999\ninvalid_key   1\n        ')
    assert_raises(BadHeaderLineError, read_asc_header, asc_file)


def test_header_missing_value():
    asc_file = StringIO('\nnrows         4\nncols         3\nxllcorner     1.\nyllcorner     2.\ncellsize      \nNODATA_value  -9999\ninvalid_key   1\n        ')
    assert_raises(BadHeaderLineError, read_asc_header, asc_file)


def test_header_bad_values():
    asc_file = StringIO('\nnrows         -4\nncols         3\nxllcorner     1.\nyllcorner     2.\ncellsize      10.\nNODATA_value  -9999\n        ')
    assert_raises(KeyValueError, read_asc_header, asc_file)


def test_header_missing_mutex_key():
    asc_file = StringIO('\nncols         3\nnrows         4\nyllcorner     2.\ncellsize      10.\nNODATA_value  -9999\n        ')
    assert_raises(MissingRequiredKeyError, read_asc_header, asc_file)


def test_header_mutex_key():
    asc_file = StringIO('\nncols         3\nnrows         4\nxllcenter     1.\nyllcorner     2.\ncellsize      10.\nNODATA_value  -9999\n        ')
    header = read_asc_header(asc_file)
    assert_equal(header['xllcenter'], 1.0)
    assert_raises(KeyError, lambda k: header[k], 'xllcorner')
    asc_file = StringIO('\nncols         3\nnrows         4\nxllcorner     1.\nyllcorner     2.\ncellsize      10.\nNODATA_value  -9999\n        ')
    header = read_asc_header(asc_file)
    assert_equal(header['xllcorner'], 1.0)
    assert_raises(KeyError, lambda k: header[k], 'xllcenter')


def test_header_missing_optional():
    asc_file = StringIO('\nncols         3\nnrows         4\nxllcenter     1.\nyllcorner     2.\ncellsize      10.\n        ')
    header = read_asc_header(asc_file)
    assert_raises(KeyError, lambda k: header[k], 'nodata_value')


def test_header_case_insensitive():
    asc_file = StringIO('\nnCoLs         3\nnrows         4\nXllcenter     1.\nYLLCORNER     2.\nCELLSIZE      10.\nNODATA_value  -999\n        ')
    header = read_asc_header(asc_file)
    for key in ['ncols', 'nrows', 'xllcenter', 'yllcorner', 'cellsize',
     'nodata_value']:
        assert_true(key in header)


def test_header_wrong_type():
    asc_file = StringIO('\nnCoLs         3.5\nnrows         4\nXllcenter     1.\nYLLCORNER     2.\nCELLSIZE      10.\nNODATA_value  -999\n        ')
    assert_raises(KeyTypeError, read_asc_header, asc_file)


def test_name_keyword():
    grid, field = read_esri_ascii(os.path.join(_TEST_DATA_DIR, '4_x_3.asc'), name='air__temperature')
    assert_is_instance(grid, RasterModelGrid)
    assert_is_instance(field, np.ndarray)
    assert_array_equal(field, np.array([9.0, 10.0, 11.0,
     6.0, 7.0, 8.0,
     3.0, 4.0, 5.0,
     0.0, 1.0, 2.0]))
    assert_array_almost_equal(grid.at_node['air__temperature'], field)
    assert_is(grid.at_node['air__temperature'], field)


if __name__ == '__main__':
    unittest.main()