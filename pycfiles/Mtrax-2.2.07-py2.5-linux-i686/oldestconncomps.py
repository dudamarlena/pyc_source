# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/oldestconncomps.py
# Compiled at: 2007-11-14 08:40:27
import numpy as num
from ellipsesk import *
from pylab import *
import scipy.ndimage as meas
from kcluster import gmm
from params import params

def ell2cov(a, b, theta):
    S = num.zeros((2, 2))
    costheta = num.cos(theta)
    sintheta = num.sin(theta)
    a = a ** 2
    b = b ** 2
    S[(0, 0)] = costheta ** 2 * a + sintheta ** 2 * b
    S[(1, 1)] = sintheta ** 2 * a + costheta ** 2 * b
    S[(0, 1)] = sintheta * costheta * (a - b)
    S[(1, 0)] = S[(0, 1)]
    return S


def cov2ell2(S00, S11, S01):
    tmp1 = S00 + S11
    tmp2 = num.sqrt(4.0 * S01 ** 2.0 + (S00 - S11) ** 2.0)
    eigA = (tmp1 + tmp2) / 2.0
    eigB = (tmp1 - tmp2) / 2.0
    angle = 0.5 * num.arctan2(2.0 * S01, S00 - S11)
    if eigB > eigA:
        sizeW = num.sqrt(eigA)
        sizeH = num.sqrt(eigB)
    else:
        sizeW = num.sqrt(eigB)
        sizeH = num.sqrt(eigA)
    return (
     sizeH, sizeW, angle)


def cov2ell(S):
    tmp1 = S[(0, 0)] + S[(1, 1)]
    tmp2 = num.sqrt(4.0 * S[(0, 1)] ** 2.0 + (S[(0, 0)] - S[(1, 1)]) ** 2.0)
    eigA = (tmp1 + tmp2) / 2.0
    eigB = (tmp1 - tmp2) / 2.0
    angle = 0.5 * num.arctan2(2.0 * S[(0, 1)], S[(0, 0)] - S[(1, 1)])
    if eigB > eigA:
        sizeW = num.sqrt(eigA)
        sizeH = num.sqrt(eigB)
    else:
        sizeW = num.sqrt(eigB)
        sizeH = num.sqrt(eigA)
    return (
     sizeH, sizeW, angle)


def drawellipse(ellipse, format='w', params={}):
    theta = num.linspace(-0.03, 2 * num.pi, 100)
    x = 2 * ellipse.major * num.cos(theta)
    y = 2 * ellipse.minor * num.sin(theta)
    X = num.cos(ellipse.angle) * x - num.sin(ellipse.angle) * y
    Y = num.sin(ellipse.angle) * x + num.cos(ellipse.angle) * y
    X += ellipse.center.x
    Y += ellipse.center.y
    h = plot(X, Y, format, **params)
    return h


def ellipsepixels(ellipse, bounds):
    S = ell2cov(ellipse.major, ellipse.minor, ellipse.angle)
    (x, y) = num.meshgrid(num.arange(bounds[2], bounds[3], 1), num.arange(bounds[0], bounds[1], 1))
    x -= ellipse.center.x
    y -= ellipse.center.y
    Sinv = num.linalg.inv(S)
    d = x ** 2 * Sinv[(0, 0)] + 2 * Sinv[(0, 1)] * x * y + y ** 2 * Sinv[(1, 1)]
    bw = d <= 4
    return bw


def copyellipse(ellipses, i, newellipse):
    """Should use ellipse.copy() instead."""
    import warnings
    warnings.warn('copyellipse() is unnecessary. Use ellipse.copy() instead.', DeprecationWarning)
    ellipses[i].center.x = newellipse.center.x
    ellipses[i].center.y = newellipse.center.y
    ellipses[i].major = newellipse.major
    ellipses[i].minor = newellipse.minor
    ellipses[i].angle = newellipse.angle
    ellipses[i].area = newellipse.area


