# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/utils/dicts.py
# Compiled at: 2020-02-05 08:29:04
# Size of source mod 2**32: 277 bytes
from typing import List

def override(dicts: List[dict]) -> dict:
    dicts = [{k:v for k, v in d.items() if v if v} for d in dicts]
    reduced = {}
    for d in dicts:
        reduced.update(d)

    return reduced