# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/legaul/venv36/lib/python3.6/site-packages/server/__init__.py
# Compiled at: 2020-02-09 16:33:06
# Size of source mod 2**32: 442 bytes
__all__ = ('add_new_highscore_hook', 'get_new_highscore_hooks', 'utils')
from typing import Callable, Iterable
from minegauler.shared import highscores as hs
from . import utils
_new_highscore_hooks = []

def add_new_highscore_hook(func: Callable[([hs.HighscoreStruct], None)]):
    _new_highscore_hooks.append(func)


def get_new_highscore_hooks() -> Iterable[Callable[([hs.HighscoreStruct], None)]]:
    return iter(_new_highscore_hooks)