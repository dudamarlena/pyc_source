# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/waters/Pedro/ChemStruct/chemstruct/__init__.py
# Compiled at: 2019-05-27 11:57:22
# Size of source mod 2**32: 440 bytes
"""
Chemical Structure Analysis (ChemStruct)
----------------------------------------

Provides
    1. Atom and Atoms objects for atomic representation
    2. Methods for chemical analysis of atomic structures
    3. Objects for reading/writing files (e.g. xyz files)

More tools are currently under development.
For updates, see:
https://github.com/pdemingos/chemstruct

"""
import numpy as np
from .quick import *
name = 'chemstruct'