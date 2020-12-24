# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_grids.py
# Compiled at: 2020-05-07 19:46:42
# Size of source mod 2**32: 2685 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
import os, pytest
here = os.path.abspath(os.path.dirname(__file__))

def test_grids():
    """Test loading and using different kinds of grids.
    """
    from gridtest.main.grids import get_grids
    from gridtest.main.test import GridRunner
    grids_file = os.path.join(here, 'grids', 'grids.yml')
    runner = GridRunner(grids_file)
    grids = runner.get_grids()
    entry = {'generate_pids': {'func':'script.get_pokemon_id',  'count':10}}
    result = get_grids(entry)
    assert 'generate_pids' in result
    assert len(result['generate_pids']) == 10
    entry = {'random_choice': {'func':'random.choice', 
                       'count':10, 
                       'grid':{'seq': [[1, 2, 3]]}}}
    result = get_grids(entry)
    assert 'random_choice' in result
    assert len(result['random_choice']) == 10
    result = get_grids({'generate_empty': {'count': 10}})
    assert 'generate_empty' in result
    assert len(result['generate_empty']) == 10
    entry = {'generate_matrix': {'grid': {'x':[1, 2, 3],  'y':[1, 2, 3]}}}
    result = get_grids(entry)
    assert 'generate_matrix' in result
    assert len(result['generate_matrix']) == 9
    entry = {'generate_lists_matrix': {'grid': {'x':[[1, 2, 3], [4, 5, 6]],  'y':[[1, 2, 3], [4, 5, 6]]}}}
    result = get_grids(entry)
    assert 'generate_lists_matrix' in result
    assert len(result['generate_lists_matrix']) == 4
    entry = {'generate_by_min_max': {'grid': {'x': {'min':0,  'max':10,  'by':2}}}}
    result = get_grids(entry)
    assert 'generate_by_min_max' in result
    assert len(result['generate_by_min_max']) == 5
    entry = {'generate_by_min_max_twovars': {'grid': {'y':{'min':0, 
                                               'max':10,  'by':2}, 
                                              'x':{'min':10, 
                                               'max':20,  'by':2}}}}
    result = get_grids(entry)
    assert 'generate_by_min_max_twovars' in result
    assert len(result['generate_by_min_max_twovars']) == 25