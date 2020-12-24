# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/LSD/tools/sourcereach.py
# Compiled at: 2019-02-26 15:34:13
# Size of source mod 2**32: 443 bytes
from LSD.inout import load
if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    g = load(path)
    vertices = set()
    for v in g:
        if g.in_degree(v) == 0:
            stack = [
             v]
            while stack:
                n = stack.pop()
                if n not in vertices:
                    vertices.add(n)
                    stack += list(g.succ[n])

    print(len(list(vertices)))