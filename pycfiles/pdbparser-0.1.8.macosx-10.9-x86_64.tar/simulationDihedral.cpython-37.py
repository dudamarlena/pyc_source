# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Examples/simulationDihedral.py
# Compiled at: 2019-02-16 11:55:26
# Size of source mod 2**32: 3402 bytes
from __future__ import print_function
import os, tempfile, copy, numpy as np
from pdbparser import pdbparser
from pdbparser.log import Logger
from pdbparser.Utilities.Database import __ATOM__
from pdbparser.Utilities.Collection import get_path
from pdbparser.Utilities.Simulate import Simulation
at1 = copy.deepcopy(__ATOM__)
at2 = copy.deepcopy(__ATOM__)
at3 = copy.deepcopy(__ATOM__)
at4 = copy.deepcopy(__ATOM__)
at5 = copy.deepcopy(__ATOM__)
at6 = copy.deepcopy(__ATOM__)
at7 = copy.deepcopy(__ATOM__)
at8 = copy.deepcopy(__ATOM__)
at1['atom_name'] = 'c1'
at2['atom_name'] = 'c2'
at3['atom_name'] = 'c3'
at4['atom_name'] = 'c4'
at5['atom_name'] = 'c5'
at6['atom_name'] = 'c6'
at7['atom_name'] = 'c7'
at8['atom_name'] = 'c8'
at1['residue_name'] = 'c'
at2['residue_name'] = 'c'
at3['residue_name'] = 'c'
at4['residue_name'] = 'c'
at5['residue_name'] = 'c'
at6['residue_name'] = 'c'
at7['residue_name'] = 'c'
at8['residue_name'] = 'c'
at1['element_symbol'] = 'c'
at2['element_symbol'] = 'c'
at3['element_symbol'] = 'c'
at4['element_symbol'] = 'c'
at5['element_symbol'] = 'c'
at6['element_symbol'] = 'c'
at7['element_symbol'] = 'c'
at8['element_symbol'] = 'c'
at1['coordinates_x'] = 0.57998
at2['coordinates_x'] = 1.69327
at3['coordinates_x'] = 2.80673
at4['coordinates_x'] = 3.92002
at5['coordinates_x'] = 5.03348
at6['coordinates_x'] = 6.14694
at7['coordinates_x'] = 7.2604
at8['coordinates_x'] = 8.37386
at1['coordinates_y'] = 0.36853
at2['coordinates_y'] = -0.36828
at3['coordinates_y'] = 0.36828
at4['coordinates_y'] = -0.36853
at5['coordinates_y'] = 0.36853
at6['coordinates_y'] = -0.36828
at7['coordinates_y'] = 0.36828
at8['coordinates_y'] = -0.36853
pdb = pdbparser()
pdb.records = [at1, at2, at3, at4]
sim = Simulation(pdb, logStatus=True, logExport=False, numberOfSteps=100,
  outputFrequency=1,
  exportInitialConfiguration=True,
  outputPath=(tempfile.mktemp('.xyz')))
sim.bonds_indexes = []
sim.angles_indexes = []
sim.lennardJones_eps *= 0
sim.atomsCharge *= 0
sim.__DIHEDRAL__['c c c c'] = {1.0: {'delta':40.0,  'n':1.0,  'kchi':3.6375696}}
sim.set_dihedrals_parameters()
Logger.info('minimizing %s steps at %s fm per step, with all terms suppressed but dihedral %s' % (sim.numberOfSteps, sim.timeStep, sim.__DIHEDRAL__['c c c c']))
sim.minimize_steepest_descent()
sim.exportInitialConfiguration = False
sim.__DIHEDRAL__['c c c c'] = {1.0: {'delta':120.0,  'n':1.0,  'kchi':3.6375696}}
sim.set_dihedrals_parameters()
Logger.info('minimizing %s steps at %s fm per step, with all terms suppressed but dihedral %s' % (sim.numberOfSteps, sim.timeStep, sim.__DIHEDRAL__['c c c c']))
sim.minimize_steepest_descent()
sim.visualize_trajectory(sim.outputPath)