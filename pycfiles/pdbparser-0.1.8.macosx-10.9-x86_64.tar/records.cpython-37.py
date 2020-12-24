# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Examples/records.py
# Compiled at: 2019-02-16 11:55:18
# Size of source mod 2**32: 1290 bytes
"""
In this test, an SDS molecule is loaded
several records manipulations, translation, rotation, orientation, ... are tested
"""
from __future__ import print_function
import os
from pdbparser.Utilities.Collection import get_path
from pdbparser.log import Logger
import pdbparser.pdbparser as pdbparser
from pdbparser.Utilities.Geometry import *
pdbRESULT = pdbparser()
Logger.info('loading sds molecule ...')
pdbSDS = pdbparser(os.path.join(get_path('pdbparser'), 'Data', 'SDS.pdb'))
INDEXES = range(len(pdbSDS.records))
sdsAxis = get_axis(INDEXES, pdbSDS)
atomToOriginIndex = get_closest_to_origin(INDEXES, pdbSDS)
atom = pdbSDS.records[atomToOriginIndex]
minX, minY, minZ = [atom['coordinates_x'], atom['coordinates_y'], atom['coordinates_z']]
translate(INDEXES, pdbSDS, [-1.1 * minX, -1.1 * minY, -1.1 * minZ])
Logger.info('orient molecule along [1,0,0] ...')
orient(axis=[1, 0, 0], indexes=INDEXES, pdb=pdbSDS, records_axis=sdsAxis)
sdsAxis = [1, 0, 0]
pdbRESULT.concatenate(pdbSDS)
Logger.info('Flip molecule 180 degrees ...')
pdb = pdbSDS.get_copy()
orient(axis=[-1, 1, 0], indexes=INDEXES, pdb=pdb, records_axis=sdsAxis)
pdbRESULT.concatenate(pdb)
pdbRESULT.visualize()