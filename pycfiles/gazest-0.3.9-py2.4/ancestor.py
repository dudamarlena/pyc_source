# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/ancestor.py
# Compiled at: 2007-09-26 14:45:55
import heapq

def ancestor(a, b, pfunc):
    """
    return the least common ancestor of nodes a and b or None if there
    is no such ancestor.

    pfunc must return a list of parent vertices
    """
    if a == b:
        return a
    visit = [
     a, b]
    depth = {}
    while visit:
        vertex = visit[(-1)]
        pl = pfunc(vertex)
        if not pl:
            depth[vertex] = 0
            visit.pop()
        else:
            for p in pl:
                if p == a or p == b:
                    return p
                if p not in depth:
                    visit.append(p)

            if visit[(-1)] == vertex:
                depth[vertex] = min([ depth[p] for p in pl ]) - 1
                visit.pop()

    def ancestors(vertex):
        h = [
         (
          depth[vertex], vertex)]
        seen = {}
        while h:
            (d, n) = heapq.heappop(h)
            if n not in seen:
                seen[n] = 1
                yield (d, n)
                for p in pfunc(n):
                    heapq.heappush(h, (depth[p], p))

    def generations(vertex):
        sg, s = None, {}
        for (g, v) in ancestors(vertex):
            if g != sg:
                if sg:
                    yield (
                     sg, s)
                sg, s = g, {v: 1}
            else:
                s[v] = 1

        yield (
         sg, s)
        return

    x = generations(a)
    y = generations(b)
    gx = x.next()
    gy = y.next()
    try:
        while 1:
            if gx[0] == gy[0]:
                for v in gx[1]:
                    if v in gy[1]:
                        return v

                gy = y.next()
                gx = x.next()
            elif gx[0] > gy[0]:
                gy = y.next()
            else:
                gx = x.next()

    except StopIteration:
        return

    return