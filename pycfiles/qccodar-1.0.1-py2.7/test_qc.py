# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/qccodar/test/test_qc.py
# Compiled at: 2017-08-23 08:27:20
"""
Tests for qc thresholds and weighted averaging.

"""
import os, numpy
numpy.set_printoptions(suppress=True)
from qccodar.qcutils import *
files = os.path.join(os.path.curdir, 'test', 'files')

def test_read_test0():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    d0 = d
    ifn2 = os.path.join(files, 'Radialmetric_test0', 'RDLv_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    assert numpy.isclose(d0, td, equal_nan=True).all(), 'should be equal, including where NaN'


def test_threshold_qc_doa_peak_power():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    d1 = threshold_qc_doa_peak_power(d, types_str, threshold=5.0)
    ifn2 = os.path.join(files, 'Radialmetric_test1', 'RDLv_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    assert numpy.isclose(d1, td, equal_nan=True).all(), 'should be equal, including where NaN'


def test_threshold_qc_doa_half_power_width():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    d2 = threshold_qc_doa_half_power_width(d, types_str, threshold=50.0)
    ifn2 = os.path.join(files, 'Radialmetric_test2', 'RDLv_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    assert numpy.isclose(d2, td, equal_nan=True).all(), 'should be equal, including where NaN'


def test_threshold_qc_monopole_snr():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    d3 = threshold_qc_monopole_snr(d, types_str, threshold=5.0)
    ifn2 = os.path.join(files, 'Radialmetric_test3', 'RDLv_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    assert numpy.isclose(d3, td, equal_nan=True).all(), 'should be equal, including where NaN'


def test_threshold_qc_loop_snr():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    d4 = threshold_qc_loop_snr(d, types_str, threshold=5.0)
    ifn2 = os.path.join(files, 'Radialmetric_test4', 'RDLv_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    assert numpy.isclose(d4, td, equal_nan=True).all(), 'should be equal, including where NaN'


def test_threshold_qc_all():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    dall = threshold_qc_all(d, types_str, thresholds=[5.0, 50.0, 5.0, 5.0])
    ifn2 = os.path.join(files, 'Radialmetric_testall', 'RDLv_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    assert numpy.isclose(dall, td, equal_nan=True).all(), 'should be equal, including where NaN'


def test_weighted_average_mp_weight_angres1():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    xd, xtypes_str = weighted_velocities(d, types_str, numdegrees=1, weight_parameter='MP')
    xc = get_columns(xtypes_str)
    ifn2 = os.path.join(files, 'RadialShorts_mp_weight_angres1', 'RDLx_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    tc = get_columns(ttypes_str)
    trngbear = td[:, [tc['SPRC'], tc['BEAR']]]
    xrngbear = xd[:, [xc['SPRC'], xc['BEAR']]]
    trows, xrows = cell_intersect(trngbear, xrngbear)
    subtd = td[(trows, tc['VELO'])]
    subxd = xd[(xrows, xc['VELO'])]
    assert numpy.isclose(subxd, subtd, equal_nan=True).all()


def _weighted_average_mp_weight_angres3():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    xd, xtypes_str = weighted_velocities(d, types_str, numdegrees=3, weight_parameter='MP')
    xc = get_columns(xtypes_str)
    ifn2 = os.path.join(files, 'RadialShorts_mp_weight_angres3', 'RDLx_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    tc = get_columns(ttypes_str)
    trngbear = td[:, [tc['SPRC'], tc['BEAR']]]
    xrngbear = xd[:, [xc['SPRC'], xc['BEAR']]]
    trows, xrows = cell_intersect(trngbear, xrngbear)
    subtd = td[(trows, tc['VELO'])]
    subxd = xd[(xrows, xc['VELO'])]
    assert numpy.isclose(subxd, subtd, rtol=1e-05, atol=0.001, equal_nan=True).all()


def test_weighted_average_snr_weight_angres1():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    xd, xtypes_str = weighted_velocities(d, types_str, numdegrees=1, weight_parameter='SNR3')
    xc = get_columns(xtypes_str)
    ifn2 = os.path.join(files, 'RadialShorts_snr_weight_angres1', 'RDLx_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    tc = get_columns(ttypes_str)
    trngbear = td[:, [tc['SPRC'], tc['BEAR']]]
    xrngbear = xd[:, [xc['SPRC'], xc['BEAR']]]
    trows, xrows = cell_intersect(trngbear, xrngbear)
    subtd = td[(trows, tc['VELO'])]
    subxd = xd[(xrows, xc['VELO'])]
    assert numpy.isclose(subxd, subtd, equal_nan=True).all()


def _weighted_average_snr_weight_angres3():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    xd, xtypes_str = weighted_velocities(d, types_str, numdegrees=3, weight_parameter='SNR3')
    xc = get_columns(xtypes_str)
    ifn2 = os.path.join(files, 'RadialShorts_snr_weight_angres3', 'RDLx_HATY_2013_11_05_0000.ruv')
    td, ttypes_str, theader, tfooter = read_lluv_file(ifn2)
    tc = get_columns(ttypes_str)
    trngbear = td[:, [tc['SPRC'], tc['BEAR']]]
    xrngbear = xd[:, [xc['SPRC'], xc['BEAR']]]
    trows, xrows = cell_intersect(trngbear, xrngbear)
    subtd = td[(trows, tc['VELO'])]
    subxd = xd[(xrows, xc['VELO'])]
    assert numpy.isclose(subxd, subtd, rtol=1e-05, atol=0.001, equal_nan=True).all()


def test_weighted_average_no_weight_angres1():
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


def _scratch():
    ofn = os.path.join(files, 'test1_output.txt')
    write_output(ofn, header, d1, footer)
    idx = numpy.where(d1 != td)
    assert numpy.isnan(d[idx]).all()
    assert numpy.isnan(d2[idx]).all()
    for i, j in numpy.array(idx).T:
        print '(%4d, %4d) %5g %5g' % (i, j, d1[(i, j)], td[(i, j)])


def _generate_output():
    ifn = os.path.join(files, 'codar_raw', 'Radialmetric_HATY_2013_11_05', 'RDLv_HATY_2013_11_05_0000.ruv')
    d, types_str, header, footer = read_lluv_file(ifn)
    d4 = threshold_qc_loop_snr(d, types_str, threshold=5.0)
    ofn = os.path.join(files, 'Radialmetric_test4', 'RDLv_HATY_2013_11_05_0000.ruv')
    write_output(ofn, header, d4, footer)