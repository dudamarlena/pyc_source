# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\elastic3rd\symmetry\symmetry.py
# Compiled at: 2020-01-13 10:15:19
# Size of source mod 2**32: 11406 bytes
from itertools import combinations, product
import elastic3rd.crystal.deform as crydef
import numpy as np, math
import elastic3rd.symmetry.symdata as symdata

def gen_strain(strain_sca):
    strain_sca = float(strain_sca)
    Strain = np.array([[0, 0, 0, 0, 0, 0]])
    for i in range(1, 7):
        straini = list(combinations([0, 1, 2, 3, 4, 5], i))
        for j in range(0, len(straini)):
            straintmp = np.array([[0, 0, 0, 0, 0, 0]], dtype=float)
            strainindex = np.array((straini[j]), dtype=int)
            strainprod = list(product([strain_sca, strain_sca / 2.0], repeat=i))
            for k in range(0, len(strainprod)):
                strainprodk = np.array(strainprod[k])
                straintmp[(0, strainindex)] = strainprodk
                straintmp[0, 3:] = 2 * straintmp[0, 3:]
                Strain = np.append(Strain, straintmp, axis=0)

        else:
            Strain = np.delete(Strain, 0, 0)
            return Strain


def Num2IJK(Num, N, Ord):
    IJK = np.zeros((int(Ord)), dtype=int)
    for i in range(int(Ord), 0, -1):
        k = i - 1
        DivNum = N ** k
        IJK[int(Ord) - 1 - k] = math.ceil(float(Num) / float(DivNum))
        if IJK[(int(Ord) - 1 - k)] > N:
            raise IndexError('ERROR')
        Num = Num % DivNum
        if Num == 0:
            for j in range(int(Ord) - k, int(Ord)):
                IJK[j] = N
            else:
                return IJK

        return IJK


def gen_strain_coef(StrainOrd, StrainOrdCoef, Ord=3):
    n_strain = len(StrainOrd)
    N = int(n_strain ** Ord)
    Coef = np.ones(N)
    Cijk = np.zeros(N)
    for i in range(0, N):
        IJK = Num2IJK(i + 1, n_strain, Ord)
        coeftmp = np.zeros(int(Ord))

    for i_ord in range(0, int(Ord)):
        coeftmp[i_ord] = StrainOrd[(IJK[i_ord] - 1)]
    else:
        coeftmp = np.sort(coeftmp)
        for j in range(0, int(Ord)):
            Cijk[i] = Cijk[i] + coeftmp[j] * 10 ** (Ord - 1 - j)
            Coef[i] = Coef[i] * StrainOrdCoef[(IJK[j] - 1)]
        else:
            CoefUniq, CoefIndex = np.unique(Cijk, return_index=True)
            Coef = Coef[CoefIndex]
            CoefUniqCoef = np.zeros(len(CoefUniq))
            for i in range(0, len(CoefUniq)):
                CoefUniqCoef[i] = sum(Cijk == CoefUniq[i])
            else:
                CoefUniqCoef = CoefUniqCoef * Coef
                return (CoefUniq, CoefUniqCoef)


def gen_strainord(strain):
    StrainOrd = []
    StrainOrdCoef = []
    if crydef.is_strain_matrix(strain):
        for i in range(0, 3):
            for j in range(0, 3):
                if not strain[(i, j)] == 0:
                    StrainOrd.append(voigtmap(i + 1, j + 1))
                    StrainOrdCoef.append(float(strain[i][j]))

    else:
        raise IOError('The input strain matrix is not symmetry.')
    return (
     StrainOrd, StrainOrdCoef)


def voigtmap(i, j):
    if i * j == 1:
        voigt = 1
    else:
        if i * j == 4:
            voigt = 2
        else:
            if i * j == 9:
                voigt = 3
            else:
                if i * j == 6:
                    voigt = 4
                else:
                    if i * j == 3:
                        voigt = 5
                    else:
                        if i * j == 2:
                            voigt = 6
                        else:
                            voigt = 0
                            IOError('Both i and j should range from 1 to 3')
                            print('ERROR: Both i and j shold range from 1 to 3.')
    return voigt


def gen_cijk_coef(CrystalType, Strain, Ord):
    StrainOrd, StrainOrdCoef = gen_strainord(Strain)
    CijkInd = symdata.coef_ind(CrystalType, Ord)
    CoefCoef = symdata.coef_crystal(CrystalType, Ord)
    Cijk, CijkCoef = gen_strain_coef(StrainOrd, StrainOrdCoef, Ord)
    CijkUniq = np.array(symdata.get_unique(CijkInd))
    CoefStrain = np.zeros(len(CijkUniq))
    CijkNum = cijk2num(Cijk, Ord)
    for i in range(0, len(CijkNum)):
        COrderi = CijkInd[CijkNum[i]]
        if type(COrderi) is list:
            for j in range(0, len(COrderi)):
                CoefOrderi = float(CoefCoef[CijkNum[i]][j]) * float(CijkCoef[i])
                Index_CoefStrain = np.argwhere(CijkUniq == COrderi[j])
                Index_CoefStrain = Index_CoefStrain[0][0]
                CoefStrain[Index_CoefStrain] = CoefStrain[Index_CoefStrain] + CoefOrderi

        else:
            if COrderi != 0:
                CoefOrderi = float(CoefCoef[CijkNum[i]]) * float(CijkCoef[i])
                Index_CoefStrain = np.argwhere(CijkUniq == COrderi)
                Index_CoefStrain = Index_CoefStrain[0][0]
                CoefStrain[Index_CoefStrain] = CoefStrain[Index_CoefStrain] + CoefOrderi
            return CoefStrain


