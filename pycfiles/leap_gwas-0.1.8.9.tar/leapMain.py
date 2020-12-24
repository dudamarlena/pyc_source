# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/omerw/git/leap/leap/regression/leapMain.py
# Compiled at: 2014-12-25 11:18:19


def eigenDecompose(bed, outFile=None):
    import eigenDecompose
    return eigenDecompose.eigenDecompose(bed, outFile)


def findRelated(bed, outFile=None, cutoff=0.05):
    import findRelated
    return findRelated.findRelated(bed, outFile, cutoff)


def calcH2(pheno, prev, eigen, keepArr=None, numRemovePCs=10, h2coeff=0.875, lowtail=False):
    import calc_h2
    return calc_h2.calc_h2(pheno, prev, eigen, keepArr, numRemovePCs, h2coeff, lowtail)


def probit(bed, pheno, h2, prev, eigen, outFile=None, keepArr=None, covar=None, thresholds=None, nofail=False, numSkipTopPCs=0, mineig=0.001, hess=False, recenter=True, maxFixedIters=100, epsilon=0.001):
    import probit
    return probit.probit(bed, pheno, h2, prev, eigen, outFile, keepArr, covar, thresholds, nofail, numSkipTopPCs, mineig, hess, recenter, maxFixedIters, epsilon)


def leapGwas(bedSim, bedTest, pheno, h2, outFile=None, eigenFile=None, covar=None):
    import leap_gwas
    return leap_gwas.gwas(bedSim, bedTest, pheno, h2, outFile, eigenFile, covar)