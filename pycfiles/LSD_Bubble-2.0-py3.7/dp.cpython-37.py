# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/LSD/paths/dp.py
# Compiled at: 2019-02-26 04:32:05
# Size of source mod 2**32: 429 bytes
from LSD.colors import RED, ORANGE

def finish_subtree(g, v):
    minval = g.property(v, 'min')
    maxval = g.property(v, 'max')
    nexts = [v]
    g.set_color(v, RED)
    while nexts:
        u = nexts.pop()
        g.property(u, 'min', minval)
        g.property(u, 'max', maxval)
        for w in g.successors(u):
            if g.get_color(w) == ORANGE:
                g.set_color(w, RED)
                nexts.append(w)