def weightedregionpropsi(BWI, w):
    Z = sum(w)
    if Z == 0:
        Z = 1
    (r, c) = num.where(BWI)
    centerX = sum(c * w) / Z
    centerY = sum(r * w) / Z
    S = num.zeros((2, 2))
    S[(0, 0)] = sum(w * c ** 2) / Z - centerX ** 2
    S[(1, 1)] = sum(w * r ** 2) / Z - centerY ** 2
    S[(0, 1)] = sum(w * c * r) / Z - centerX * centerY
    S[(1, 0)] = S[(0, 1)]
    (sizeH, sizeW, angle) = cov2ell(S)
    if sizeH < 0.125 or num.isnan(sizeH):
        sizeH = 0.125
        sizeW = 0.125
    elif sizeW < 0.125 or num.isnan(sizeW):
        sizeW = 0.125
    area = num.pi * sizeW * sizeH * 4
    return Ellipse(centerX, centerY, sizeW, sizeH, angle, area, -1)


def weightedregionprops(L, ncc, dfore):
    if ncc == 0:
        return []
    index = range(1, ncc + 1)
    time0 = time.time()
    w = dfore
    z = num.array(meas.sum(w, L, index))
    z[z == 0] = 1
    cx = num.array(meas.sum(w * params.GRID.X, L, index))
    cy = num.array(meas.sum(w * params.GRID.Y, L, index))
    cx /= z
    cy /= z
    cx2 = num.array(meas.sum(w * params.GRID.X2, L, index))
    cy2 = num.array(meas.sum(w * params.GRID.Y2, L, index))
    cxy = num.array(meas.sum(w * params.GRID.XY, L, index))
    cx2 /= z
    cy2 /= z
    cxy /= z
    cx2 -= cx ** 2
    cy2 -= cy ** 2
    cxy -= cx * cy
    ellipses = []
    for i in range(len(cx)):
        (sizeH, sizeW, angle) = cov2ell2(cx2[i], cy2[i], cxy[i])
        if sizeH < 0.125 or num.isnan(sizeH):
            sizeH = 0.125
        if sizeW < 0.125 or num.isnan(sizeW):
            sizeW = 0.125
        area = num.pi * sizeW * sizeH * 4
        ellipses.append(Ellipse(cx[i], cy[i], sizeW, sizeH, angle, area, -1))

    return ellipses


def getboundingboxbig(ellipse, sz):
    r1 = floor(ellipse.center.y - params.maxshape.major * 4)
    if r1 < 0:
        r1 = 0
    r2 = ceil(ellipse.center.y + params.maxshape.major * 4) + 1
    if r2 > sz[0]:
        r2 = sz[0]
    c1 = floor(ellipse.center.x - params.maxshape.major * 4)
    if c1 < 0:
        c1 = 0
    c2 = ceil(ellipse.center.x + params.maxshape.major * 4) + 1
    if c2 > sz[1]:
        c2 = sz[1]
    return (
     r1, r2, c1, c2)


def getboundingboxtight(ellipse, sz):
    r1 = floor(ellipse.center.y - ellipse.major * 2)
    if r1 < 0:
        r1 = 0
    r2 = ceil(ellipse.center.y + ellipse.major * 2) + 1
    if r2 > sz[0]:
        r2 = sz[0]
    c1 = floor(ellipse.center.x - ellipse.major * 2)
    if c1 < 0:
        c1 = 0
    c2 = ceil(ellipse.center.x + ellipse.major * 2) + 1
    if c2 > sz[1]:
        c2 = sz[1]
    return (
     r1, r2, c1, c2)


def getnewlabel(Lnewbox, ncc, Lbox, i):
    if ncc == 1:
        llowerthresh = 1
    else:
        newl = Lnewbox[(Lbox == i + 1)]
        llowerthresh = newl[0]
        if num.all(newl == llowerthresh) == False:
            print 'Something is wrong -- this should never happen!\n'
            bins = linspace(-0.5, ncc + 0.5, ncc + 2)
            votes = num.histogram(Lnewbox[(Lbox == i + 1)], bins)
            llowerthresh = argmax(votes)
    return llowerthresh


