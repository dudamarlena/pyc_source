# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/codes/flexible_clustering_tree/flexible_clustering_tree/utils.py
# Compiled at: 2019-10-29 19:17:30
# Size of source mod 2**32: 268 bytes
from typing import List, Tuple
from collections import Counter
from itertools import chain

def default_fun_string_aggregation(input_lists: List[str]) -> List[Tuple[(str, int)]]:
    c_obj = Counter(input_lists)
    return c_obj.most_common(3)