# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\lib\affine.py
# Compiled at: 2002-01-21 21:43:26


class AffineMatrix:
    """Represents a 2D + 1 affine transformation"""

    def __init__(self, init=None):
        if init:
            if len(init) == 6:
                self.A = init
            if type(init) == type(self):
                self.A = init.A
        else:
            self.A = [
             1.0, 0, 0, 1.0, 0.0, 0.0]

    def scale(self, sx, sy):
        self.A = [sx * self.A[0], sx * self.A[1], sy * self.A[2], sy * self.A[3], self.A[4], self.A[5]]

    def rotate(self, theta):
        """counter clockwise rotation in standard SVG/libart coordinate system"""
        co = math.cos(PI * theta / 180.0)
        si = math.sin(PI * theta / 180.0)
        self.A = [self.A[0] * co + self.A[2] * si,
         self.A[1] * co + self.A[3] * si,
         -self.A[0] * si + self.A[2] * co,
         -self.A[1] * si + self.A[3] * co,
         self.A[4],
         self.A[5]]

    def translate(self, tx, ty):
        self.A = [
         self.A[0], self.A[1], self.A[2], self.A[3],
         self.A[0] * tx + self.A[2] * ty + self.A[4],
         self.A[1] * tx + self.A[3] * ty + self.A[5]]

    def rightMultiply(self, a, b, c, d, e, f):
        """multiply self.A by matrix M defined by coefficients a,b,c,d,e,f"""
        m = self.A
        self.A = [m[0] * a + m[2] * b,
         m[1] * a + m[3] * b,
         m[0] * c + m[2] * d,
         m[1] * c + m[3] * d,
         m[0] * e + m[2] * f + m[4],
         m[1] * e + m[3] * f + m[5]]

    def transformPt(self, pt):
        (x, y) = pt
        (a, b, c, d, e, f) = self.A
        return [a * x + c * y + e, b * x + d * y + f]

    def scaleRotateVector(self, v):
        (x, y) = v
        (a, b, c, d, e, f) = self.A
        return [a * x + c * y, b * x + d * y]

    def transformFlatList(self, seq):
        N = len(seq)
        res = []
        for ii in xrange(0, N, 2):
            pt = self.transformPt((seq[ii], seq[(ii + 1)]))
            res.extend(pt)

        return res