def trylowerthresh(ellipses, i, L, dfore):
    if params.minbackthresh >= 1:
        return (
         True, ellipses[i])
    (r1, r2, c1, c2) = getboundingboxbig(ellipses[i], L.shape)
    dforebox = dfore[r1:r2, c1:c2]
    isforebox = dforebox >= params.minbackthresh * params.n_bg_std_thresh_low
    Lbox = L[r1:r2, c1:c2]
    (Lnewbox, ncc) = meas.label(isforebox)
    inew = getnewlabel(Lnewbox, ncc, Lbox, i)
    tmp = Lbox[(Lnewbox == inew)]
    if num.any(num.logical_and(tmp != 0, tmp != i + 1)):
        return (True, ellipses[i])
    ellipsenew = weightedregionpropsi(Lnewbox == inew, dforebox[(Lnewbox == inew)])
    ellipsenew.x += c1
    ellipsenew.y += r1
    issmall = ellipsenew.area < params.minshape.area
    return (issmall, ellipsenew)


def findclosecenters(ellipses, i):
    if num.isinf(params.maxshape.major):
        maxmajor = 0.0
        for ell in ellipses:
            maxmajor = max(maxmajor, ell.major)

    else:
        maxmajor = params.maxshape.major
    maxdmergecenter = maxmajor * 4 + ellipses[i].minor * 2
    isotherind = num.ones(len(ellipses), dtype=bool)
    isotherind[i] = False
    for j in range(len(ellipses)):
        if ellipses[j].area == 0:
            isotherind[j] = False

    otherinds = num.where(isotherind)[0]
    nother = len(otherinds)
    dx = num.zeros(nother)
    for j in range(nother):
        dx[j] = abs(ellipses[otherinds[j]].center.x - ellipses[i].center.x)

    isclose = dx < maxdmergecenter
    cannotmerge = num.any(isclose) == False
    if cannotmerge == False:
        dy = num.zeros(nother)
        dy[:] = maxdmergecenter
        dy[isclose] = abs(ellipses[j].center.y - ellipses[i].center.y)
        isclose[isclose] = dy[isclose] < maxdmergecenter
        cannotmerge = num.any(isclose) == False
    if cannotmerge == False:
        maxdmergecentersquared = maxdmergecenter ** 2
        d = num.zeros(nother)
        d[:] = maxdmergecentersquared
        d[isclose] = dx[isclose] ** 2 + dy[isclose] ** 2
        isclose[isclose] = d[isclose] < maxdmergecentersquared
        cannotmerge = num.any(isclose) == False
    indsmerge = otherinds[isclose]
    return indsmerge


def computemergepenalty(ellipses, i, j, L, dfore):
    BWmerge = num.logical_or(L == i + 1, L == j + 1)
    if not BWmerge.any():
        return (
         0.0, ellipses[i])
    ellipsemerge = weightedregionpropsi(BWmerge, dfore[BWmerge])
    if ellipsemerge.area > params.maxshape.area or ellipsemerge.minor > params.maxshape.minor or ellipsemerge.major > params.maxshape.major:
        return (
         params.maxpenaltymerge, ellipses[i])
    (r1, r2, c1, c2) = getboundingboxtight(ellipsemerge, L.shape)
    isforepredmerge = ellipsepixels(ellipsemerge, num.array([r1, r2, c1, c2]))
    isforepredi = ellipsepixels(ellipses[i], num.array([r1, r2, c1, c2]))
    isforepredj = ellipsepixels(ellipses[j], num.array([r1, r2, c1, c2]))
    isforepredi = num.logical_or(isforepredi, L[r1:r2, c1:c2] == i + 1)
    newforemerge = num.logical_and(isforepredmerge, num.logical_or(isforepredi, isforepredj) == False)
    dforemerge = dfore[r1:r2, c1:c2]
    dforemerge = 1 - dforemerge[newforemerge]
    dforemerge[dforemerge < 0] = 0
    mergepenalty = num.sum(dforemerge)
    return (
     mergepenalty, ellipsemerge)


def mergeellipses(ellipses, i, j, ellipsemerge, issmall, L):
    ellipses[i] = ellipsemerge.copy()
    ellipses[j].area = 0
    issmall[i] = ellipsemerge.area < params.minshape.area
    issmall[j] = False
    L[L == j + 1] = i + 1


