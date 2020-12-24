# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vickitoy/Research/RATIR-GSFC/code/photometry/dependencies/photprocesslibrary.py
# Compiled at: 2015-08-10 11:44:28
import astropy.io.fits as pf, fnmatch, os
from numpy import sqrt
import numpy as np

def circle(xcenter, ycenter, radius):
    points = np.linspace(0.0, 2.0 * np.pi, 100)
    x = xcenter + radius * np.cos(points)
    y = ycenter + radius * np.sin(points)
    return np.transpose([x, y])


def nearest(x, y, xarr, yarr, maxdist):
    dist = sqrt((x - xarr) ** 2 + (y - yarr) ** 2)
    good = dist < maxdist
    return good


def choosefiles(selection, loc='.'):
    matches = []
    for files in os.listdir(loc):
        if fnmatch.fnmatch(files, selection):
            matches.append(files)

    return matches


def weightedge(array, itarray, scale=1, column=None, row=None):
    oldsum = 0
    for i in itarray:
        if column is not None:
            newsum = sum(array[:, i])
        elif row is not None:
            newsum = sum(array[i, :])
        if scale * newsum >= oldsum:
            oldsum = newsum
        else:
            return i - 1

    return


def hextractlite(newfile, data, fitsheader, x1, x2, y1, y2):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    fitsheader.add_history('HEXTRACT: Original image size was ' + str(fitsheader['NAXIS2']) + ' by ' + str(fitsheader['NAXIS1']))
    fitsheader.add_history('Extracted Image: [' + str(y1) + ':' + str(y2 + 1) + ',' + str(x1) + ':' + str(x2 + 1) + ']')
    fitsheader.update('naxis1', x2 - x1 + 1)
    fitsheader.update('naxis2', y2 - y1 + 1)
    oldcrpix1 = fitsheader['crpix1']
    oldcrpix2 = fitsheader['crpix2']
    fitsheader.update('crpix1', oldcrpix1 - x1)
    fitsheader.update('crpix2', oldcrpix2 - y1)
    newdata = data[y1:y2 + 1, x1:x2 + 1]
    pf.writeto(newfile, newdata, fitsheader, clobber=True)


from numpy import *

def djs_iterstat(InputArr, SigRej=3.0, MaxIter=10, Mask=0, Max='', Min='', RejVal='', BinData=0):
    NGood = InputArr.size
    ArrShape = InputArr.shape
    if NGood == 0:
        print 'No data points given'
        return (0, 0, 0, 0, 0)
    if NGood == 1:
        print 'Only one data point; cannot compute stats'
        return (0, 0, 0, 0, 0)
    if Max == '':
        Max = InputArr.max()
    if Min == '':
        Min = InputArr.min()
    if unique(InputArr).size == 1:
        return (0, 0, 0, 0, 0)
    Mask = zeros(ArrShape, dtype=byte) + 1
    Mask[InputArr > Max] = 0
    Mask[InputArr < Min] = 0
    if RejVal != '':
        Mask[InputArr == RejVal] = 0
    FMean = sum(1.0 * InputArr * Mask) / NGood
    FSig = sqrt(sum((1.0 * InputArr - FMean) ** 2 * Mask) / (NGood - 1))
    NLast = -1
    Iter = 0
    NGood = sum(Mask)
    if NGood < 2:
        return (-1, -1, -1, -1, -1)
    while Iter < MaxIter and NLast != NGood and NGood >= 2:
        LoVal = FMean - SigRej * FSig
        HiVal = FMean + SigRej * FSig
        NLast = NGood
        Mask[InputArr < LoVal] = 0
        Mask[InputArr > HiVal] = 0
        NGood = sum(Mask)
        if NGood >= 2:
            FMean = sum(1.0 * InputArr * Mask) / NGood
            FSig = sqrt(sum((1.0 * InputArr - FMean) ** 2 * Mask) / (NGood - 1))
            SaveMask = Mask.copy()
        else:
            SaveMask = Mask.copy()
        Iter = Iter + 1

    if sum(SaveMask) > 2:
        FMedian = median(InputArr[(SaveMask == 1)])
        if BinData == 1:
            HRange = InputArr[(SaveMask == 1)].max() - InputArr[(SaveMask == 1)].min()
            bins_In = arange(HRange) + InputArr[(SaveMask == 1)].min()
            Bins, N = histOutline.histOutline(InputArr[(SaveMask == 1)], binsIn=bins_In)
            FMode = Bins[where(N == N.max())[0]].mean()
        else:
            FMode = 0
    else:
        FMedian = FMean
        FMode = FMean
    return (
     FMean, FSig, FMedian, FMode, SaveMask)