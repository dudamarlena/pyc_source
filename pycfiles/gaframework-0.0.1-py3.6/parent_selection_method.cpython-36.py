# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/GaPy/parent_selection_method.py
# Compiled at: 2019-05-31 17:47:49
# Size of source mod 2**32: 1257 bytes
from enum import Enum

class ParentSelectionMethod(Enum):
    fitness_proportionate_selection = 0
    stochastic_universal_sampling = 1
    tournament_selection = 2
    random_selection = 3