def trymerge(ellipses, issmall, i, L, dfore):
    closeinds = findclosecenters(ellipses, i)
    if len(closeinds) == 0:
        return False
    mergepenalty = ones(len(closeinds))
    mergepenalty[:] = params.maxpenaltymerge
    ellipsesmerge = []
    for j in range(len(closeinds)):
        (mergepenalty[j], newellipse) = computemergepenalty(ellipses, i, closeinds[j], L, dfore)
        ellipsesmerge.append(newellipse)

    bestjmerge = num.argmin(mergepenalty)
    minmergepenalty = mergepenalty[bestjmerge]
    if minmergepenalty > params.maxpenaltymerge:
        return False
    canmergewith = closeinds[bestjmerge]
    mergeellipses(ellipses, i, canmergewith, ellipsesmerge[bestjmerge], issmall, L)
    return True


def trydelete(ellipses, i, issmall):
    if ellipses[i].area < params.maxareadelete:
        ellipses[i].area = 0
        issmall[i] = False


def deleteellipses(ellipses, L):
    i = 0
    while True:
        if i >= len(ellipses):
            break
        if ellipses[i].area == 0:
            ellipses.pop(i)
            L[L == i + 1] = 0
            L[L > i + 1] = L[(L > i + 1)] - 1
        else:
            i += 1


def printellipse(ellipse):
    print '[x: %f y: %f a: %f b: %f t: %f A: %f]' % (ellipse.center.x, ellipse.center.y, ellipse.major, ellipse.minor, ellipse.angle, ellipse.area)


def fixsmall(ellipses, L, dfore):
    issmall = num.zeros(len(ellipses), dtype=bool)
    for i in range(len(ellipses)):
        issmall[i] = ellipses[i].area < params.minshape.area

    while num.any(issmall):
        i = num.where(issmall)[0]
        i = i[0]
        didmerge = False
        (issmall[i], ellipselowerthresh) = trylowerthresh(ellipses, i, L, dfore)
        if issmall[i] == False:
            ellipses[i] = ellipselowerthresh
        if issmall[i]:
            didmerge = trymerge(ellipses, issmall, i, L, dfore)
        if issmall[i] and didmerge == False:
            ellipses[i] = ellipselowerthresh.copy()
            trydelete(ellipses, i, issmall)
            issmall[i] = False

    deleteellipses(ellipses, L)


def trysplit(ellipses, i, isdone, L, dfore):
    (r, c) = num.where(L == i + 1)
    x = num.hstack((c.reshape(c.size, 1), r.reshape(r.size, 1)))
    w = dfore[(L == i + 1)]
    ndata = r.size
    err0 = num.abs(ellipses[i].area - params.meanshape.area)
    ncomponents = 2
    while True:
        (mu, S, priors, gamma, negloglik) = gmm(x, ncomponents, weights=w, kmeansthresh=0.1, emthresh=0.1)
        err = 0
        major = num.zeros(ncomponents)
        minor = num.zeros(ncomponents)
        angle = num.zeros(ncomponents)
        area = num.zeros(ncomponents)
        for j in range(ncomponents):
            (major[j], minor[j], angle[j]) = cov2ell(S[:, :, j])
            area[j] = major[j] * minor[j] * num.pi * 4.0
            if area[j] < params.minshape.area:
                err += 10000
            else:
                err += num.abs(params.meanshape.area - area[j])

        if err >= err0:
            break
        ncomponents += 1
        mu0 = mu.copy()
        major0 = major.copy()
        minor0 = minor.copy()
        angle0 = angle.copy()
        area0 = area.copy()
        err0 = err
        gamma0 = gamma.copy()

    ncomponents -= 1
    if ncomponents == 1:
        isdone[i] = True
    else:
        idx = num.argmax(gamma0, axis=1)
        ellipses[i].center.x = mu0[(0, 0)]
        ellipses[i].center.y = mu0[(0, 1)]
        ellipses[i].major = major0[0]
        ellipses[i].minor = minor0[0]
        ellipses[i].angle = angle0[0]
        ellipses[i].area = area0[0]
        isdone[i] = ellipses[i].area <= params.maxshape.area
        for j in range(1, ncomponents):
            ellipse = Ellipse(mu0[(j, 0)], mu0[(j, 1)], minor0[j], major0[j], angle0[j], area0[j])
            ellipses.append(ellipse)
            isdone = num.append(isdone, ellipse.area <= params.maxshape.area)
            L[(r[(idx == j)], c[(idx == j)])] = len(ellipses)

        num.concatenate((isdone, num.zeros(ncomponents, dtype=bool)))


