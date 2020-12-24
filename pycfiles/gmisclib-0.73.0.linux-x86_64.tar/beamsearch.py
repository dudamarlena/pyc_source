# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/beamsearch.py
# Compiled at: 2007-08-13 06:22:59


def beamsearch(cost, extra, initial, B, E):
    """A breadth-first beam search.
        B = max number of options to keep,
        E = max cost difference between best and worst threads in beam.
        initial = [ starting positions ]
        extra = arbitrary information for cost function.
        cost = fn(state, extra) -> (total_cost, [next states], output_if_goal)
        """
    o = []
    B = max(B, len(initial))
    hlist = [ (0.0, tmp) for tmp in initial ]
    while len(hlist) > 0:
        hlist.sort()
        if len(hlist) > B:
            hlist = hlist[:B]
        hlist = filter(lambda q, e0=hlist[0][0], e=E: q[0] - e0 <= e, hlist)
        nlist = []
        while len(hlist) > 0:
            c, point = hlist.pop(0)
            newcost, nextsteps, is_goal = cost(point, extra)
            if is_goal:
                o.append((newcost, is_goal))
            for t in nextsteps:
                nlist.append((newcost, t))

        hlist = nlist

    o.sort()
    return o