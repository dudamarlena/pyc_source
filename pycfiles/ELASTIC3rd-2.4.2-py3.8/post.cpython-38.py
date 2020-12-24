# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\elastic3rd\post\post.py
# Compiled at: 2020-01-13 11:01:54
# Size of source mod 2**32: 6306 bytes
import numpy as np
import elastic3rd.post.esfit as esfit
import elastic3rd.symmetry.symmetry as essym
import elastic3rd.esutils as esutils
import math

def get_cij(coef_fit, coef2, coef3, flag_se):
    flag_se = flag_se.lower()
    if flag_se == 'e':
        C3 = np.linalg.solve(coef3, 6.0 * coef_fit[:, 1])
        C2 = np.linalg.lstsq(coef2, (2.0 * coef_fit[:, 0]), rcond=None)[0]
    else:
        if flag_se == 's':
            pass
    return (
     C2, C3)


def get_cijall(coef_fit, coef, Ord=3, flag_se='e'):
    C = CCOEF(Ord)
    for i in range(2, int(Ord + 1)):
        a = 0
        if flag_se == 'e':
            a = math.factorial(i)
        else:
            if flag_se == 's':
                pass
        exec('NumCoef = coef.coef' + str(i) + '.shape[0]')
        exec('RankCoef = np.linalg.matrix_rank(coef.coef' + str(i) + ')')
        if NumCoef == RankCoef:
            exec('C.C' + str(int(i)) + '= np.linalg.solve(coef.coef' + str(i) + ', a*coef_fit[:, i - 2])')
        else:
            exec('C.C' + str(int(i)) + '= np.linalg.lstsq(coef.coef' + str(i) + ', a*coef_fit[:, i - 2], rcond = None)[0]')
    else:
        return C


def get_cij_2nd(coef_2nd, coef2):
    Cij2 = np.linalg.lstsq(coef2, (2.0 * coef_2nd), rcond=None)[0]
    return Cij2


def get_coef_2nd(s, e, V0):
    eVpmol2GPa = 160.21719175
    m, n = e.shape
    coef_2nd = np.zeros((n, 1))
    for i in range(0, n):
        e0 = e[int((m - 1) / 2)][i]
        ei = e[:, i]
        ei = (ei - e0) / V0 * eVpmol2GPa
        coefi, pcovi = esfit.esfit_2nd(s, ei)
        coef_2nd[i] = coefi
    else:
        return coef_2nd


def get_coef(s, e, V0, flag_se, flag):
    flag_se = flag_se.lower()
    eVpmol2GPa = 160.21719175
    m, n = e.shape
    if flag > 3:
        coef_fit = np.zeros((n, flag - 1))
    else:
        coef_fit = np.zeros((n, 2))
    n_d = int((m - 1) / 2)
    for i in range(0, n):
        e0 = e[n_d][i]
        ei = e[:, i]
        if flag_se == 'e':
            ei = (ei - e0) / V0 * eVpmol2GPa
        else:
            if flag_se == 's':
                pass
        if flag > 2:
            coefi, pcovi = esfit.esfit(s, ei, flag_se, flag)
        else:
            s2 = s
        s2[n_d] = 1
        if flag == 1:
            e2 = ei / s2 / s2
            s2 = np.delete(s2, n_d)
            e2 = np.delete(e2, n_d)
            coefi, pcovi = esfit.esfit(s2, e2, flag_se, flag)
        else:
            if flag == 2:
                e2 = ei / s2
                s2[n_d] = 0
                coefi, pcovi = esfit.esfit(s2, e2, flag_se, flag)
        coef_fit[i, :] = coefi
    else:
        return coef_fit


def read_e(EEnergy='EEnergy.txt'):
    e = np.loadtxt(EEnergy)
    return e


def escoef(CrystalType, Ord):
    if Ord == 3:
        coef3, StrainMode, coef2 = essym.gen_strain_mode(CrystalType, Ord)
        return (coef3, coef2, StrainMode)
    if Ord == 2:
        coef2, StrainMode = essym.gen_strain_mode(CrystalType, Ord)
        return coef2


def post_mode(V0, Flag_Fig=1, Flag_Ord=3, EEnergy='EEnergy.txt', INPUT='INPUT', STRAINMODE='STRAINMODE'):
    StrainIn = esutils.read_strainmode(STRAINMODE)
    CrystalType, Ord, flag_se, StrainList = get_post_param(INPUT)
    E = read_e(EEnergy)
    C2, C3 = post_single(StrainList / 100.0, E, StrainIn, V0, Flag_Fig, Flag_Ord, INPUT)
    return (C2, C3)


def post_single(x, E, StrainIn, V0, Flag_Fig=1, Flag_Ord=3, INPUT='INPUT'):
    CrystalType, Ord, flag_se, StrainList = get_post_param(INPUT)
    if flag_se == 'e':
        Cij_mode, coef_e, StrainMode = essym.CoefForSingleMode(CrystalType, Ord, StrainIn)
    else:
        if flag_se == 's':
            pass
    coef_fit = get_coef(x, E, V0, flag_se, Flag_Ord)
    if Flag_Fig == 1:
        esfit.multiesplot(x, E, coef_fit, flag_se, Flag_Ord, V0)
    else:
        coef2 = coef_e.coef2
        coef3 = coef_e.coef3
        n = coef3.shape[1]
        SMRank = np.linalg.matrix_rank(coef3)
        if SMRank < n:
            print(SMRank)
            print(n)
            C2 = np.zeros((1, coef2.shape[1]))
            C3 = np.zeros((1, n))
        else:
            C2, C3 = get_cij(coef_fit, coef2, coef3, flag_se)
    return (
     C2, C3)


def post(V0, Flag_Fig=1, Flag_Ord=3, EEnergy='EEnergy.txt', INPUT='INPUT'):
    CrystalType, Ord, flag_se, StrainList = get_post_param(INPUT)
    E = read_e(EEnergy)
    if flag_se == 'e':
        coef_e, StrainMode = essym.gen_strain_mode(CrystalType, Ord)
    else:
        if flag_se == 's':
            pass
    coef_fit = get_coef(StrainList / 100.0, E, V0, flag_se, Flag_Ord)
    coef2 = coef_e.coef2
    coef3 = coef_e.coef3
    C2, C3 = get_cij(coef_fit, coef2, coef3, flag_se)
    if Flag_Fig == 1:
        esfit.multiesplot(StrainList / 100.0, E, coef_fit, flag_se, Flag_Ord, V0)
    return (
     C2, C3)


def get_post_param(INPUT='INPUT'):
    ParaIn = esutils.read_input(INPUT)
    flag_se = ParaIn['FlagSE'].lower()
    CrystalType = ParaIn['CrystalType']
    Ord = ParaIn['Ord']
    StrainList = esutils.gen_strain_list(ParaIn)
    return (CrystalType, Ord, flag_se, StrainList)


class CCOEF:
    __doc__ = 'This is the structure for coefficients. The attaches is coef + i, \n    where i is 2 to Ord\n    Take Ord = 3 as an example, there are two attaches, coef2 and coef3'

    def __init__(self, Ord=3):
        for i in range(2, int(Ord) + 1):
            exec('self.C' + str(i) + ' = []')