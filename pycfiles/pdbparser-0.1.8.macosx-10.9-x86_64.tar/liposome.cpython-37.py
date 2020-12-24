# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Examples/liposome.py
# Compiled at: 2019-02-16 11:55:07
# Size of source mod 2**32: 602 bytes
from __future__ import print_function
import os
from pdbparser.Utilities.Collection import get_path
from pdbparser import pdbparser
from pdbparser.Utilities.Construct import Liposome
from pdbparser.Utilities.Modify import reset_sequence_identifier_per_model
pdbSDS = pdbparser(os.path.join(get_path('pdbparser'), 'Data/SDS.pdb'))
pdbLIPOSOME = Liposome(pdbSDS, innerInsertionNumber=1000,
  positionsGeneration='symmetric').construct()
pdbLIPOSOME.get_pdb().visualize()