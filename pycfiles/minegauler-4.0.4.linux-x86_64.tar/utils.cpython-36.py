# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/legaul/venv36/lib/python3.6/site-packages/server/utils.py
# Compiled at: 2020-02-09 16:33:06
# Size of source mod 2**32: 759 bytes
__all__ = ('is_highscore_new_best', 'multiple_contexts')
import contextlib
from typing import Optional
from minegauler.shared import highscores as hs

def is_highscore_new_best(h: hs.HighscoreStruct) -> Optional[str]:
    all_highscores = hs.get_highscores((hs.HighscoresDatabases.REMOTE), settings=h)
    return hs.is_highscore_new_best(h, all_highscores)


@contextlib.contextmanager
def multiple_contexts(*contexts):
    """
    Context manager to activate multiple context managers.

    :param contexts:
        The context managers to activate.
    """
    stack = contextlib.ExitStack()
    entered = []
    for ctx in contexts:
        entered.append(stack.enter_context(ctx))

    try:
        yield tuple(entered)
    finally:
        stack.close()