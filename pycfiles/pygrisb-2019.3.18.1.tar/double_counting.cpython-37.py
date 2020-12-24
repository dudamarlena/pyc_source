# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/mbody/double_counting.py
# Compiled at: 2019-02-22 23:25:02
# Size of source mod 2**32: 1098 bytes
import numpy

def get_vdc_hf(v2e, dm):
    """get Hartree-Fock type double counting potential,
    given the full coulomb matrix (chemist convention, including spin index)
    and the one-particle density matrix.
    The usual minus sign is included.
    """
    vdc = -numpy.einsum('ijkl,kl->ij', v2e, dm)
    vdc += numpy.einsum('ikjl,kl->ij', v2e, dm)
    return vdc


def get_vdc_fll(uavg, javg, ntot):
    """get double counting potential in the full-localization limit.
    The usual minus sign is included.
    """
    vdc = -uavg * (ntot - 0.5) + javg / 2 * (ntot - 1)
    return vdc


def get_vdc_amf(uavg, javg, ntot, l):
    """get double counting potential in the around mean-field form.
    The usual minus sign is included.
    """
    alpha = -uavg / 2.0 + (uavg + 2 * l * javg) / (2 * l + 1) / 4.0
    vdc = alpha * 2 * ntot
    return vdc


if __name__ == '__main__':
    uavg, javg, ntot, l = (6.0, 0.8, 5.2, 3)
    print(get_vdc_fll(uavg, javg, ntot))
    print(get_vdc_amf(uavg, javg, ntot, l))