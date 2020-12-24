# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/utils/_vaccination.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 1058 bytes
from array import array
import os
from .._network import Network
from .._infections import Infections
__all__ = [
 'allocate_vaccination',
 'how_many_vaccinated', 'vaccinate_same_id']

def allocate_vaccination(network: Network, output_dir: str):
    """Allocate memory and open files needed to track vaccination"""
    null_int = (network.nnodes + 1) * [0]
    null_float = (network.nnodes + 1) * [0.0]
    int_t = 'i'
    float_t = 'd'
    vac = array(int_t, null_int)
    wards_ra = array(int_t, null_int)
    risk_ra = array(float_t, null_float)
    sort_ra = array(int_t, null_int)
    VACF = open(os.path.join(output_dir, 'Vaccinated.dat', 'w'))
    trigger = 0
    return (
     vac, wards_ra, risk_ra, sort_ra, VACF, trigger)


def how_many_vaccinated(vac):
    raise AssertionError('how_many_vaccinated has not yet been written')


def vaccinate_same_id(network: Network, risk_ra, sort_ra, infections: Infections, vac, params):
    raise AssertionError('vaccinate_same_id has not yet been written')