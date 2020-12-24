# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/duranton/Documents/CERFACS/CODES/arnica/src/arnica/__init__.py
# Compiled at: 2020-03-30 05:30:51
# Size of source mod 2**32: 433 bytes
"""
ARNICA
======

Provides a python wrapper to setup, run and post-process AVBP simulations.

Available subpackages
---------------------
utils
    A collection of tools for geometrical problems
phys
    A collection of tools for physical problems, essentially around CHT configurations
solvers_2d
    Small 2d structured FD solvers in(Dperecated)
"""
from arnica import utils
from arnica import phys
from arnica import solvers_2d