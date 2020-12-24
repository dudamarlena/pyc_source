# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\lib\path.py
# Compiled at: 2010-05-01 15:45:14
from container import Container

def drill(obj, root='', levels=-1):
    if levels == 0:
        yield (
         root, obj)
        return
    levels -= 1
    if isinstance(obj, Container):
        for (k, v) in obj:
            r = '%s.%s' % (root, k)
            if levels:
                for (r2, v2) in drill(v, r, levels):
                    yield (
                     r2, v2)

            else:
                yield (
                 r, v)

    elif isinstance(obj, list):
        for (i, item) in enumerate(obj):
            r = '%s[%d]' % (root, i)
            if levels:
                for (r2, v2) in drill(item, r, levels):
                    yield (
                     r2, v2)

            else:
                yield (
                 r, item)

    else:
        yield (
         root, obj)


if __name__ == '__main__':
    from construct import *
    c = Struct('foo', Byte('a'), Struct('b', Byte('c'), UBInt16('d')), Byte('e'), Array(4, Struct('f', Byte('x'), Byte('y'))), Byte('g'))
    o = c.parse('acddexyxyxyxyg')
    for lvl in range(4):
        for (path, value) in drill(o, levels=lvl):
            print path, value

        print '---'

    output = ' \n     Container:\n        a = 97\n        b = Container:\n            c = 99\n            d = 25700\n        e = 101\n        f = [\n            Container:\n                x = 120\n                y = 121\n            Container:\n                x = 120\n                y = 121\n            Container:\n                x = 120\n                y = 121\n            Container:\n                x = 120\n                y = 121\n        ]\n        g = 103\n    ---\n    .a 97\n    .b Container:\n        c = 99\n        d = 25700\n    .e 101\n    .f [\n        Container:\n            x = 120\n            y = 121\n        Container:\n            x = 120\n            y = 121\n        Container:\n            x = 120\n            y = 121\n        Container:\n            x = 120\n            y = 121\n    ]\n    .g 103\n    ---\n    .a 97\n    .b.c 99\n    .b.d 25700\n    .e 101\n    .f[0] Container:\n        x = 120\n        y = 121\n    .f[1] Container:\n        x = 120\n        y = 121\n    .f[2] Container:\n        x = 120\n        y = 121\n    .f[3] Container:\n        x = 120\n        y = 121\n    .g 103\n    ---\n    .a 97\n    .b.c 99\n    .b.d 25700\n    .e 101\n    .f[0].x 120\n    .f[0].y 121\n    .f[1].x 120\n    .f[1].y 121\n    .f[2].x 120\n    .f[2].y 121\n    .f[3].x 120\n    .f[3].y 121\n    .g 103\n    ---\n    '