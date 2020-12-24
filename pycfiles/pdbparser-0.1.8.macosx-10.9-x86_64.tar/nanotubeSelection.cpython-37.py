# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Examples/nanotubeSelection.py
# Compiled at: 2019-02-16 11:55:14
# Size of source mod 2**32: 1910 bytes
from __future__ import print_function
import os, numpy as np
from pdbparser.log import Logger
from pdbparser import pdbparser
from pdbparser.Utilities.Collection import get_path
from pdbparser.Utilities.Selection import NanotubeSelection
from pdbparser.Utilities.Information import get_models_records_indexes_by_records_indexes, get_records_indexes_in_attribute_values
from pdbparser.Utilities.Modify import *
from pdbparser.Utilities.Geometry import get_principal_axis, translate, orient
pdbCNT = pdbparser(os.path.join(get_path('pdbparser'), 'Data/nanotubeWaterNAGMA.pdb'))
Logger.info('Define models')
define_models_by_records_attribute_value(pdbCNT.indexes, pdbCNT)
Logger.info('Getting nanotube indexes')
cntIndexes = get_records_indexes_in_attribute_values(pdbCNT.indexes, pdbCNT, 'residue_name', 'CNT')
Logger.info('Create selection')
sel = NanotubeSelection(pdbCNT, nanotubeIndexes=cntIndexes).select()
Logger.info('Get models inside nanotube')
indexes = get_models_records_indexes_by_records_indexes(sel.selections['inside_nanotube'], pdbCNT)
pdb = pdbCNT.get_copy(cntIndexes + indexes)
Logger.info('Orient to OX and translate to nanotube center')
center, _, _, _, vect1, _, _ = get_principal_axis(cntIndexes, pdbCNT)
translate(pdb.indexes, pdb, -1.0 * np.array(center))
orient(axis=[1, 0, 0], indexes=(pdb.indexes), pdb=pdb, records_axis=vect1)
Logger.info('Delete extra molecules to refine selection and reset models and records serial number')
Logger.info('Reset serial number and sequence identifier')
reset_records_serial_number(pdb)
reset_sequence_identifier_per_record(pdb)
pdb.visualize()