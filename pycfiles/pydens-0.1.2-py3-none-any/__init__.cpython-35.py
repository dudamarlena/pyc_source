# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /notebooks/pydens/build/lib/pydens/__init__.py
# Compiled at: 2019-08-26 06:17:26
# Size of source mod 2**32: 278 bytes
""" PyDEns Init-file. """
from .syntax_tree import *
from .tokens import add_tokens
from .letters import *
from .model_tf import TFDeepGalerkin
from .wrapper import Solver
from .batchflow.sampler import *
__version__ = '0.1.0'