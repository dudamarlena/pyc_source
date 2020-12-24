# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/convex_hull2d.py
# Compiled at: 2008-06-20 17:21:05
"""convexhull.py

Calculate the convex hull of a set of n 2D-points in O(n log n) time.  
Taken from Berg et al., Computational Geometry, Springer-Verlag, 1997.
Prints output as EPS file.

When run from the command line it generates a random set of points
inside a square of given length and finds the convex hull for those,
printing the result as an EPS file.

Usage: convexhull.py <numPoints> <squareLength> <outFile>

Dinu C. Gherman

Small Bug: Only works with a list of UNIQUE points, Evan Jones, 2005/05/18
If the list of points passed to this function is not unique, it will raise an assertion.
To fix this, remove these lines from the beginning of the convexHull function:

Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66527
and modified to work with complex numbers.

"""
import sys, random

class DuplicatePoints(ValueError):

    def __init__(self, s):
        ValueError.__init__(self, s)


def _myDet(p, q, r):
    """Calc. determinant of a special matrix with three 2D points.

    The sign, "-" or "+", determines the side, right or left,
    respectivly, on which the point r lies, when measured against
    a directed vector from p to q.
    """
    sum = q.real * (r.imag - p.imag) + p.real * (q.imag - r.imag) + r.real * (p.imag - q.imag)
    return sum


def _isRightTurn((p, q, r)):
    """Do the vectors pq:qr form a right turn, or not?"""
    if p == q or p == r or q == r:
        if p == q:
            dup = p
        elif p == r:
            dup = p
        elif q == r:
            dup = q
        raise DuplicatePoints, 'Two points are identical at %s' % str(dup)
    return _myDet(p, q, r) < 0


def _isPointInPolygon(r, P):
    """Is point r inside a given polygon P?"""
    for i in xrange(len(P[:-1])):
        p, q = P[i], P[(i + 1)]
        if not _isRightTurn((p, q, r)):
            return False

    return True


def _makeRandomData(numPoints=30, sqrLength=100, addCornerPoints=0):
    """Generate a list of random points within a square."""
    mn, mx = 0, sqrLength
    P = []
    for i in xrange(numPoints):
        rand = random.randint
        y = rand(mn + 1, mx - 1)
        x = rand(mn + 1, mx - 1)
        P.append(complex(x, y))

    if addCornerPoints != 0:
        P = P + [complex(min, min), complex(max, max), complex(min, max), complex(max, min)]
    return P


epsHeader = '%%!PS-Adobe-2.0 EPSF-2.0\n%%%%BoundingBox: %d %d %d %d\n\n/r 2 def                %% radius\n\n/circle                 %% circle, x, y, r --> -\n{\n    0 360 arc           %% draw circle\n} def\n\n/cross                  %% cross, x, y --> -\n{\n    0 360 arc           %% draw cross hair\n} def\n\n1 setlinewidth          %% thin line\nnewpath                 %% open page\n0 setgray               %% black color\n\n'

def saveAsEps(P, H, boxSize, path):
    """Save some points and their convex hull into an EPS file."""
    f = open(path, 'w')
    f.write(epsHeader % (0, 0, boxSize, boxSize))
    format = '%3d %3d'
    if H:
        f.write('%s moveto\n' % format % (H[0].real, H[0].imag))
        for p in H:
            f.write('%s lineto\n' % format % (p.real, p.imag))

        f.write('%s lineto\n' % format % (H[0].real, H[0].imag))
        f.write('stroke\n\n')
    for p in P:
        f.write('%s r circle\n' % format % (p.real, p.imag))
        f.write('stroke\n')

    f.write('\nshowpage\n')


def convexHull(P):
    """Calculate the convex hull of a set of complex points.
    If the hull has a duplicate point, an exception will be raised.
    It is up to the application not to provide duplicates.
    """
    points = list(set(P))
    points.sort(lambda a, b: 2 * cmp(a.real, b.real) + cmp(a.imag, b.imag))
    upper = [
     points[0], points[1]]
    for p in points[2:]:
        upper.append(p)
        while len(upper) > 2 and not _isRightTurn(upper[-3:]):
            del upper[-2]

    while len(upper) > 2 and not _isRightTurn(upper[-2:] + upper[:1]):
        del upper[-1]

    points.reverse()
    lower = [
     points[0], points[1]]
    for p in points[2:]:
        lower.append(p)
        while len(lower) > 2 and not _isRightTurn(lower[-3:]):
            del lower[-2]

    while len(lower) > 2 and not _isRightTurn(lower[-2:] + lower[:1]):
        del lower[-1]

    us = set(upper)
    for q in lower:
        if q not in us:
            upper.append(q)

    return tuple(upper)


def test():
    a = 200
    p = _makeRandomData(300, a, 0)
    c = convexHull(p)
    saveAsEps(p, c, a, 'foo.eps')


if __name__ == '__main__':
    try:
        numPoints = int(sys.argv[1])
        squareLength = int(sys.argv[2])
        path = sys.argv[3]
    except IndexError:
        numPoints = 30
        squareLength = 200
        path = 'sample.eps'

    p = _makeRandomData(numPoints, squareLength, addCornerPoints=0)
    c = convexHull(p)
    saveAsEps(p, c, squareLength, path)