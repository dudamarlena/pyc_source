# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/LSD/paths/max_c_path.py
# Compiled at: 2019-02-26 04:43:51
# Size of source mod 2**32: 2533 bytes
from LSD.cycles import cycle_distance
from LSD.colors import BLACK, RED
from LSD.paths.dp import finish_subtree
from math import inf

def caculate_cmax(g, cycle, postorder, inorder, i):
    k = len(cycle)

    def cycle_min(*args):
        min_value = inf
        min_position = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value < min_value:
                min_value = new_value
                min_position = x

        return min_position

    def cycle_max(*args):
        max_value = -1
        max_position = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value > max_value:
                max_value = new_value
                max_position = x

        return max_position

    def checkbackedge(w, u):
        return postorder.index(w) < postorder.index(u)

    for j in range(len(postorder)):
        v = postorder[j]
        inpos = inorder.index(v)
        g.property(v, 'link', inpos)
        for child in g.successors(v):
            color = g.get_color(child)
            if child in cycle:
                pos = cycle.index(child)
                g.update_property(v, 'min', cycle_min, pos)
                g.update_property(v, 'max', cycle_max, pos)
            elif color != BLACK:
                if color != RED:
                    if checkbackedge(v, child):
                        g.update_property(v, 'link', min, inorder.index(child))
            if g.property(child, 'min') is not None:
                if cycle_distance(k, i, g.property(child, 'min')) > cycle_distance(k, i, g.property(child, 'max')):
                    return (
                     True, g.property(child, 'min'))
                g.update_property(v, 'min', cycle_min, g.property(child, 'min'))
                g.update_property(v, 'max', cycle_max, g.property(child, 'max'))
                if color != RED:
                    g.update_property(v, 'link', min, g.property(child, 'link'))

        if g.property(v, 'link') == inpos:
            finish_subtree(g, v)

    return (
     False, g.property(cycle[i], 'max'))