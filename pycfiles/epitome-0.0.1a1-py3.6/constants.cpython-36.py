# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/epitome/constants.py
# Compiled at: 2020-01-21 11:50:03
# Size of source mod 2**32: 1096 bytes
"""
=========
Constants
=========
.. currentmodule:: epitome.constants

.. autosummary::
  :toctree: _generate/

  Dataset
"""
from enum import Enum
import numpy as np, os

class Features(Enum):
    MASK_IDX = 0
    FEATURE_IDX = 1


class Label(Enum):
    IMPUTED_UNBOUND = -3
    IMPUTED_BOUND = -2
    UNK = -1
    UNBOUND = 0
    BOUND = 1


class Dataset(Enum):
    __doc__ = ' Enumeration determining train, valid, test or runtime.\n    '
    TRAIN = 1
    VALID = 2
    TEST = 3
    RUNTIME = 4