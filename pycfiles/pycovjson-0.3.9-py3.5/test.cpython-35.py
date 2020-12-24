# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pycovjson/test/test.py
# Compiled at: 2016-11-10 06:15:19
# Size of source mod 2**32: 1256 bytes
from pycovjson.model import TileSet, Coverage, Reference
import os, numpy as np, pycovjson
from pycovjson.read_netcdf import NetCDFReader

def test():
    dir_name = os.path.dirname(__file__)
    json_template = os.path.join(dir_name, '..', 'data', 'jsont_template.json')
    testfile = 'test_xy.nc'
    dataset_path = os.path.join(dir_name, 'testdata', testfile)
    dataset = np.arange(60)
    dataset.reshape(10, 6)
    urlTemplate = 'localhost:8080/'
    tile_shape = [
     2, 1]
    try:
        variable_names = NetCDFReader(testfile).get_var_names()
    except OSError:
        print('Error: ', OSError)

    assert len(variable_names) > 0


def read():
    dir_name = os.path.dirname(__file__)
    testfile = 'test_xy.nc'
    dataset_path = os.path.join(dir_name, 'testdata', testfile)
    reader = NetCDFReader(dataset_path)
    coverage = reader.read()


def test_convert():
    import pycovjson.convert
    pycovjson.convert('foam_2011-01-01.nc', 'coverage.covjson', ['SALTY'])


test()
test_convert()