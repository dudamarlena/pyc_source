# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Coding\py\py3\experiments\easyEEG_dist\easyEEG\__init__.py
# Compiled at: 2018-05-22 20:02:08
# Size of source mod 2**32: 802 bytes
from .default import *
from . import io
from . import group
from . import structure
from . import graph
from . import statistics
from . import algorithms
import importlib

def reload(module=None):
    for _ in range(2):
        importlib.reload(io.save)
        importlib.reload(io.load)
        importlib.reload(io)
        importlib.reload(structure)
        importlib.reload(structure.group)
        importlib.reload(group)
        importlib.reload(algorithms)
        importlib.reload(algorithms.basic)
        importlib.reload(algorithms.stats_methods)
        importlib.reload(graph)
        importlib.reload(graph.figure_group)
        importlib.reload(graph.figure_unit)
        if module != None:
            importlib.reload(module)


print('EasyEEG loaded.')