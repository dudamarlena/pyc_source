# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_cosmic_comoving_volume.py
# Compiled at: 2019-10-02 03:40:12
# Size of source mod 2**32: 4273 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, numpy as np
from astropy import units as u
from copy import copy
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import apply_cosmology
cosmo = apply_cosmology.apply_cosmology(70, 0.3, 0.7)
print('cosmo', cosmo)
if sys.version_info.major >= 3:
    long = int
else:

    def calc_cosmic_comoving_volume_1(z_edge_1, z_edge_2, obs_area_arcmin2):
        if type(obs_area_arcmin2) is u.quantity.Quantity:
            obs_area = obs_area_arcmin2
        else:
            obs_area = obs_area_arcmin2 * u.arcmin ** 2
        comoving_volume = (cosmo.comoving_volume(z_edge_2) - cosmo.comoving_volume(z_edge_1)) / (4.0 * np.pi * u.steradian) * obs_area.to(u.steradian)
        print('comoving_volume = %e [%s]' % (comoving_volume.value, comoving_volume.unit))
        return comoving_volume.value


    def calc_cosmic_comoving_volume_2(z_edge_1, z_edge_2, obs_area_arcmin2):
        if type(obs_area_arcmin2) is u.quantity.Quantity:
            obs_area = obs_area_arcmin2
        else:
            obs_area = obs_area_arcmin2 * u.arcmin ** 2
        differntial_z_list = np.linspace(z_edge_1, z_edge_2, num=10, endpoint=True)
        comoving_volume = np.sum(cosmo.differential_comoving_volume(differntial_z_list[1:]) * np.diff(differntial_z_list) * obs_area.to(u.steradian))
        print('comoving_volume = %e [%s]' % (comoving_volume.value, comoving_volume.unit))
        return comoving_volume.value


    if __name__ == '__main__':
        obs_area = 1.5546582999901375 * u.deg * u.deg
        print('obs_area = %s [%s]' % (obs_area.to(u.arcmin * u.arcmin).value, obs_area.to(u.arcmin * u.arcmin).unit))
        print('obs_area = %s [%s]' % (obs_area.to(u.steradian).value, obs_area.to(u.steradian).unit))
        z_edges = [
         0.02, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]
        for i in range(len(z_edges) - 1):
            print('z %s - %s, cosmic age %.2f - %.2f, time interval %.2f' % (
             z_edges[i],
             z_edges[(i + 1)],
             cosmo.age(z_edges[i]).to('Gyr').value,
             cosmo.age(z_edges[(i + 1)]).to('Gyr').value,
             cosmo.age(z_edges[i]).to('Gyr').value - cosmo.age(z_edges[(i + 1)]).to('Gyr').value))
            z = (z_edges[i] + z_edges[(i + 1)]) / 2.0
            calc_cosmic_comoving_volume_1(z_edges[i], z_edges[(i + 1)], obs_area)
            calc_cosmic_comoving_volume_2(z_edges[i], z_edges[(i + 1)], obs_area)