# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/MorphoTester/DNE.py
# Compiled at: 2015-10-02 14:15:52
"""
Created on Feb 1, 2012

This module calculates Dirichlet Normal Energy for a provided 3D mesh (see Bunn
et al. 2011 and Winchester 2015 for further details on method) through 
calcdne() and supporting functions. Morpho.py calls calcdne().

@author: Julia M. Winchester
"""
import implicitfair, normcore
from numpy import zeros, transpose, nonzero, sqrt, sum, trace, mat, array, dot, isnan, copy
from numpy.linalg import cond
from scipy.sparse import lil_matrix
from scipy.stats import scoreatpercentile
from collections import defaultdict

def vertexfacedict(faces, nvert):
    vfdict = defaultdict(list)
    for findex, face in enumerate(faces):
        for vertex in face:
            vfdict[vertex].append(findex)

    return vfdict


def edgevertexarray(faces, nvert):
    M = lil_matrix((nvert, nvert))
    nedge = 0
    for face in faces:
        v1, v2, v3 = face
        if M[(v1, v2)] == 0:
            nedge += 1
            M[(v1, v2)] = nedge
            M[(v2, v1)] = nedge
        if M[(v3, v1)] == 0:
            nedge += 1
            M[(v1, v3)] = nedge
            M[(v3, v1)] = nedge
        if M[(v2, v3)] == 0:
            nedge += 1
            M[(v3, v2)] = nedge
            M[(v2, v3)] = nedge

    evarray = zeros([nedge, 2], int)
    nonzeroarray = transpose(nonzero(M))
    for entry in nonzeroarray:
        evarray[M[(entry[0], entry[1])] - 1] = [entry[0], entry[1]]

    return evarray


def boundaryfaces(vfarray, egarray):
    fBoundary = list()
    for verts in egarray:
        f1, f2 = [ vfarray[vert] for vert in verts ]
        cf = [ x for x in f2 for y in f1 if x == y ]
        if len(cf) == 1:
            fBoundary.append(cf[0])

    return fBoundary


def energy(face, i, varray, vnormal, conditioncontrolischecked):
    TV1 = array([varray[face[0]], varray[face[1]], varray[face[2]]])
    TV2 = array([vnormal[face[0]], vnormal[face[1]], vnormal[face[2]]])
    b1 = TV1[1] - TV1[0]
    b2 = TV1[2] - TV1[0]
    g = array(([dot(b1, b1), dot(b1, b2)], [dot(b2, b1), dot(b2, b2)]))
    if conditioncontrolischecked == 1:
        if cond(g) > 100000:
            print 'Warning: high matrix condition number at face number ' + str(i)
            print 'Condition number:  ' + str(cond(g))
            return [
             0, 1]
    c1 = TV2[1] - TV2[0]
    c2 = TV2[2] - TV2[0]
    fstarh = array(([dot(c1, c1), dot(c1, c2)], [dot(c2, c1), dot(c2, c2)]))
    gm = mat(g)
    e = trace(gm.I * fstarh)
    facearea = 0.5 * sqrt(g[(0, 0)] * g[(1, 1)] - g[(0, 1)] * g[(1, 0)])
    if isnan(e):
        print 'TV2 = '
        print TV2
        print 'c1 = ' + str(c1)
        print 'c2 = ' + str(c2)
        print gm.I
        print fstarh
        print e
    return [e, facearea]


def meshenergy(vertex, faceindex, vnormal, conditioncontrolischecked):
    energyfarea = array([ energy(face, i, vertex, vnormal, conditioncontrolischecked) for i, face in enumerate(faceindex) ])
    return [energyfarea[:, 0], energyfarea[:, 1]]


def totaldne(fBoundary, e, facearea, dooutlierremoval):
    e[fBoundary] = 0
    edensity = array([ x * y for x, y in zip(e, facearea) ])
    if dooutlierremoval == 1:
        ptoneperc = scoreatpercentile(e, 99.9)
        for i, energy in enumerate(e):
            if energy > ptoneperc or isnan(energy):
                print 'Energy outlier removed. DNE value: ' + str(energy) + ' Face area: ' + str(facearea[i])
                edensity[i] = 0

    return sum(edensity)


def calcdne(mesh, implicitfairischecked, conditioncontrolischecked, iterationnumber, stepsize, dooutlierremoval):
    varray = mesh[0]
    farray = mesh[2]
    nvert = len(varray)
    if implicitfairischecked == 1:
        varray = implicitfair.smooth(copy(varray), farray, int(iterationnumber), float(stepsize))
        if varray == '!':
            return '!'
    vfdict = vertexfacedict(farray, nvert)
    evarray = edgevertexarray(farray, nvert)
    fboundary = boundaryfaces(vfdict, evarray)
    normals = normcore.computenormal(varray, farray, mesh[1], vfdict)
    energyperface = meshenergy(varray, farray, normals[0], conditioncontrolischecked)
    return totaldne(fboundary, energyperface[0], energyperface[1], dooutlierremoval)