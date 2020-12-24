# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /run/media/etienne/DATA/Toolbox/tensorpac/tensorpac/__init__.py
# Compiled at: 2019-10-07 10:13:11
# Size of source mod 2**32: 436 bytes
"""
Tensorpac
=========

Tensorpac is an open-source Python toolbox designed for computing
Phase-Amplitude Coupling.
"""
import logging
from tensorpac import methods, signals, utils, stats
from tensorpac.pac import Pac, EventRelatedPac, PreferredPhase
from tensorpac.io import set_log_level
logger = logging.getLogger('brainets')
set_log_level('info')
__version__ = '0.6.2'