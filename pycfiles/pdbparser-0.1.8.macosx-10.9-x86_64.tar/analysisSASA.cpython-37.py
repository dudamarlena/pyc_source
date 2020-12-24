# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Examples/analysisSASA.py
# Compiled at: 2019-02-16 11:13:15
# Size of source mod 2**32: 1545 bytes
from __future__ import print_function
import os, copy
from collections import Counter
import numpy as np
from pdbparser import pdbparser
from pdbparser.Utilities.Collection import get_path
from pdbparser.Utilities.Database import __ATOM__
from pdbparser.Utilities.Construct import Micelle, Sheet, Nanotube
import pdbparser.Analysis.Structure.SolventAccessibleSurfaceArea as SolventAccessibleSurfaceArea
pdbSDS = pdbparser(os.path.join(get_path('pdbparser'), 'Data/SDS.pdb'))
pdbCTAB = pdbparser(os.path.join(get_path('pdbparser'), 'Data/CTAB.pdb'))
PDB = Nanotube().construct().get_pdb()
PDB = Sheet().construct().get_pdb()
PDB = Micelle([pdbSDS], flipPdbs=[
 True, True],
  positionsGeneration='symmetric').construct().get_pdb()
SASA = SolventAccessibleSurfaceArea(trajectory=PDB, configurationsIndexes=[0], targetAtomsIndexes=(PDB.indexes),
  atomsRadius='vdwRadius',
  makeContiguous=False,
  probeRadius=0,
  resolution=0.5,
  storeSurfacePoints=True,
  tempdir=None)
SASA.run()
print('Surface Accessible Surface Area is:', SASA.results['sasa'][0], 'Ang^2.')
points = SASA.results['surface points'][0]
__ATOM__['element_symbol'] = 'cu'
__ATOM__['atom_name'] = 'cu'
surface = pdbparser()
surface.records = [copy.copy(__ATOM__) for _ in range(points.shape[0])]
surface.set_coordinates(points)
PDB.concatenate(surface)
PDB.visualize()