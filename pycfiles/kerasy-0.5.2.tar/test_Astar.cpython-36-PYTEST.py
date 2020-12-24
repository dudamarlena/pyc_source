# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/search/test_Astar.py
# Compiled at: 2020-05-13 03:17:00
# Size of source mod 2**32: 519 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.search.Astar import OptimalTransit

def test_8puzzle():
    n_rows, n_cols = (3, 3)
    initial_str = '2,-1,6,1,3,4,7,5,8'
    last_str = '1,2,3,4,5,6,7,8,-1'
    pannel_lst = OptimalTransit(n_rows=n_rows, n_cols=n_cols, initial_str=initial_str,
      last_str=last_str,
      heuristic_method='Manhattan_distance',
      verbose=(-1),
      retval=True)