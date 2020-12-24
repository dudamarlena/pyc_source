# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/modeller/standardtemplates.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 283 bytes
""" Standard residue templates for biomolecular residues """
import os
from parmed.amber.offlib import AmberOFFLibrary as _parser
StandardBiomolecularResidues = _parser.parse(os.path.join(os.path.split(__file__)[0], 'data', 'standard_residues.lib'))