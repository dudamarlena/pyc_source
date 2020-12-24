# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/templ8/templ8/utils.py
# Compiled at: 2020-03-03 15:08:04
# Size of source mod 2**32: 425 bytes
import os
from emoji import emojize
from typing import Any

def pretty_log(msg: str) -> None:
    TOPHAT = emojize(':tophat:', use_aliases=True)
    print(f"{TOPHAT}  {msg}")


def get_child_files(root):
    paths = []
    for rel_root, dirs, files in os.walk(root):
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        paths += [os.path.join(rel_root, file) for file in files]

    return paths