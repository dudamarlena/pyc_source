# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Examples/argonSimulation.py
# Compiled at: 2019-02-16 11:54:58
# Size of source mod 2**32: 1877 bytes
from __future__ import print_function
import os, tempfile, copy, numpy as np
from pdbparser import pdbparser
from pdbparser.log import Logger
from pdbparser.Utilities.Database import __ATOM__
from pdbparser.Utilities.Construct import AmorphousSystem
from pdbparser.Utilities.Collection import get_path
from pdbparser.Utilities.Simulate import Simulation
Ar1 = copy.deepcopy(__ATOM__)
Ar1['atom_name'] = 'Ar1'
Ar1['residue_name'] = 'Ar'
Ar1['element_symbol'] = 'Ar'
Ar2 = copy.deepcopy(Ar1)
Ar2['atom_name'] = 'Ar2'
Ar2['coordinates_x'] = 1
pdbAr = pdbparser()
pdbAr.records = [Ar1]
boxSize = np.array([20, 20, 20])
pdb = AmorphousSystem([pdbAr], boxSize=boxSize, interMolecularMinimumDistance=2.5, periodicBoundaries=True).construct().get_pdb()
sim = Simulation(pdb, logStatus=True, logExport=False, numberOfSteps=100,
  outputFrequency=100,
  boxVectors=boxSize,
  foldCoordinatesIntoBox=True,
  exportInitialConfiguration=True,
  outputPath=(tempfile.mktemp('.xyz')))
sim.bonds_indexes = []
sim.nBondsThreshold = [[] for ids in pdb.indexes]
sim.angles_indexes = []
sim.dihedrals_indexes = []
sim.atomsCharge *= 0
sim.exportInitialConfiguration = True
sim.outputFrequency = 1
sim.logExport = True
sim.timeStep = 0.1
Logger.info('equilibration at %s fm per step' % sim.timeStep)
sim.simulate(100)
sim.exportInitialConfiguration = False
sim.outputFrequency = 1
sim.logExport = True
sim.timeStep = 1
Logger.info('production at %s fm per step' % sim.timeStep)
sim.simulate(3000, initializeVelocities=False)
sim.visualize_trajectory(sim.outputPath)