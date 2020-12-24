# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_metal_Z.py
# Compiled at: 2019-07-18 22:30:15
# Size of source mod 2**32: 22140 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, numpy as np
from astropy.table import Table, Column, hstack
from copy import copy
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import apply_cosmology
cosmo = apply_cosmology.cosmo
if sys.version_info.major >= 3:
    long = int
else:

    def calc_metalZ_from_FMR_following_Kewley2008_PP04_O3N2(M_star):
        x = np.log10(M_star)
        a = 32.1488
        b = -8.51258
        c = 0.976384
        d = -0.0359763
        metalZ_PP04 = a + b * x + c * x ** 2 + d * x ** 3
        return metalZ_PP04


    def calc_metalZ_from_FMR_following_Kewley2008_PP04_N2(M_star):
        x = np.log10(M_star)
        a = 23.9049
        b = -5.62784
        c = 0.645142
        d = -0.0235065
        metalZ_PP04 = a + b * x + c * x ** 2 + d * x ** 3
        return metalZ_PP04


    def calc_metalZ_from_FMR_following_Kewley2008_KK04(M_star):
        x = np.log10(M_star)
        a = 27.7911
        b = -6.94493
        c = 0.808097
        d = -0.0301508
        metalZ_KK04 = a + b * x + c * x ** 2 + d * x ** 3
        return metalZ_KK04


    def calc_metalZ_from_FMR_following_Kewley2008_KD02(M_star):
        x = np.log10(M_star)
        a = 28.0974
        b = -7.23631
        c = 0.850344
        d = -0.0318315
        metalZ_KD02 = a + b * x + c * x ** 2 + d * x ** 3
        return metalZ_KD02


    def calc_metalZ_from_FMR_following_Mannucci2010(M_star, SFR):
        m = np.log10(M_star) - 10
        s = np.log10(SFR)
        metalZ_M08 = 8.9 + 0.37 * m - 0.14 * s - 0.19 * m ** 2 + 0.12 * m * s - 0.054 * s ** 2
        return metalZ_M08


    def calc_metalZ_from_FMR_following_Mannucci2010_Eq2(M_star, SFR):
        m = np.log10(M_star) - 10
        s = np.log10(SFR)
        metalZ_M08 = 8.9 + 0.37 * m - 0.14 * s - 0.19 * m ** 2 + 0.12 * m * s - 0.054 * s ** 2
        return metalZ_M08


    def calc_metalZ_from_FMR_following_Mannucci2010_Eq4(M_star, SFR):
        x = np.log10(M_star) - 0.32 * np.log10(SFR) - 10
        metalZ_M08 = 8.9 + 0.39 * x - 0.2 * x ** 2 - 0.077 * x ** 3 + 0.064 * x ** 4
        return metalZ_M08


    def calc_metalZ_from_FMR_following_Mannucci2011(M_star, SFR):
        m = np.log10(M_star) - 10
        s = np.log10(SFR)
        mu032 = np.log10(M_star) - 0.32 * np.log10(SFR)
        x = np.log10(M_star) - 0.32 * np.log10(SFR) - 10
        if np.isscalar(mu032):
            if mu032 >= 9.5:
                metalZ_M08 = 8.9 + 0.37 * m - 0.14 * s - 0.19 * m ** 2 + 0.12 * m * s - 0.054 * s ** 2
            else:
                metalZ_M08 = 8.93 + 0.51 * (mu032 - 10)
        else:
            if np.isscalar(s):
                if ~np.isscalar(m):
                    s = m * 0.0 + s
            if np.isscalar(m):
                if ~np.isscalar(s):
                    m = s * 0.0 + m
            mask = mu032 >= 9.5
            metalZ_M08 = 8.9 + 0.37 * m - 0.14 * s - 0.19 * m ** 2 + 0.12 * m * s - 0.054 * s ** 2
            metalZ_M08[~mask] = 8.93 + 0.51 * (mu032[(~mask)] - 10)
        return metalZ_M08


    def calc_metalZ_from_FMR_following_Maiolino2008(M_star, z):
        m = np.log10(M_star)
        spl_z = np.array([0.07, 0.7, 2.2, 3.5])
        spl_m0 = np.array([11.18, 11.57, 12.38, 12.76])
        spl_K0 = np.array([9.04, 9.04, 8.99, 8.79])
        m0 = np.interp(z, spl_z, spl_m0)
        K0 = np.interp(z, spl_z, spl_K0)
        metalZ_M08 = -0.0864 * (m - m0) ** 2 + K0
        print('calc_metalZ_from_FMR_following_Maiolino2008: logM0 = %s, K0 = %s' % (m0, K0))
        return metalZ_M08


    def calc_metalZ_from_FMR_following_Magnelli2012(M_star, z):
        m = np.log10(M_star)
        if z < 1.5:
            a = -4.45
        else:
            a = -4.51
        metalZ_D02 = 2.18 * m - 0.0896 * m ** 2 + a
        return metalZ_D02


    def calc_metalZ_from_FMR_following_Genzel2015_Eq12a_with_dzliu_limit(M_star, z):
        a = 8.74
        b = 10.4 + 4.46 * np.log10(1 + z) - 1.78 * np.log10(1 + z) ** 2
        diff = np.log10(M_star) - b
        if np.isscalar(diff):
            if diff < 0.0:
                diff = 0.0
        else:
            diff[diff < 0.0] = 0.0
        metalZ_PP04 = a - 0.087 * diff ** 2
        return metalZ_PP04


    def calc_metalZ_from_FMR_following_Genzel2015_Eq12a(M_star, z):
        a = 8.74
        b = 10.4 + 4.46 * np.log10(1 + z) - 1.78 * np.log10(1 + z) ** 2
        metalZ_PP04 = a - 0.087 * (np.log10(M_star) - b) ** 2
        return metalZ_PP04


    def calc_metalZ_from_FMR_following_Genzel2015a(M_star, SFR, z):
        a = 8.74
        b = 10.4 + 4.46 * np.log10(1 + z) - 1.78 * np.log10(1 + z) ** 2
        metalZ_PP04 = a - 0.087 * (np.log10(M_star) - b) ** 2
        return metalZ_PP04


    def calc_metalZ_from_FMR_following_Genzel2015_Eq12b(M_star, SFR):
        dZM08 = calc_metalZ_from_FMR_following_Mannucci2010_Eq4(M_star, SFR) - 8.69
        metalZ = 8.9 + (-0.4408 + 0.7044 * dZM08 - 0.1602 * dZM08 ** 2 - 0.4105 * dZM08 ** 3 - 0.1898 * dZM08 ** 4)
        return metalZ


    def calc_metalZ_from_FMR_following_Genzel2015b(M_star, SFR):
        dZM08 = calc_metalZ_from_FMR_following_Mannucci2010_Eq4(M_star, SFR) - 8.69
        metalZ = 8.9 + (-0.4408 + 0.7044 * dZM08 - 0.1602 * dZM08 ** 2 - 0.4105 * dZM08 ** 3 - 0.1898 * dZM08 ** 4)
        return metalZ


    def calc_metalZ_from_FMR_following_Genzel2015ab_combined_by_dzliu(M_star, SFR, z):
        if np.isscalar(M_star):
            input_M_star = np.array([M_star])
        else:
            input_M_star = np.array(M_star)
        if np.isscalar(SFR):
            input_SFR = np.array([SFR])
        else:
            input_SFR = np.array(SFR)
        if np.isscalar(z):
            input_z = np.array([z])
        else:
            input_z = np.array(z)
        if len(input_SFR) == 1:
            if len(input_M_star) > 1:
                input_SFR = np.array([input_SFR[0]] * len(input_M_star))
        if len(input_z) == 1:
            if len(input_M_star) > 1:
                input_z = np.array([input_z[0]] * len(input_M_star))
        mask = input_M_star >= 10000000000.0
        output_metalZ = input_M_star * 0.0
        output_metalZ[mask] = calc_metalZ_from_FMR_following_Genzel2015b(input_M_star[mask], input_SFR[mask])
        output_metalZ[~mask] = calc_metalZ_from_FMR_following_Genzel2015a(input_M_star[(~mask)], input_SFR[(~mask)], input_z[(~mask)])
        renorm_metalZ = calc_metalZ_from_FMR_following_Genzel2015b(10000000000.0, input_SFR[(~mask)]) - calc_metalZ_from_FMR_following_Genzel2015a(10000000000.0, input_SFR[(~mask)], input_z[(~mask)])
        output_metalZ[~mask] = output_metalZ[(~mask)] + renorm_metalZ
        return output_metalZ


    def calc_metalZ_from_FMR_following_Guo2016(M_star, SFR):
        m = np.log10(M_star)
        metalZ_M08 = 5.83 + 0.3 * m
        return metalZ_M08


    def convert_metalZ_M08_to_metalZ_PP04(metalZ_M08):
        x = metalZ_M08 - 8.69
        return 8.9 + 0.57 * (-0.7732 + 1.2357 * x - 0.2811 * x ** 2 - 0.7201 * x ** 3 - 0.333 * x ** 4)


    def convert_metalZ_M08_to_metalZ_PP04_N2_polynomial(metalZ_M08):
        x = metalZ_M08 - 8.69
        N2 = -0.7732 + 1.2357 * x - 0.2811 * x ** 2 - 0.7201 * x ** 3 - 0.333 * x ** 4
        metalZ_PP04 = 9.37 + 2.03 * N2 + 1.26 * N2 ** 2 + 0.32 * N2 ** 3
        return metalZ_PP04


    def convert_metalZ_D02_to_metalZ_PP04(metalZ_D02):
        a = -444.7831
        b = 165.426
        c = -20.202
        d = 0.8249386
        x = metalZ_D02
        return a + b * x + c * x ** 2 + d * x ** 3


    def convert_metalZ_KK04_to_metalZ_PP04(metalZ_KK04):
        a = 916.7484
        b = -309.5448
        c = 35.05168
        d = -1.3188
        x = metalZ_KK04
        return a + b * x + c * x ** 2 + d * x ** 3


    def convert_metalZ_KK04_to_metalZ_PP04_O3N2(metalZ_KK04):
        a = 631.2766
        b = -210.0209
        c = 23.48305
        d = -0.8704286
        x = metalZ_KK04
        return a + b * x + c * x ** 2 + d * x ** 3


    def convert_metalZ_KD02_to_metalZ_PP04(metalZ_KD02):
        a = 569.4927
        b = -192.5182
        c = 21.91836
        d = -0.827884
        x = metalZ_KD02
        return a + b * x + c * x ** 2 + d * x ** 3


    def convert_metalZ_KD02_to_metalZ_PP04_O3N2(metalZ_KD02):
        a = 664.8453
        b = -225.7533
        c = 25.76888
        d = -0.9761368
        x = metalZ_KD02
        return a + b * x + c * x ** 2 + d * x ** 3


    def convert_metalZ_PP04_N2_to_metalZ_PP04_O3N2(metalZ_PP04_N2):
        a = -8.0069
        b = 2.74353
        c = -0.09368
        d = 0.0
        x = metalZ_PP04_N2
        return a + b * x + c * x ** 2 + d * x ** 3


    def convert_metalZ_PP04_N2_linear_to_metalZ_PP04_N2_polynomial(metalZ_PP04_N2_linear):
        N2 = (metalZ_PP04_N2_linear - 8.9) / 0.57
        metalZ_PP04_N2_polynomial = 9.37 + 2.03 * N2 + 1.26 * N2 ** 2 + 0.32 * N2 ** 3
        return metalZ_PP04_N2_polynomial


    def calc_metalZ_from_FMR_with_dzliu_selection(M_star, SFR, z):
        input_M_star = np.log10(M_star)
        if np.isscalar(M_star):
            input_M_star = np.array([M_star])
        else:
            input_M_star = np.array(M_star)
        if np.isscalar(SFR):
            input_SFR = np.array([SFR])
        else:
            input_SFR = np.array(SFR)
        if np.isscalar(z):
            input_z = np.array([z])
        else:
            input_z = np.array(z)
        if len(input_z) == 1:
            if len(input_M_star) > 1:
                input_z = np.array([input_z[0]] * len(input_M_star))
        if len(input_SFR) == 1:
            if len(input_M_star) > 1:
                input_SFR = np.array([input_SFR[0]] * len(input_M_star))
        metalZ_G15a = calc_metalZ_from_FMR_following_Genzel2015_Eq12a(input_M_star, input_z)
        metalZ_M10Eq4 = convert_metalZ_M08_to_metalZ_PP04_N2_polynomial(calc_metalZ_from_FMR_following_Mannucci2010_Eq4(input_M_star, input_SFR))
        mask1 = metalZ_G15a < metalZ_M10Eq4
        metalZ_out = metalZ_M10Eq4
        metalZ_out[mask1] = metalZ_G15a[mask1]
        ref_M_star = 10 ** (10.4 + 4.46 * np.log10(1 + input_z) - 1.78 * np.log10(1 + input_z) ** 2)
        ref_metalZ_G15a = calc_metalZ_from_FMR_following_Genzel2015_Eq12a(ref_M_star, input_z)
        ref_metalZ_M10Eq4 = convert_metalZ_M08_to_metalZ_PP04_N2_polynomial(calc_metalZ_from_FMR_following_Mannucci2010_Eq4(ref_M_star, input_SFR))
        mask1 = np.logical_and(metalZ_G15a < metalZ_M10Eq4, input_M_star < ref_M_star)
        metalZ_out = metalZ_M10Eq4
        metalZ_out[mask1] = metalZ_G15a[mask1]
        mask3 = input_M_star >= ref_M_star
        metalZ_out[mask3] = ref_metalZ_G15a[mask3]
        return metalZ_out