# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/hcpre/util.py
# Compiled at: 2014-01-08 13:26:15


def orientation_from_dcm_header(header):
    if not header:
        raise ValueError("didn't get a header")
    o = getattr(header, 'ImageOrientationPatient', None)
    o = [ float(a) for a in o ]
    if not o:
        raise ValueError("couldn't find ImageOrientationPatient in header")
    if len(o) != 6:
        raise ValueError('cannot be translated to cosine vectors')
    epsilon = 0.001
    if abs(o[0] * o[3] + o[1] * o[4] + o[2] * o[5]) > 0.001:
        raise ValueError('cosine vectors not orthogonal')
    if abs(1.0 - o[0] * o[0] - o[1] * o[1] - o[2] * o[2]) > epsilon:
        raise ValueError('cosine vectors not normal')
    absNormalX = abs(o[1] * o[5] - o[2] * o[4])
    absNormalY = abs(o[2] * o[3] - o[0] * o[5])
    absNormalZ = abs(o[0] * o[4] - o[1] * o[3])
    if absNormalX > absNormalY:
        if absNormalX > absNormalZ:
            return 'sagittal'
        return 'transverse'
    else:
        if absNormalY > absNormalZ:
            return 'coronal'
        else:
            return 'transverse'

        return


def numberfy(s):
    n = s
    try:
        n = float(n)
        return n
    except Exception:
        return s


def float_or_none(s):
    n = s
    try:
        n = float(n)
        return n
    except Exception:
        return

    return


def int_or_none(s):
    n = s
    try:
        n = int(n)
        return n
    except ValueError:
        return

    return