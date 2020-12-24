# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/polypy/PolyPy.py
# Compiled at: 2018-11-09 10:49:26
# Size of source mod 2**32: 1353 bytes
import os, sys, numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import math as mt, Generic as ge, Read as rd, TrajectoryAnalysis as ta, Write as wr
from scipy import stats
from scipy.constants import codata
sys.path.append('Path')
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
Atom = 'BR'
Bin = 0.1
box = 0.1
ul = 8.0
ll = 0.01
timestep = 0.25
data = rd.read_history('HISTORY_F', Atom)
volume, t = ta.system_volume(lv, timesteps, timestep)
dens = ta.Density(data)
plane = dens.one_dimensional_density_sb(ul=ul, ll=ll)
dens.one_dimensional_density(Bin=0.1)
dens.two_dimensional_density(box=0.1)
dens.two_dimensional_density(box=0.1, log=True)
ta.msd(data, timestep, conductivity=True, temperature=1500)
ta.smooth_msd(data, timestep, runs=10, conductivity=True, temperature=1500)
ta.plane_msd(data, timestep, runs=10, ul=ul, ll=ll, direction='x', conductivity=False)