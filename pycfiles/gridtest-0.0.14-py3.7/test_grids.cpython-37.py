# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_grids.py
# Compiled at: 2020-05-09 20:18:22
# Size of source mod 2**32: 2635 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
import os, sys, pytest
here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)
sys.path.insert(0, os.path.join(here, 'grids'))

def test_grids():
    """Test loading and using different kinds of grids.
    """
    from gridtest.main.grids import Grid
    from gridtest.main.test import GridRunner
    from grids.script import get_pokemon_id
    grids_file = os.path.join(here, 'grids', 'grids.yml')
    runner = GridRunner(grids_file)
    grids = runner.get_grids()
    for key, grid in grids.items():
        print(list(grid))

    grid = Grid(name='generate_pids',
      params={'functions':{'pid': get_pokemon_id},  'count':10})
    assert grid.name == 'generate_pids'
    assert len(list(grid)) == 10
    entry = {'functions':{'pid': 'random.choice'}, 
     'count':10, 
     'args':{'seq': [[1, 2, 3]]}}
    grid = Grid(name='random_choice', params=entry)
    assert grid.name == 'random_choice'
    assert len(list(grid)) == 10
    assert len(grid.argsets) == 0
    entry['cache'] = True
    grid = Grid(name='random_choice', params=entry)
    assert len(grid.argsets) == 10
    grid = Grid(name='generate_empty', params={'count': 10})
    assert len(list(grid)) == 10
    params = {'args': {'x':[1, 2, 3],  'y':[1, 2, 3]}}
    grid = Grid('generate_matrix', params=params)
    assert len(list(grid)) == 9
    params = {'args': {'x':[[1, 2, 3], [4, 5, 6]],  'y':[[1, 2, 3], [4, 5, 6]]}}
    grid = Grid('generate_lists_matrix', params=params)
    assert len(list(grid)) == 4
    entry = {'args': {'x': {'min':0,  'max':10,  'by':2}}}
    grid = Grid('generate_by_min_max', params=entry)
    assert len(list(grid)) == 5
    entry = {'args': {'y':{'min':0, 
               'max':10,  'by':2}, 
              'x':{'min':10, 
               'max':20,  'by':2}}}
    grid = Grid('generate_by_min_max_twovars', params=entry)
    assert len(list(grid)) == 25