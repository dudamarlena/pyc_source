# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Examples/micelle.py
# Compiled at: 2019-02-16 11:55:11
# Size of source mod 2**32: 761 bytes
from __future__ import print_function
import os
from pdbparser.Utilities.Collection import get_path
from pdbparser import pdbparser
from pdbparser.Utilities.Construct import Micelle
pdbSDS = pdbparser(os.path.join(get_path('pdbparser'), 'Data/SDS.pdb'))
pdbCTAB = pdbparser(os.path.join(get_path('pdbparser'), 'Data/CTAB.pdb'))
pdbMICELLE = Micelle([pdbCTAB, pdbSDS], flipPdbs=[
 True, True],
  positionsGeneration='symmetric').construct().solvate(density=0.25, restrictions='np.sqrt(x**2+y**2+z**2)<25')
pdbMICELLE.get_pdb().visualize()