# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/qccodar/test/test_radialshorts.py
# Compiled at: 2017-08-23 08:27:20
"""
Test functions for generating radialshort data output.

"""
import os, numpy
numpy.set_printoptions(suppress=True)
from qccodar.qcutils import *
files = os.path.join(os.path.curdir, 'test', 'files')

def test_generate_radialshort_array():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    xd, xtypes_str = weighted_velocities(d, types_str, 1, 'NONE')
    rsd, rsdtypes_str = generate_radialshort_array(xd, xtypes_str, header)
    rsc = get_columns(rsdtypes_str)
    ifn2 = os.path.join(files, 'RadialShorts_no_weight_angres1', 'RDLx_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    tc = get_columns(ttypes_str)
    trngbear = td[:, [tc['SPRC'], tc['BEAR']]]
    rsrngbear = rsd[:, [rsc['SPRC'], rsc['BEAR']]]
    trows, rsrows = cell_intersect(trngbear, rsrngbear)
    subtd = td[trows, :]
    subrsd = rsd[rsrows, :]
    tcol = numpy.array([tc['BEAR'], tc['SPRC']])
    rscol = numpy.array([rsc['BEAR'], rsc['SPRC']])
    assert numpy.isclose(subrsd[:, rscol], subtd[:, tcol], rtol=1e-05, atol=0.001, equal_nan=True).all(), 'something wrong with BEAR or SPRC, not close to CODAR '
    tcol = numpy.array([tc['RNGE']])
    rscol = numpy.array([rsc['RNGE']])
    assert numpy.isclose(subrsd[:, rscol], subtd[:, tcol], rtol=1e-05, atol=0.001, equal_nan=True).all(), 'something wrong with RNGE, not close to CODAR '
    tcol = numpy.array([tc['LOND'], tc['LATD']])
    rscol = numpy.array([rsc['LOND'], rsc['LATD']])
    assert numpy.isclose(subrsd[:, rscol], subtd[:, tcol], rtol=1e-05, atol=0.001, equal_nan=True).all(), 'something wrong with LATD or LOND, not close to CODAR '
    tcol = numpy.array([tc['VELO']])
    rscol = numpy.array([rsc['VELO']])
    assert numpy.isclose(subrsd[:, rscol], subtd[:, tcol], rtol=1e-05, atol=0.001, equal_nan=True).all(), 'something wrong with VELOs'
    tcol = numpy.array([tc['XDST'], tc['YDST']])
    rscol = numpy.array([rsc['XDST'], rsc['YDST']])
    assert numpy.isclose(subrsd[:, rscol], subtd[:, tcol], rtol=1e-05, atol=0.001, equal_nan=True).all(), 'something wrong with XDST, YDST'
    assert numpy.isclose(subrsd[:, rsc['VELU']], subtd[:, tc['VELU']], rtol=0.1, atol=0.1, equal_nan=True).all(), 'something wrong with VELU, is not close to CODAR VELU'


def test_generate_radialshort_header():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    xd, xtypes_str = weighted_velocities(d, types_str, 1, 'NONE')
    rsd, rsdtypes_str = generate_radialshort_array(xd, xtypes_str, header)
    rsdheader = generate_radialshort_header(rsd, rsdtypes_str, header)
    assert rsdheader.split('\n')[0] == '%CTF: 1.00'
    assert re.search('%TableColumnTypes:.*\\n', rsdheader).group() == '%TableColumnTypes: LOND LATD VELU VELV VFLG ESPC MAXV MINV EDVC ERSC XDST YDST RNGE BEAR VELO HEAD SPRC\n'
    assert re.search('%TableType:.*\\n', rsdheader).group() == '%TableType: LLUV RDL7\n'
    assert re.search('%TableStart:.*\\n', rsdheader).group() == '%TableStart:\n'
    assert int(re.search('%TableRows:\\s(\\d*?)\\n', rsdheader).groups()[0]) == rsd.shape[0]
    assert int(re.search('%TableColumns:\\s(\\d*?)\\n', rsdheader).groups()[0]) == rsd.shape[1]


def test_generate_radialshort_empty_array_when_no_radial_data():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_01', 'RDLv_HATY_2013_11_01_1830.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    assert d.size == 0
    rsd, rsdtypes_str = generate_radialshort_array(d, types_str, header)
    assert rsd.size == 0
    assert rsdtypes_str == 'LOND LATD VELU VELV VFLG ESPC MAXV MINV EDVC ERSC XDST YDST RNGE BEAR VELO HEAD SPRC'


def test_generate_radialshort_header_for_empty_array_when_no_radial_data():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_01', 'RDLv_HATY_2013_11_01_1830.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    rsd, rsdtypes_str = generate_radialshort_array(d, types_str, header)
    rsdheader = generate_radialshort_header(rsd, rsdtypes_str, header)
    rsc = get_columns(rsdtypes_str)
    assert rsdheader.split('\n')[0] == '%CTF: 1.00'
    assert re.search('%TableColumnTypes:.*\\n', rsdheader).group() == '%TableColumnTypes: LOND LATD VELU VELV VFLG ESPC MAXV MINV EDVC ERSC XDST YDST RNGE BEAR VELO HEAD SPRC\n'
    assert re.search('%TableType:.*\\n', rsdheader).group() == '%TableType: LLUV RDL7\n'
    assert re.search('%TableStart:.*\\n', rsdheader).group() == '%TableStart:\n'
    assert int(re.search('%TableRows:\\s(\\d*?)\\n', rsdheader).groups()[0]) == 0
    assert int(re.search('%TableColumns:\\s(\\d*?)\\n', rsdheader).groups()[0]) == len(rsc)


def _scratch():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    xd, xtypes_str = weighted_velocities(d, types_str, numdegrees=1, weight_parameter='NONE')
    xc = get_columns(xtypes_str)
    ifn2 = os.path.join(files, 'RadialShorts_no_weight_angres1', 'RDLx_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    tc = get_columns(ttypes_str)
    trngbear = td[:, [tc['SPRC'], tc['BEAR']]]
    xrngbear = xd[:, [xc['SPRC'], xc['BEAR']]]
    trows, xrows = cell_intersect(trngbear, xrngbear)
    subtd = td[(trows, tc['VELO'])]
    subxd = xd[(xrows, xc['VELO'])]
    assert numpy.isclose(subxd, subtd, rtol=1e-05, atol=0.001, equal_nan=True).all()