# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\lib\bezierPolynomial.py
# Compiled at: 2002-01-21 21:43:26


def cubicCurveToBezierCtrlPts(tinterval=(0.0, 1.0), A=(0.0, 0.0), B=(0.0, 0.0), C=(0.0, 0.0), D=(0.0, 0.0)):
    """Given a parameterized curve,  W(t) = A t^3 + B t^2 + C t + D,
    where A,B,C,D are 2D vectors and t ranges from tinterval[0] to tinterval[1],
    returns the bezier ctrl points for the curve"""
    coeffs = _cubicCurveReparameterizeT(tinterval[0], tinterval[1], A, B, C, D)
    return _normalizedCubicCoeff2BezierCtrlPts(coeffs)


def _cubicCurveReparameterizeT(T1, T2, A, B, C, D):
    """Given a curve w(t) = A t^3 + B t^2 + C t + D with t going from T1 to T2,"""
    scale = T2 - T1
    scale2 = scale ** 2
    scale3 = scale ** 3
    a = (A[0] * scale3, A[1] * scale3)
    b = ((B[0] + 3 * A[0]) * scale2, (B[1] + 3 * A[1]) * scale2)
    c = (
     (C[0] + T1 * (2 * B[0] + 3 * A[0] * T1)) * scale, (C[1] + T1 * (2 * B[1] + 3 * A[1] * T1)) * scale)
    d = (A[0] * T1 ** 3 + B[0] * T1 ** 2 + C[0] * T1 + D[0], A[1] * T1 ** 3 + B[1] * T1 ** 2 + C[1] * T1 + D[1])
    return (a, b, c, d)


def _normalizedCubicCoeff2BezierCtrlPts(coeffs):
    """Given a curve w(t) = a t^3 + b t^2 + c t + d with t going from 0 to 1
"""
    (a, b, c, d) = coeffs
    x = [d[0], 0, 0, 0]
    y = [d[1], 0, 0, 0]
    v = [x, y]
    for ii in (0, 1):
        v[ii][1] = v[ii][0] + c[ii] / 3.0
        v[ii][2] = v[ii][1] + (c[ii] + b[ii]) / 3.0
        v[ii][3] = v[ii][0] + c[ii] + b[ii] + a[ii]

    return (x[0], y[0],
     x[1], y[1],
     x[2], y[2],
     x[3], y[3])


def quadraticToCtrlPts(xinterval, A=0.0, B=0.0, C=0.0):
    """return the control points for a bezier curve that fits the quadratic function
    y = A x^2 + B x + C.  for the interval along the x-axis given by xinterval=(x0,x1)"""
    x0 = float(xinterval[0])
    x3 = float(xinterval[1])
    y0 = A * x0 ** 2 + B * x0 + C
    xlen = x3 - x0
    cx = xlen
    a = (0, 0)
    b = (0, A * cx * cx)
    c = (cx, B * cx + 2 * b[1] * x0 / cx)
    v0 = (x0, C - b[1] / (cx * cx) * x0 * x0)
    x = [
     x0, 0, 0, 0]
    y = [y0, 0, 0, 0]
    v = [
     x, y]
    for ii in (0, 1):
        v[ii][1] = v[ii][0] + c[ii] / 3.0
        v[ii][2] = v[ii][1] + (c[ii] + b[ii]) / 3.0
        v[ii][3] = v[ii][0] + c[ii] + b[ii] + a[ii]

    return (v[0][0], v[1][0],
     v[0][1], v[1][1],
     v[0][2], v[1][2],
     v[0][3], v[1][3])


def cubicToCtrlPts(xinterval, A=0.0, B=0.0, C=0.0, D=0):
    """return the control points for a bezier curve that fits the cubic polynomial
    y = A x^3 + B x^2 + C x + D.  for the interval along the x-axis given by
    xinterval=(xStart,xEnd)"""
    x0 = float(xinterval[0])
    x3 = float(xinterval[1])
    x0sqrd = x0 * x0
    y0 = A * x0 * x0sqrd + B * x0sqrd + C * x0 + D
    xlen = x3 - x0
    cx = xlen
    a = (
     0, A * cx * cx * cx)
    b = (0, B * cx * cx + 3 * A * cx * cx * x0)
    c = (cx, C * cx + 2 * B * cx * x0 + 3 * A * cx * x0 * x0)
    v0 = (x0, y0)
    x = [
     x0, 0, 0, 0]
    y = [y0, 0, 0, 0]
    v = [
     x, y]
    for ii in (0, 1):
        v[ii][1] = v[ii][0] + c[ii] / 3.0
        v[ii][2] = v[ii][1] + (c[ii] + b[ii]) / 3.0
        v[ii][3] = v[ii][0] + c[ii] + b[ii] + a[ii]

    return (v[0][0], v[1][0],
     v[0][1], v[1][1],
     v[0][2], v[1][2],
     v[0][3], v[1][3])