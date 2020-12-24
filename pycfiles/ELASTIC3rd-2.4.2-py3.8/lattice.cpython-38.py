# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\elastic3rd\crystal\lattice.py
# Compiled at: 2020-01-13 10:16:05
# Size of source mod 2**32: 2724 bytes
import math, numpy as np

def volume_crystal(a, b, c, alpha=90, beta=90, gamma=90):
    alpha = math.radians(alpha)
    beta = math.radians(beta)
    gamma = math.radians(gamma)
    a = float(a)
    b = float(b)
    c = float(c)
    V = a * b * c * math.sqrt(1 - math.cos(alpha) ** 2 - math.cos(beta) ** 2 - math.cos(gamma) ** 2 + 2.0 * math.cos(alpha) * math.cos(beta) * math.cos(gamma))
    return V


def base_vec2ABC(BaseVec):
    va = BaseVec[0, :]
    vb = BaseVec[1, :]
    vc = BaseVec[2, :]
    a = np.linalg.norm(va, ord=2)
    b = np.linalg.norm(vb, ord=2)
    c = np.linalg.norm(vc, ord=2)
    alpha = vec_ang(vb, vc)
    beta = vec_ang(va, vc)
    gamma = vec_ang(va, vb)
    ABC = np.array([a, b, c, alpha, beta, gamma])
    return ABC


def ABC2base_vec(ABC):
    a, b, c, alpha, beta, gamma = ABC
    alpha = math.radians(alpha)
    beta = math.radians(beta)
    gamma = math.radians(gamma)
    x = np.array([a, 0, 0])
    y1 = b * math.cos(gamma)
    y2 = math.sqrt(b ** 2 - y1 ** 2)
    y = np.array([y1, y2, 0])
    z1 = c * math.cos(beta)
    z2 = (b * c * math.cos(alpha) - y1 * z1) / y2
    z3 = math.sqrt(c ** 2 - z1 ** 2 - z2 ** 2)
    z = np.array([z1, z2, z3])
    BaseVec = np.array([x, y, z])
    BaseVec = BaseVec.T
    return BaseVec


def vec_ang(va, vb):
    a = np.linalg.norm(va, ord=2)
    b = np.linalg.norm(vb, ord=2)
    alpha = np.degrees(np.arccos(va.dot(vb) / (a * b)))
    return alpha


def print_base_vec(BaseVec):
    str_i = '    '
    for i in range(0, 3):
        BaseVeci = []
        for j in range(0, 3):
            BaseVeci.append('%.10f' % BaseVec[i][j])
        else:
            print('     ' + '     '.join(BaseVeci))


def print_ABC(ABC):
    print('    a         b         c      alpha   beta    gamma')
    ABC_str = []
    for i in range(0, 6):
        if i < 3:
            strparam = '%.6f'
        else:
            strparam = '%.3f'
        ABC_str.append(strparam % ABC[i])
    else:
        print('  '.join(ABC_str))


def print_lattice(BaseVec):
    print('BaseVec:')
    print_base_vec(BaseVec)
    print('Lattice Parameter:')
    ABC = base_vec2ABC(BaseVec)
    print_ABC(ABC)
    V0 = volume_crystal(ABC[0], ABC[1], ABC[2], ABC[3], ABC[4], ABC[5])
    print('Volume : ' + str(V0) + '\n')
    return V0