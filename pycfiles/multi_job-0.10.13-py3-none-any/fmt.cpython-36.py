# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/utils/fmt.py
# Compiled at: 2020-01-30 08:25:52
# Size of source mod 2**32: 299 bytes
import os
from typing import Callable

def formatted_update(a: dict, b: dict, callback: Callable[([str], str)]) -> dict:
    if callback:
        return {k:(b[fmt(k)] if b[fmt(k)] else v) for k, v in a.items()}


def join_paths(a: str, b: str) -> str:
    return os.path.abspath(os.path.join(a, b))