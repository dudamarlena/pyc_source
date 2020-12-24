# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/utility.py
# Compiled at: 2009-05-29 13:49:17
import numpy, os, config
from scipy import size

def getDataArray(matrixString, **args):
    """ Read data and save as array."""
    tmpFname = 'tempMat.dat'
    tmpFile = open(tmpFname, 'w+')
    tmpFile.write(matrixString)
    tmpFile.close()
    try:
        matrix = numpy.loadtxt(tmpFname)
    except:
        return [
         0]

    return matrix


def getLabelAndDataArray(str, **args):
    """ Read label as list and data as array to save them as dictionary."""
    firstReturn = str.find('\n')
    line1 = str[:firstReturn]
    rest = str[firstReturn + 1:]
    labels = line1.split()
    matrix = getDataArray(rest)
    if matrix.any() == 0:
        return 0
    numCol = size(matrix, 1)
    if numCol != len(labels):
        raise 'Number of coloumns=%d is not equal to number of labels=%d.' % (numCol, len(labels))
    dict = {}
    for i in range(len(labels)):
        dict[labels[i]] = matrix[:, i]

    return (
     dict, labels)


def readExp(fpath):
    fid = open(fpath, 'r')
    strAll = fid.read()
    D = getLabelAndDataArray(strAll)
    return D


def readModelMacro(fpath='epsc3.out'):
    """ Read macro model result(array) with labels(lists) as dictionary."""
    fid = open(fpath, 'r')
    strAll = fid.read()
    ind = strAll.find('EPS1')
    str = strAll[ind:]
    print str
    D = getLabelAndDataArray(str)
    fid.close()
    return D


def readModelHKL(fpath='epsc9.out'):
    """ Read hkl model result(array) with labels(lists) as dictionary."""
    fid = open(fpath, 'r')
    strAll = fid.read()
    ind1 = strAll.find('angle_eta')
    if ind1 == -1:
        return -1
    ind2 = strAll.find('\n', ind1)
    ind3 = strAll.find('SET', ind2)
    hklString = strAll[ind2 + 1:ind3].strip()
    hklLines = hklString.split('\n')
    ind4 = strAll.find('control', ind3)
    valueString = strAll[ind4:]
    (D, labels) = getLabelAndDataArray(valueString)
    fid.close()
    return D


def readModelHKL_phase1(fpath='epsc9.out'):
    """ Read hkl model result(array) with labels(lists) as dictionary."""
    fid = open(fpath, 'r')
    strAll = fid.read()
    ind1 = strAll.find('angle_eta')
    ind2 = strAll.find('\n', ind1)
    ind3 = strAll.find('SET', ind2)
    hklString = strAll[ind2 + 1:ind3].strip()
    hklLines = hklString.split('\n')
    ind4 = strAll.find('control', ind3)
    valueString = strAll[ind4:]
    (D, labels) = getLabelAndDataArray(valueString)
    fid.close()
    return D


def checkExp(fpath, names):
    """ function which check the file(fpath) have properties with name in 'names'
    """
    try:
        fid = open(fpath, 'r')
        strAll = fid.read()
        (labels, data) = getLabelAndDataArray(strAll)
        for name in names:
            if labels.has_key(name) == False:
                return False

    except:
        return False

    return True