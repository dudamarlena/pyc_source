# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/io/tests/test_powder_output.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 5397 bytes
"""
    This module is for test output.py saving integrated powder
    x-ray diffraction intensities into  different file formats.
    (Output into different file formats, .chi, .dat, .xye, gsas)
    Added a test to check the GSAS file reader and file writer
"""
from __future__ import absolute_import, division, print_function
import six, os, math, numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
import skxray.io.save_powder_output as output
from skxray.io.save_powder_output import gsas_writer
from skxray.io.gsas_file_reader import gsas_reader

def test_save_output():
    filename = 'function_values'
    x = np.arange(0, 100, 1)
    y = np.exp(x)
    y1 = y * math.erf(0.5)
    output.save_output(x, y, filename, q_or_2theta='Q', err=None, dir_path=None)
    output.save_output(x, y, filename, q_or_2theta='2theta', ext='.dat', err=None, dir_path=None)
    output.save_output(x, y, filename, q_or_2theta='2theta', ext='.xye', err=y1, dir_path=None)
    Data_chi = np.loadtxt('function_values.chi', skiprows=7)
    Data_dat = np.loadtxt('function_values.dat', skiprows=7)
    Data_xye = np.loadtxt('function_values.xye', skiprows=7)
    assert_array_almost_equal(x, Data_chi[:, 0])
    assert_array_almost_equal(y, Data_chi[:, 1])
    assert_array_almost_equal(x, Data_dat[:, 0])
    assert_array_almost_equal(y, Data_dat[:, 1])
    assert_array_almost_equal(x, Data_xye[:, 0])
    assert_array_almost_equal(y, Data_xye[:, 1])
    assert_array_almost_equal(y1, Data_xye[:, 2])
    os.remove('function_values.chi')
    os.remove('function_values.dat')
    os.remove('function_values.xye')


def test_gsas_output():
    filename = 'function_values'
    x = np.arange(0, 100, 5)
    y = np.arange(0, 200, 10)
    err = y * math.erf(0.2)
    vi = []
    esd_vi = []
    for ei in err:
        if ei > 0.0:
            vi.append(1.0 / ei ** 2)
            esd_vi.append(1.0 / round(ei) ** 2)
        else:
            vi.append(0.0)
            esd_vi.append(0.0)

    gsas_writer(x, y, filename + '_std', mode=None, err=None, dir_path=None)
    gsas_writer(x, y, filename + '_esd', mode='ESD', err=err, dir_path=None)
    gsas_writer(x, y, filename + '_fxye', mode='FXYE', err=err, dir_path=None)
    tth1, intensity1, err1 = gsas_reader(filename + '_std.gsas')
    tth2, intensity2, err2 = gsas_reader(filename + '_esd.gsas')
    tth3, intensity3, err3 = gsas_reader(filename + '_fxye.gsas')
    assert_array_equal(x, tth1)
    assert_array_equal(x, tth2)
    assert_array_equal(x, tth3)
    assert_array_equal(y, intensity1)
    assert_array_equal(y, intensity2)
    assert_array_equal(y, intensity3)
    assert_array_equal(esd_vi, err2)
    assert_array_almost_equal(vi, err3, decimal=12)
    os.remove(filename + '_std.gsas')
    os.remove(filename + '_esd.gsas')
    os.remove(filename + '_fxye.gsas')