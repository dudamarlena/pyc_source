# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/max/Workspaces/gsfc/photometry_pipeline/code/reduction/astrom/astrometrystats.py
# Compiled at: 2016-11-15 15:22:29
import numpy

def median(l):
    a = numpy.array(l)
    return numpy.median(a)


def stdev(l):
    a = numpy.array(l)
    return numpy.std(a)


def most(list, vmin=1, vmax=1):
    counter = numpy.zeros(len(list))
    for i in range(0, len(list)):
        counter[i] = ((list[i] + vmax >= list) & (list[i] - vmin <= list)).sum()

    if len(set(counter)) == 1:
        return numpy.median(list)
    else:
        return list[counter.argmax()]


def rasex2deg(rastr):
    rastr = str(rastr).strip()
    ra = rastr.split(':')
    if len(ra) == 1:
        return float(rastr)
    return 15 * (float(ra[0]) + float(ra[1]) / 60.0 + float(ra[2]) / 3600.0)


def decsex2deg(decstr):
    decstr = str(decstr).strip()
    dec = decstr.split(':')
    if len(dec) == 1:
        return float(decstr)
    sign = 1
    if decstr[0] == '-':
        sign = -1
    return sign * (abs(float(dec[0])) + float(dec[1]) / 60.0 + float(dec[2]) / 3600.0)


def magcomp(obj1, obj2):
    return (obj1.mag > obj2.mag) - (obj1.mag < obj2.mag)


def unique(inlist):
    lis = inlist[:]
    lis.sort()
    llen = len(lis)
    i = 0
    while i < llen - 1:
        if lis[(i + 1)] == lis[i]:
            del lis[i + 1]
            llen = llen - 1
        else:
            i = i + 1

    return lis