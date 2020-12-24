# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/calcangle.py
# Compiled at: 2008-04-20 13:19:45
from math import degrees, acos

def calc_angle(a, b, c):
    assert a > 0
    assert b > 0
    assert c > 0
    assert a <= abs(b + c)
    assert a >= abs(b - c)
    cos_A = (b * b + c * c - a * a) / (2 * b * c)
    A = degrees(acos(cos_A))
    cos_B = (a * a + c * c - b * b) / (2 * a * c)
    B = degrees(acos(cos_B))
    cos_C = (a * a + b * b - c * c) / (2 * a * b)
    C = degrees(acos(cos_C))
    print A, B, C


def main():
    import sys
    if len(sys.argv) != 4:
        import os.path
        sys.stderr.write('Usage: %s a b c\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    calc_angle(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))


if __name__ == '__main__':
    main()