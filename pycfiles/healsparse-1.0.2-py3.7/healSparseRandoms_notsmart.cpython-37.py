# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healsparse/healSparseRandoms_notsmart.py
# Compiled at: 2019-04-09 13:02:56
# Size of source mod 2**32: 5794 bytes
from __future__ import division, absolute_import, print_function
import numpy as np, healpy as hp, copy, esutil

def makeUniformRandoms(sparseMap, nRandom):
    """
    Make an array of uniform randoms.

    Parameters
    ----------
    sparseMap: `healsparse.HealSparseMap`
       Sparse map object
    nRandom: `int`
       Number of randoms to generate

    Returns
    -------
    raArray: `np.array`
       Float array of RAs (degrees)
    decArray: `np.array`
       Float array of declinations (degrees)
    """
    r = 1.0
    minGen = 10000
    maxGen = 1000000
    covMask = sparseMap.coverageMask
    covPix, = np.where(covMask)
    covTheta, covPhi = hp.pix2ang((sparseMap.nsideCoverage), covPix, nest=True)
    extraBoundary = 2.0 * hp.nside2resol(sparseMap.nsideCoverage)
    raRange = np.clip([np.min(covPhi - extraBoundary),
     np.max(covPhi + extraBoundary)], 0.0, 2.0 * np.pi)
    decRange = np.clip([np.min(np.pi / 2.0 - covTheta - extraBoundary),
     np.max(np.pi / 2.0 - covTheta + extraBoundary)], -np.pi / 2.0, np.pi / 2.0)
    rotated = False
    covPhiRot = covPhi + np.pi
    test, = np.where(covPhiRot > 2.0 * np.pi)
    covPhiRot[test] -= 2.0 * np.pi
    raRangeRot = np.clip([np.min(covPhiRot - extraBoundary),
     np.max(covPhiRot + extraBoundary)], 0.0, 2.0 * np.pi)
    if raRangeRot[1] - raRangeRot[0] < raRange[1] - raRange[0] - 0.1:
        raRange = raRangeRot
        rotated = True
    zRange = r * np.sin(decRange)
    phiRange = raRange
    raRand = np.zeros(nRandom)
    decRand = np.zeros(nRandom)
    nLeft = copy.copy(nRandom)
    ctr = 0
    while nLeft > 0:
        nGen = np.clip(nLeft * 2, minGen, maxGen)
        z = np.random.uniform(low=(zRange[0]), high=(zRange[1]), size=nGen)
        phi = np.random.uniform(low=(phiRange[0]), high=(phiRange[1]), size=nGen)
        theta = np.arcsin(z / r)
        raRandTemp = np.degrees(phi)
        decRandTemp = np.degrees(theta)
        if rotated:
            raRandTemp -= 180.0
            raRandTemp[(raRandTemp < 0.0)] += 360.0
        valid, = np.where(sparseMap.getValueRaDec(raRandTemp, decRandTemp, validMask=True))
        nValid = valid.size
        if nValid > nLeft:
            nValid = nLeft
        raRand[ctr:ctr + nValid] = raRandTemp[valid[0:nValid]]
        decRand[ctr:ctr + nValid] = decRandTemp[valid[0:nValid]]
        ctr += nValid
        nLeft -= nValid

    return (raRand, decRand)


def makeSparseUniformRandoms(sparseMap, nRandom):
    """
    Make an array of uniform randoms, using a sparse selection.

    This is more efficient for a very sparse map, but is less
    efficient for a contiguous region.  Also, it may possibly
    introduce artifacts at some scales, which needs to be tested.

    Parameters
    ----------
    sparseMap: `healsparse.HealSparseMap`
       Sparse map object
    nRandom: `int`
       Number of randoms to generate

    Returns
    -------
    raArray: `np.array`
       Float array of RAs (degrees)
    decArray: `np.array`
       Float array of declinations (degrees)
    """
    r = 1.0
    minGen = 10000
    maxGen = 1000000
    covMap = sparseMap.coverageMap
    covPix, = np.where(sparseMap.coverageMask)
    prob = covMap[covPix]
    prob /= prob.sum()
    pixIndices = np.random.choice(covPix, size=nRandom, replace=True, p=prob)
    h, rev = esutil.stat.histogram(pixIndices, min=0, max=(hp.nside2npix(sparseMap.nsideCoverage) - 1), rev=True)
    raRand = np.zeros(nRandom)
    decRand = np.zeros(nRandom)
    ctr = 0
    gdPix, = np.where(h > 0)
    for pix in gdPix:
        nLeft = h[pix]
        i1a = rev[rev[pix]:rev[(pix + 1)]]
        corners = hp.boundaries((sparseMap.nsideCoverage), pix, nest=True, step=1)
        cornerTheta, cornerPhi = hp.vec2ang(corners.T)
        raRange = [
         np.min(cornerPhi), np.max(cornerPhi)]
        decRange = [np.min(np.pi / 2.0 - cornerTheta), np.max(np.pi / 2.0 - cornerTheta)]
        zRange = r * np.sin(decRange)
        phiRange = raRange
        while nLeft > 0:
            nGen = np.clip(nLeft * 2, minGen, maxGen)
            z = np.random.uniform(low=(zRange[0]), high=(zRange[1]), size=nGen)
            phi = np.random.uniform(low=(phiRange[0]), high=(phiRange[1]), size=nGen)
            theta = np.arcsin(z / r)
            raRandTemp = np.degrees(phi)
            decRandTemp = np.degrees(theta)
            valid, = np.where(sparseMap.getValueRaDec(raRandTemp, decRandTemp, validMask=True))
            nValid = valid.size
            if nValid > nLeft:
                nValid = nLeft
            raRand[ctr:ctr + nValid] = raRandTemp[valid[0:nValid]]
            decRand[ctr:ctr + nValid] = decRandTemp[valid[0:nValid]]
            ctr += nValid
            nLeft -= nValid

    return (
     raRand, decRand)