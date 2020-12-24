# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Examples/amorphousSystem.py
# Compiled at: 2019-02-16 12:34:06
# Size of source mod 2**32: 1011 bytes
import os
from pdbparser.Utilities.Collection import get_path
from pdbparser import pdbparser
from pdbparser.Utilities.Construct import AmorphousSystem
from pdbparser.Utilities.Database import __WATER__
pdbWATER = pdbparser()
pdbWATER.records = __WATER__
pdbWATER.set_name('water')
pdbDMPC = pdbparser(os.path.join(get_path('pdbparser'), 'Data', 'DMPC.pdb'))
pdbNAGMA = pdbparser(os.path.join(get_path('pdbparser'), 'Data', 'NAGMA.pdb'))
pdbNALMA = pdbparser(os.path.join(get_path('pdbparser'), 'Data', 'NALMA.pdb'))
pdbAMORPH = AmorphousSystem([pdbWATER, pdbDMPC, pdbNAGMA, pdbNALMA], boxSize=[
 150, 150, 150],
  density=0.25,
  restrictions='np.sqrt(x**2+y**2+z**2)<25').construct()
pdbAMORPH.get_pdb().visualize()