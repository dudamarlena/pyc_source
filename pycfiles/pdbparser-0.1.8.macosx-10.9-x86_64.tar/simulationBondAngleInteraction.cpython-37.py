# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Examples/simulationBondAngleInteraction.py
# Compiled at: 2019-02-16 11:55:23
# Size of source mod 2**32: 2010 bytes
from __future__ import print_function
import os, tempfile, numpy as np
from pdbparser.log import Logger
from pdbparser.Utilities.Collection import get_path
from pdbparser import pdbparser
from pdbparser.Utilities.Simulate import Simulation
pdb = pdbparser(os.path.join(get_path('pdbparser'), 'Data/WATER.pdb'))
sim = Simulation(pdb, logStatus=False, logExport=False, numberOfSteps=100,
  outputFrequency=1,
  outputPath=(tempfile.mktemp('.xyz')))
Logger.info('minimizing 100 step with H-O-H angle %s and O-H bond %s' % (sim.__ANGLE__['h o h']['theta0'], sim.__BOND__['h o']['b0']))
sim.minimize_steepest_descent()
sim.__ANGLE__['h o h']['theta0'] = 120
sim.set_angles_parameters()
sim.set_bonds_parameters()
Logger.info('minimizing 100 step with H-O-H angle %s and O-H bond %s' % (sim.__ANGLE__['h o h']['theta0'], sim.__BOND__['h o']['b0']))
sim.minimize_steepest_descent()
sim.__BOND__['h o']['b0'] = 3
sim.set_angles_parameters()
sim.set_bonds_parameters()
Logger.info('minimizing 100 step with H-O-H angle %s and O-H bond %s' % (sim.__ANGLE__['h o h']['theta0'], sim.__BOND__['h o']['b0']))
sim.minimize_steepest_descent()
sim.__ANGLE__['h o h']['theta0'] = 10
sim.__BOND__['h o']['b0'] = 0.92
sim.set_angles_parameters()
sim.set_bonds_parameters()
Logger.info('minimizing 100 step with H-O-H angle %s and O-H bond %s' % (sim.__ANGLE__['h o h']['theta0'], sim.__BOND__['h o']['b0']))
sim.minimize_steepest_descent()
sim.__ANGLE__['h o h']['theta0'] = 104.52
sim.__BOND__['h o']['b0'] = 0.92
sim.set_angles_parameters()
sim.set_bonds_parameters()
Logger.info('minimizing 100 step with H-O-H angle %s and O-H bond %s' % (sim.__ANGLE__['h o h']['theta0'], sim.__BOND__['h o']['b0']))
sim.minimize_steepest_descent()
sim.visualize_trajectory(sim.outputPath)