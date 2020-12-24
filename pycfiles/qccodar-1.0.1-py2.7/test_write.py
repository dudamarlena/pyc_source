# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/qccodar/test/test_write.py
# Compiled at: 2017-08-23 08:27:20
"""
Tests for writing lluv files.

We may need to deal with different types of LLUV files eventually.

"""
import os, numpy
numpy.set_printoptions(suppress=True)
from qccodar.qcutils import *
files = os.path.join(os.path.curdir, 'test', 'files')

def test_write_empty_output_by_readback():
    """ 
    Write empty LLUV file output, and test by comparing to readback.

    """
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_01', 'RDLv_HATY_2013_11_01_1830.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    ofn = os.path.join(files, 'test_output.txt')
    write_output(ofn, header, d, footer)
    ifn2 = ofn
    d2, types_str2, header2, footer2 = read_lluv_file(ifn2)
    assert header == header2
    assert footer == footer2
    assert numpy.isclose(d, d2, equal_nan=True).all(), 'should be equal, including where NaN'
    assert d.size == 0, 'should be empty'
    assert d2.size == 0, 'should be emtpy'


def test_write_output_by_readback():
    """ 
    Write typical LLUV file output test by comparing to readback.

    """
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    ofn = os.path.join(files, 'test_output.txt')
    write_output(ofn, header, d, footer)
    ifn2 = ofn
    d2, types_str2, header2, footer2 = read_lluv_file(ifn2)
    assert header == header2
    assert footer == footer2
    assert numpy.isclose(d, d2, equal_nan=True).all(), 'should be equal, including where NaN'