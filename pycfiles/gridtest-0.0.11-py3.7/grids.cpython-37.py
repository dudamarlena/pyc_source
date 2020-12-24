# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridtest/main/grids.py
# Compiled at: 2020-05-07 19:46:42
# Size of source mod 2**32: 1751 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from gridtest.utils import read_yaml, write_yaml, write_json
from gridtest.main.generate import import_module
from gridtest.main.substitute import expand_args
from copy import deepcopy
from gridtest.logger import bot
import itertools, re, shutil, sys, os

def get_grids(lookup, filename=''):
    """given a loaded items (a grids section from a GridRunner). return 
       the parameterized grids.
    """
    grids = {}
    for name, grid in lookup.items():
        args = expand_args(entry={'grid':grid.get('grid', {}), 
         'args':grid.get('args', {})})
        if 'count' in grid:
            args = args * grid['count']
        if 'func' in grid:
            sys.path.insert(0, os.path.dirname(filename))
            funcname = grid.get('func')
            module = '.'.join(funcname.split('.')[:-1])
            funcname = funcname.split('.')[(-1)]
            try:
                module = import_module(module)
                func = getattr(module, funcname)
                if func is None:
                    bot.exit(f"Cannot find {funcname}.")
            except:
                bot.exit(f"Cannot import grid function {funcname}")

            args = [func(**k) for k in args]
        grids[name] = args

    return grids