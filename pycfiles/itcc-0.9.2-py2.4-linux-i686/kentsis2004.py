# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/kentsis2004.py
# Compiled at: 2008-04-20 13:19:45
from itcc.ccs2.pyramid import pyramid as _pyramid
from itcc.ccs2.config import config
from itcc.core import tools
threshold = config.get('Mezei_p24_threshold', -0.1 * 0.1)

def pyramid(a, b, c, rax, rbx, rcx):
    if a is None or b is None or c is None:
        return (None, None)
    (res1, res2) = _pyramid(a, b, c, rax, rbx, rcx)
    if res2 < threshold:
        return (None, None)
    return res1


class Kentsis2004(object):
    __module__ = __name__

    def __init__(self):
        self.dismat = None
        self.atmidx = None
        return

    def r(self, i1, i2):
        return self.dismat[self.atmidx[(i1 - 1)]][self.atmidx[(i2 - 1)]]

    def R6(self, coords, atmidx, dismat):
        """resolve a fragment of protein:
N1-C2-C3(=O)-N4-C5-C6(=O)-N7-C8-C9(=O)

known the coords of p1, p2, p8, p9, and all the bond length and
bond length and bond angles, to calculate the coords from p3 to p7
"""
        self.dismat = dismat
        self.atmidx = atmidx
        r1 = coords[0]
        r2 = coords[1]
        r8 = coords[7]
        r9 = coords[8]
        (i1, i2, i3, i4, i5, i6, i7, i8, i9) = tuple(atmidx)
        r27 = 0.0
        while r27 <= 10.0:
            print r27,
            r7s = pyramid(r2, r8, r9, r27, self.r(7, 8), self.r(7, 9))
            for r7 in r7s:
                r5s = pyramid(r2, r7, r8, self.r(2, 5), self.r(5, 7), self.r(5, 8))
                for r5 in r5s:
                    r6s = pyramid(r5, r7, r8, self.r(6, 5), self.r(6, 7), self.r(6, 8))
                    r3s = pyramid(r1, r2, r5, self.r(3, 1), self.r(3, 2), self.r(3, 5))
                    for r3 in r3s:
                        r4s = pyramid(r2, r3, r5, self.r(4, 2), self.r(4, 3), self.r(4, 5))
                        for r4 in r4s:
                            for r6 in r6s:
                                if r4 is None or r6 is None:
                                    print 0.0,
                                else:
                                    print tools.length(r4 - r6),

            print
            r27 += 0.1

        return


_inst = Kentsis2004()
R6 = _inst.R6