# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Examples/waterSphere.py
# Compiled at: 2019-02-16 12:33:04
# Size of source mod 2**32: 1529 bytes
"""
In this test two water amorphous box are constructed
one with a hollow sphere inside, the other only a shere of water is kept
"""
from __future__ import print_function
import os
from pdbparser.Utilities.Collection import get_path
from pdbparser import pdbparser
from pdbparser.log import Logger
from pdbparser.Utilities.Construct import AmorphousSystem, Micelle
from pdbparser.Utilities.Geometry import get_satisfactory_records_indexes, translate
from pdbparser.Utilities.Modify import delete_records_and_models_records
from pdbparser.Utilities.Database import __WATER__
pdbWATER = pdbparser()
pdbWATER.records = __WATER__
pdbWATER.set_name('water')
Logger.info('Create water box')
pdbWATER = AmorphousSystem(pdbWATER, density=0.5).construct().get_pdb()
pdbWATERhollow = pdbWATER.get_copy()
Logger.info('Create a water sphere of 15A radius')
sphereIndexes = get_satisfactory_records_indexes(pdbWATER.indexes, pdbWATER, 'np.sqrt(x**2 + y**2 + z**2) >= 15')
delete_records_and_models_records(sphereIndexes, pdbWATER)
Logger.info('Remove a water sphere of 15A radius')
hollowIndexes = get_satisfactory_records_indexes(pdbWATERhollow.indexes, pdbWATERhollow, 'np.sqrt(x**2 + y**2 + z**2) <= 15')
delete_records_and_models_records(hollowIndexes, pdbWATERhollow)
translate((pdbWATERhollow.indexes), pdbWATERhollow, vector=[60, 0, 0])
pdbWATER.concatenate(pdbWATERhollow)
pdbWATER.visualize()