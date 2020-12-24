# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arf_tools/src/classifiers/utils/kernels.py
# Compiled at: 2018-03-23 07:37:24
# Size of source mod 2**32: 515 bytes
""" ARF - TME2, Estimation de densité
Contient tous les noyaux utilisés pour une estimation de densité.

Auteurs :
* BIZZOZZERO Nicolas
* ADOUM Robert

Source :
* https://en.wikipedia.org/wiki/Kernel_(statistics)
"""
import numpy as np

def parzen_ND(v):
    if np.linalg.norm(v) < 0.5:
        return 1
    return 0


def gaussian_ND(v):
    d = len(v)
    return np.power(1 / np.sqrt(2 * np.pi), d) * np.exp(-0.5 * np.power(np.linalg.norm(v), 2))


if __name__ == '__main__':
    pass