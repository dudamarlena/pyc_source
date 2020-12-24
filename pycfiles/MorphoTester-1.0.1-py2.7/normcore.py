# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/MorphoTester/normcore.py
# Compiled at: 2015-10-02 14:16:33
"""
Created on Oct 1, 2015

Functions for the creation and manipulation of normal vectors.

@author: Julia M. Winchester
"""
from numpy import cross, array, sqrt, column_stack, spacing, zeros, isnan, mean, sum

def normal(plane):
    a = plane[0]
    b = plane[1]
    c = plane[2]
    ab = [b[0] - a[0], b[1] - a[1], b[2] - a[2]]
    ac = [c[0] - a[0], c[1] - a[1], c[2] - a[2]]
    return cross(ab, ac)


def normalmap(varray, farray):
    return array([ normal(varray[verts]) for verts in farray ])


def normalize(vects):
    d = sqrt((vects ** 2).sum(axis=1))
    d = [ 1 if m < spacing(1) else m for m in d ]
    return vects / column_stack((d, d, d))


def computenormal(varray, faceindex, fvarray, vfarray):
    nvert = len(varray)
    fnormal = normalmap(varray, faceindex)
    fnormal4 = normalize(fnormal)
    vnormal = zeros([nvert, 3], float)
    for vindex, faces in vfarray.iteritems():
        vnormal[vindex] = sum(fnormal4[faces], axis=0)
        if isnan(fnormal4[faces]).any():
            print 'nan found during vertex normal creation at vertex #: ' + str(vindex)

    vnormal4 = normalize(vnormal)
    for i, norm in enumerate(vnormal4):
        if isnan(norm).any():
            print 'nan vnormal 4 entry found'
            print 'corresponding vnormal entry:'
            print norm

    mvertex = mean(varray, 1)
    repmvertex = column_stack((mvertex, mvertex, mvertex))
    v = varray - repmvertex
    s = sum(v * vnormal4, 0)
    s2 = 0
    s3 = 0
    for i in s:
        if i > 0:
            s2 += 1
        if i < 0:
            s3 += 1

    if s2 < s3:
        print 'Outward normal flipping has occurred'
        vnormal4 = -vnormal4
        fnormal4 = -fnormal4
    return [vnormal4, fnormal4]