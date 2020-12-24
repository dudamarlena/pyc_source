# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Examples/simulationNonBonded.py
# Compiled at: 2019-02-16 11:55:30
# Size of source mod 2**32: 2802 bytes
from __future__ import print_function
import os, tempfile, copy, numpy as np
from pdbparser import pdbparser
from pdbparser.log import Logger
from pdbparser.Utilities.Database import __ATOM__
from pdbparser.Utilities.Collection import get_path
from pdbparser.Utilities.Simulate import Simulation
at1 = copy.deepcopy(__ATOM__)
at2 = copy.deepcopy(__ATOM__)
at1['atom_name'] = 'h1'
at2['atom_name'] = 'h2'
at1['residue_name'] = 'h2'
at2['residue_name'] = 'h2'
at1['element_symbol'] = 'h'
at2['element_symbol'] = 'h'
at1['coordinates_x'] = -0.125
at2['coordinates_x'] = 0.125
pdb1 = pdbparser()
pdb1.records = [at1, at2]
sim = Simulation(pdb1, logStatus=False, logExport=False, stepTime=0.2,
  numberOfSteps=10,
  outputFrequency=1,
  exportInitialConfiguration=True,
  outputPath=(tempfile.mktemp('.xyz')))
sim.bonds_indexes = []
sim.angles_indexes = []
sim.dihedrals_indexes = []
sim.nBondsThreshold = [[], []]
sim.atomsCharge = [
 0, 0]
Logger.info('minimizing %s steps at %s fm per step, with atoms charge %s, VDW forces push atoms to equilibrium distance %s' % (sim.numberOfSteps, sim.timeStep, sim.atomsCharge, 2 * sim.__LJ__['h']['rmin/2']))
sim.minimize_steepest_descent()
sim.atomsCharge = [
 0.15, 0.15]
sim.stepTime = 0.02
sim.exportInitialConfiguration = False
Logger.info('minimizing %s steps at %s fm per step, with atoms charge %s, VDW forces push atoms to equilibrium distance %s' % (sim.numberOfSteps, sim.timeStep, sim.atomsCharge, 2 * sim.__LJ__['h']['rmin/2']))
sim.minimize_steepest_descent()
sim.atomsCharge = [
 -0.15, 0.15]
Logger.info('minimizing %s steps at %s fm per step, with atoms charge %s, VDW forces push atoms to equilibrium distance %s' % (sim.numberOfSteps, sim.timeStep, sim.atomsCharge, 2 * sim.__LJ__['h']['rmin/2']))
sim.minimize_steepest_descent()
sim.atomsCharge = [
 -0.15, -0.15]
Logger.info('minimizing %s steps at %s fm per step, with atoms charge %s, VDW forces push atoms to equilibrium distance %s' % (sim.numberOfSteps, sim.timeStep, sim.atomsCharge, 2 * sim.__LJ__['h']['rmin/2']))
sim.minimize_steepest_descent()
sim.atomsCharge = [
 0.15, -0.15]
Logger.info('minimizing %s steps at %s fm per step, with atoms charge %s, VDW forces push atoms to equilibrium distance %s' % (sim.numberOfSteps, sim.timeStep, sim.atomsCharge, 2 * sim.__LJ__['h']['rmin/2']))
sim.minimize_steepest_descent()
sim.visualize_trajectory(sim.outputPath)