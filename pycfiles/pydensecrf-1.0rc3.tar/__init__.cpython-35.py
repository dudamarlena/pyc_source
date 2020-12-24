# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /notebooks/pydens/build/lib/pydens/__init__.py
# Compiled at: 2019-08-26 06:17:26
# Size of source mod 2**32: 278 bytes
__doc__ = ' PyDEns Init-file. '
from .syntax_tree import *
from .tokens import add_tokens
from .letters import *
from .model_tf import TFDeepGalerkin
from .wrapper import Solver
from .batchflow.sampler import *
__version__ = '0.1.0'