def fixlarge(ellipses, L, dfore):
    isdone = num.zeros(len(ellipses), dtype=bool)
    for i in range(len(ellipses)):
        isdone[i] = ellipses[i].area <= params.maxshape.area

    while True:
        i = num.where(isdone == False)[0]
        if i.size == 0:
            break
        i = i[0]
        trysplit(ellipses, i, isdone, L, dfore)


def trymergedisplay(ellipses, issmall, i, L, dfore):
    closeinds = findclosecenters(ellipses, i)
    if len(closeinds) == 0:
        return (
         False, None)
    mergepenalty = ones(len(closeinds))
    mergepenalty[:] = params.maxpenaltymerge
    ellipsesmerge = []
    for j in range(len(closeinds)):
        (mergepenalty[j], newellipse) = computemergepenalty(ellipses, i, closeinds[j], L, dfore)
        ellipsesmerge.append(newellipse)

    bestjmerge = num.argmin(mergepenalty)
    minmergepenalty = mergepenalty[bestjmerge]
    if minmergepenalty > params.maxpenaltymerge:
        return (
         False, None)
    canmergewith = closeinds[bestjmerge]
    mergeellipses(ellipses, i, canmergewith, ellipsesmerge[bestjmerge], issmall, L)
    return (True, canmergewith)


def fixsmalldisplay(ellipses, L, dfore):
    issmall = num.zeros(len(ellipses), dtype=bool)
    for i in range(len(ellipses)):
        issmall[i] = ellipses[i].area < params.minshape.area

    retissmall = issmall.copy()
    retdidlowerthresh = num.zeros(len(ellipses), dtype=bool)
    retdidmerge = []
    for i in range(len(ellipses)):
        retdidmerge.append(set([i]))

    retdiddelete = num.zeros(len(ellipses), dtype=bool)
    while num.any(issmall):
        i = num.where(issmall)[0]
        i = i[0]
        didmerge = False
        (issmall[i], ellipselowerthresh) = trylowerthresh(ellipses, i, L, dfore)
        if retissmall[i] == True and issmall[i] == False:
            ellipses[i] = ellipselowerthresh
            retdidlowerthresh[i] = True
        if issmall[i]:
            (didmerge, mergedwith) = trymergedisplay(ellipses, issmall, i, L, dfore)
            if didmerge:
                retdidmerge[i] = retdidmerge[i] | retdidmerge[mergedwith]
        if issmall[i] and didmerge == False:
            ellipses[i] = ellipselowerthresh.copy()
            trydelete(ellipses, i, issmall)
            if ellipses[i].area == 0:
                retdiddelete[i] = True
            issmall[i] = False

    deleteellipses(ellipses, L)
    return (
     retissmall, retdidlowerthresh, retdidmerge, retdiddelete)


def fixlargedisplay(ellipses, L, dfore):
    isdone = num.zeros(len(ellipses), dtype=bool)
    for i in range(len(ellipses)):
        isdone[i] = ellipses[i].area <= params.maxshape.area

    retislarge = isdone.copy()
    retdidsplit = []
    for i in range(len(ellipses)):
        retdidsplit.append(set([i]))

    while True:
        i = num.where(isdone == False)[0]
        if i.size == 0:
            break
        i = i[0]
        oldlen = len(ellipses)
        trysplit(ellipses, i, isdone, L, dfore)
        newlen = len(ellipses)
        newellipses = set(range(oldlen, newlen))
        if i >= len(retislarge):
            for j in range(len(retislarge)):
                if i in retdidsplit[j]:
                    break

        else:
            j = i
        retdidsplit[j] = retdidsplit[j] | newellipses

    return (
     retislarge, retdidsplit)