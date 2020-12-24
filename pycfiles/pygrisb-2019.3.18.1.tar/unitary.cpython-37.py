# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/symm/unitary.py
# Compiled at: 2019-02-24 00:01:05
# Size of source mod 2**32: 3957 bytes
import numpy as np
from sympy.physics.quantum.cg import CG

def jj_to_cubic_relativistic_harmonics(orbital='f'):
    if 'f' == orbital:
        jj_to_cubic = np.zeros((14, 14))
        jj_to_cubic[(0, 8)] = -np.sqrt(0.16666666666666666)
        jj_to_cubic[(4, 8)] = np.sqrt(0.8333333333333334)
        jj_to_cubic[(5, 10)] = -np.sqrt(0.16666666666666666)
        jj_to_cubic[(1, 10)] = np.sqrt(0.8333333333333334)
        jj_to_cubic[(4, 0)] = np.sqrt(0.16666666666666666)
        jj_to_cubic[(0, 0)] = np.sqrt(0.8333333333333334)
        jj_to_cubic[(1, 2)] = np.sqrt(0.16666666666666666)
        jj_to_cubic[(5, 2)] = np.sqrt(0.8333333333333334)
        jj_to_cubic[(3, 4)] = 1.0
        jj_to_cubic[(2, 6)] = 1.0
        jj_to_cubic[(13, 12)] = np.sqrt(0.4166666666666667)
        jj_to_cubic[(9, 12)] = np.sqrt(0.5833333333333334)
        jj_to_cubic[(6, 13)] = np.sqrt(0.4166666666666667)
        jj_to_cubic[(10, 13)] = np.sqrt(0.5833333333333334)
        jj_to_cubic[(12, 11)] = -np.sqrt(0.75)
        jj_to_cubic[(8, 11)] = np.sqrt(0.25)
        jj_to_cubic[(7, 9)] = np.sqrt(0.75)
        jj_to_cubic[(11, 9)] = -np.sqrt(0.25)
        jj_to_cubic[(13, 7)] = np.sqrt(0.5833333333333334)
        jj_to_cubic[(9, 7)] = -np.sqrt(0.4166666666666667)
        jj_to_cubic[(6, 5)] = -np.sqrt(0.5833333333333334)
        jj_to_cubic[(10, 5)] = np.sqrt(0.4166666666666667)
        jj_to_cubic[(12, 3)] = -np.sqrt(0.25)
        jj_to_cubic[(8, 3)] = -np.sqrt(0.75)
        jj_to_cubic[(7, 1)] = np.sqrt(0.25)
        jj_to_cubic[(11, 1)] = np.sqrt(0.75)
    else:
        raise ValueError('UndefinedFunction')
    return jj_to_cubic


def comp_sph_harm_to_real_harm(dim_m):
    csh2rh = np.zeros((dim_m, dim_m), dtype=complex)
    l = dim_m // 2
    iy = list(range(dim_m))
    for i in range(l):
        iy += [iy.pop(0)]

    for m in range(-l, l + 1):
        if m < 0:
            csh2rh[(iy[m], iy[m])] = complex(0.0, 1.0) / np.sqrt(2.0)
            csh2rh[(iy[(-m)], iy[m])] = complex(-0.0, -1.0) / np.sqrt(2.0) * (-1) ** m
        elif m == 0:
            csh2rh[(iy[m], iy[m])] = 1.0
        else:
            csh2rh[(iy[(-m)], iy[m])] = 1.0 / np.sqrt(2)
            csh2rh[(iy[m], iy[m])] = 1.0 / np.sqrt(2) * (-1) ** m

    return csh2rh


def get_u_csh2rh_all(ncorbs_list):
    u_csh2rh_list = [comp_sph_harm_to_real_harm(ncorbs) for ncorbs in ncorbs_list]
    return u_csh2rh_list


def comp_sph_harm_to_relativistic_harm(dim_ms):
    """transformation matrix from spin-complex spherical harmonics
    (orbital fast) to relativistic harmonics
    """
    csh2relh = np.zeros((dim_ms, dim_ms), dtype=complex)
    dim_m = dim_ms // 2
    l = dim_m // 2
    iy = list(range(dim_m))
    for i in range(l):
        iy += [iy.pop(0)]

    iys = {0.5:iy, 
     -0.5:[iy[i] + dim_m for i in range(dim_m)]}
    i_jm = -1
    for i in (-0.5, 0.5):
        _j = l + i
        for mj in np.arange(-_j, _j + 1):
            i_jm += 1
            for s in (-0.5, 0.5):
                csh2relh[(iys[s][int(round(mj - s))], i_jm)] = CG(l, mj - s, 0.5, s, _j, mj).doit()

    return csh2relh


def get_u_csh2relh_all(ncorbs_list):
    u_csh2relh_list = [comp_sph_harm_to_relativistic_harm(ncorbs) for ncorbs in ncorbs_list]
    return u_csh2relh_list


def get_u_csh2wan_all(ncorbs_list):
    ncorbs = ncorbs_list[0]
    if ncorbs % 2 == 0:
        u_csh2wan_list = get_u_csh2relh_all(ncorbs_list)
    else:
        u_csh2wan_list = get_u_csh2rh_all(ncorbs_list)
    return u_csh2wan_list