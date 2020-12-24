# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lhsmdu/__init__.py
# Compiled at: 2018-02-23 06:43:09
""" This is an implementation of Latin Hypercube Sampling with Multi-Dimensional Uniformity (LHS-MDU) from Deutsch and Deutsch, "Latin hypercube sampling with multidimensional uniformity", Journal of Statistical Planning and Inference 142 (2012) , 763-772 

***Currently only for independent variables***
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from numpy.linalg import norm
from numpy import random, matrix, zeros, triu_indices, sum, argsort, ravel, max
from numpy import min as minimum
from scipy.stats import rv_continuous, rv_discrete
from scipy.stats.distributions import rv_frozen
scalingFactor = 5
numToAverage = 2
randomSeed = 42

def createRandomStandardUniformMatrix(nrow, ncol):
    """ Creates a matrix with elements drawn from a uniform distribution in [0,1]"""
    rows = [ [ random.random() for i in range(ncol) ] for j in range(nrow) ]
    return matrix(rows)


def findUpperTriangularColumnDistanceVector(inputMatrix, ncol):
    """ Finds the 1-D upper triangular euclidean distance vector for the columns of a matrix."""
    assert ncol == inputMatrix.shape[1]
    distance_1D = []
    for i in range(ncol - 1):
        for j in range(i + 1, ncol):
            realization_i, realization_j = inputMatrix[:, i], inputMatrix[:, j]
            distance_1D.append(norm(realization_i - realization_j))

    return distance_1D


def createSymmetricDistanceMatrix(distance, nrow):
    """ Creates a symmetric distance matrix from an upper triangular 1D distance vector."""
    distMatrix = zeros((nrow, nrow))
    indices = triu_indices(nrow, k=1)
    distMatrix[indices] = distance
    distMatrix[(indices[1], indices[0])] = distance
    return distMatrix


def eliminateRealizationsToStrata(distance_1D, matrixOfRealizations, numSamples, numToAverage=numToAverage):
    """ Eliminating realizations using average distance measure to give Strata """
    numDimensions = matrixOfRealizations.shape[0]
    numRealizations = matrixOfRealizations.shape[1]
    distMatrix = createSymmetricDistanceMatrix(distance_1D, numRealizations)
    averageDistance = {i:0 for i in range(numRealizations)}
    while len(averageDistance) > numSamples:
        for rowNum in sorted(averageDistance.keys()):
            meanAvgDist = sum(sorted(distMatrix[(rowNum, sorted(averageDistance.keys()))])[:numToAverage + 1]) / numToAverage
            averageDistance.update({rowNum: meanAvgDist})

        indexToDelete = min(averageDistance, key=averageDistance.get)
        del averageDistance[indexToDelete]

    StrataMatrix = matrixOfRealizations[:, sorted(averageDistance.keys())]
    assert numSamples == StrataMatrix.shape[1]
    assert numDimensions == StrataMatrix.shape[0]
    return StrataMatrix


def inverseTransformSample(distribution, uniformSamples):
    """ This function lets you convert from a standard uniform sample [0,1] to
    a sample from an arbitrary distribution. This is done by taking the cdf [0,1] of 
    the arbitrary distribution, and calculating its inverse to picking the sample."
    """
    assert isinstance(distribution, rv_continuous) or isinstance(distribution, rv_discrete) or isinstance(distribution, rv_frozen)
    newSamples = distribution.ppf(uniformSamples)
    return newSamples


def resample():
    """ Resampling function from the same strata"""
    numDimensions = matrixOfStrata.shape[0]
    numSamples = matrixOfStrata.shape[1]
    matrixOfSamples = []
    for row in range(numDimensions):
        sortedIndicesOfStrata = argsort(ravel(matrixOfStrata[row, :]))
        newSamples = [ float(x) / numSamples + random.random() / numSamples for x in sortedIndicesOfStrata ]
        matrixOfSamples.append(newSamples)

    assert minimum(matrixOfSamples) >= 0.0
    assert max(matrixOfSamples) <= 1.0
    return matrix(matrixOfSamples)


def sample(numDimensions, numSamples, scalingFactor=scalingFactor, numToAverage=numToAverage, randomSeed=randomSeed):
    """ Main LHS-MDU sampling function """
    global matrixOfStrata
    random.seed(randomSeed)
    numRealizations = scalingFactor * numSamples
    matrixOfRealizations = createRandomStandardUniformMatrix(numDimensions, numRealizations)
    distance_1D = findUpperTriangularColumnDistanceVector(matrixOfRealizations, numRealizations)
    matrixOfStrata = eliminateRealizationsToStrata(distance_1D, matrixOfRealizations, numSamples)
    matrixOfSamples = resample()
    return matrixOfSamples