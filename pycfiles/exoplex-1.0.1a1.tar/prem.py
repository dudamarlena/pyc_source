# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/run/PREM/prem.py
# Compiled at: 2018-03-29 19:08:52
import os, sys, numpy as np, matplotlib.pyplot as plt, pdb
prem_dat = 'PREM.csv'
REarth = 6371
verbose = True

def prem():
    cwd = os.path.dirname(__file__)
    dat = np.genfromtxt(cwd + '/PREM.csv', delimiter=',', usecols=(0, 1, 2, 3, 4, 5,
                                                                   6))
    rad = dat[:, 0]
    depth = dat[:, 1]
    rho_depth = dat[:, 2]
    rho_rad = rho_depth[::-1]
    prem_data = {'radius': rad, 'depth': depth, 'rho_depth': rho_depth, 'rho_radius': rho_rad, 'VPV': dat[:, 3], 
       'VPH': dat[:, 4], 'VSV': dat[:, 5], 'VSH': dat[:, 6]}
    return prem_data