def gen_strain_mode(CrystalType, Ord):
    StrainAll = gen_strain(1)
    CijkInd = symdata.coef_ind(CrystalType, Ord)
    CoefCoef = symdata.coef_crystal(CrystalType, Ord)
    CijkUniq = np.array(symdata.get_unique(CijkInd))
    n_uniq = len(CijkUniq)
    Cijk = num2cijk(CijkUniq, Ord)
    StrainMode = np.zeros((n_uniq, 3, 3), dtype=float)
    StrainModeCoef = CoefStr(Ord)
    exec('StrainModeCoef.coef' + str(int(Ord)) + ' = np.zeros((n_uniq, n_uniq), dtype = float)')
    for i in range(2, int(Ord)):
        CijUniq = np.array(symdata.get_unique(symdata.coef_ind(CrystalType, i)))
        n_uniqi = len(CijUniq)
        exec('StrainModeCoef.coef' + str(i) + ' = np.zeros((n_uniq, n_uniqi), dtype = float)')
    else:
        count = 0
        for i in range(0, len(StrainAll)):
            Straini = crydef.vec2matrix(StrainAll[i])
            StrainModei = gen_cijk_coef(CrystalType, Straini, Ord)
            if i == 0:
                StrainMode[count, :, :] = Straini
                exec('StrainModeCoef.coef' + str(int(Ord)) + '[count, :] = StrainModei')
                for j in range(2, int(Ord)):
                    exec('StrainModeCoef.coef' + str(j) + '[count, :] = gen_cijk_coef(CrystalType, Straini, j)')
                else:
                    count = count + 1

            else:
                StrainModetmp = np.zeros((count + 1, n_uniq), dtype=float)
                StrainModetmp[0:count, :] = eval('StrainModeCoef.coef' + str(int(Ord)) + '[0:count, :]')
                StrainModetmp[count, :] = StrainModei
                SMRank = np.linalg.matrix_rank(StrainModetmp)
                if SMRank == count + 1:
                    exec('StrainModeCoef.coef' + str(int(Ord)) + '[count, :] = StrainModei')
                    StrainMode[count, :, :] = Straini

    for j in range(2, int(Ord)):
        exec('StrainModeCoef.coef' + str(j) + '[count, :] = gen_cijk_coef(CrystalType, Straini, j)')
    else:
        count = count + 1
        if count == n_uniq:
            break
        return (StrainModeCoef, StrainMode)


def gen_cijall(Ord):
    N = int(6 ** Ord)
    CijkAll = np.zeros(N, dtype=int)
    for i in range(0, N):
        IJK = Num2IJK(i + 1, 6, int(Ord))
        IJK = np.sort(IJK)
        for j in range(0, int(Ord)):
            CijkAll[i] = CijkAll[i] + IJK[j] * 10 ** (Ord - 1 - j)
        else:
            CijkAll = np.unique(CijkAll)
            return CijkAll


def cijk2num(Cijk, Ord):
    CijkAll = gen_cijall(Ord)
    CijkNum = []
    for i in Cijk:
        indexi = np.argwhere(CijkAll == i)
        CijkNum.append(indexi[0][0])
    else:
        return CijkNum


def num2cijk(num, Ord):
    CijkAll = gen_cijall(Ord)
    Cijk = CijkAll[(num - 1)]
    return Cijk


def CoefForSingleMode(CrystalType, Ord, Strain):
    m = Strain.shape
    if len(m) == 1:
        m = 1
    else:
        m = m[0]
    StrainMode = np.zeros((m, 3, 3))
    StrainModeCoef = CoefStr(Ord)
    for i in range(2, int(Ord) + 1):
        CijUniq = np.array(symdata.get_unique(symdata.coef_ind(CrystalType, i)))
        n_uniq = len(CijUniq)
        exec('StrainModeCoef.coef' + str(i) + ' = np.zeros((m, n_uniq), dtype = float)')
    else:
        Cijk = CoefStr(Ord)
        for i in range(2, int(Ord) + 1):
            exec('Cijk.coef' + str(i) + ' = print_cijk(CrystalType, i)')
            for j in range(0, m):
                StrainM = crydef.vec2matrix(Strain[j, :])
                StrainMode[j, :, :] = StrainM
                exec('StrainModeCoef.coef' + str(i) + '[j, :] = gen_cijk_coef(CrystalType, StrainM, i)')
            else:
                exec('print(StrainModeCoef.coef' + str(i) + ')')

        else:
            return (
             Cijk, StrainModeCoef, StrainMode)


def print_cijk(CrystalType, Ord):
    CijkInd = symdata.coef_ind(CrystalType, Ord)
    CijkUniq = np.array(symdata.get_unique(CijkInd))
    Cijk = num2cijk(CijkUniq, Ord)
    print(Cijk)
    return Cijk


class CoefStr:
    __doc__ = 'This is the structure for coefficients. The attaches is coef + i, \n    where i is 2 to Ord\n    Take Ord = 3 as an example, there are two attaches, coef2 and coef3'

    def __init__(self, Ord=3):
        for i in range(2, int(Ord) + 1):
            exec('self.coef' + str(i) + ' = []')