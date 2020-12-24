# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/test.py
# Compiled at: 2008-01-29 20:48:29
import numpy as num
from ellipses import *
from pylab import *
from kcluster import gmm
import scipy.ndimage.measurements as meas

class ShapeParams:

    def __init__(self, major=0, minor=0, area=0, ecc=0):
        self.major = major
        self.minor = minor
        self.area = area
        self.ecc = ecc


class EllipseParams:

    def __init__(self):
        self.maxshape = ShapeParams(55, 25, 1375 * num.pi * 4)
        self.minshape = ShapeParams(15, 5, 75 * num.pi * 4)
        self.minbackthresh = 0.1
        self.maxpenaltymerge = 40
        self.maxareadelete = 5


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
    ellipses[i].center.x = newellipse.center.x
    ellipses[i].center.y = newellipse.center.y
    ellipses[i].major = newellipse.major
    ellipses[i].minor = newellipse.minor
    ellipses[i].angle = newellipse.angle
    ellipses[i].area = newellipse.area


def weightedregionpropsi(BWI, w):
    w = w / sum(w)
    (r, c) = num.where(BWI)
    centerX = sum(c * w)
    centerY = sum(r * w)
    r = r - centerY
    c = c - centerX
    S = num.zeros((2, 2))
    S[(0, 0)] = sum(w * c ** 2)
    S[(1, 1)] = sum(w * r ** 2)
    S[(0, 1)] = sum(w * c * r)
    S[(1, 0)] = S[(0, 1)]
    (sizeH, sizeW, angle) = cov2ell(S)
    if sizeH < 0.125 or num.isnan(sizeH):
        sizeH = 0.125
        sizeW = 0.125
    elif sizeW < 0.125 or num.isnan(sizeW):
        sizeW = 0.125
    area = num.pi * sizeW * sizeH * 4
    return Ellipse(centerX, centerY, sizeW, sizeH, angle, area)


def weightedregionprops(L, ncc, dfore):
    ellipses = EllipseList()
    S = num.zeros((2, 2))
    for i in range(ncc):
        BW = L == i + 1
        ellipse = weightedregionpropsi(BW, dfore[BW])
        ellipses.append(ellipse)

    return ellipses


def getboundingboxbig(ellipse, sz, params):
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


def trylowerthresh(ellipses, i, L, dfore, params):
    (r1, r2, c1, c2) = getboundingboxbig(ellipses[i], L.shape, params)
    dforebox = dfore[r1:r2, c1:c2]
    isforebox = dforebox >= params.minbackthresh
    Lbox = L[r1:r2, c1:c2]
    (Lnewbox, ncc) = meas.label(isforebox)
    inew = getnewlabel(Lnewbox, ncc, Lbox, i)
    tmp = Lbox[(Lnewbox == inew)]
    if num.any(num.logical_and(tmp != 0, tmp != i + 1)):
        return (True, ellipses[i])
    ellipsenew = weightedregionpropsi(Lnewbox == inew, dforebox[(Lnewbox == inew)])
    issmall = ellipsenew.area < params.minshape.area
    if issmall == False:
        print 'new area of ellipse is %f > %f' % (ellipsenew.area, params.minshape.area)
        copyellipse(ellipses, i, ellipsenew)
    return (
     issmall, ellipsenew)


def findclosecenters(ellipses, i, params):
    maxdmergecenter = params.maxshape.major * 4 + ellipses[i].minor * 2
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


def computemergepenalty(ellipses, i, j, L, dfore, params):
    BWmerge = num.logical_or(L == i + 1, L == j + 1)
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
    return (mergepenalty, ellipsemerge)


def mergeellipses(ellipses, i, j, ellipsemerge, issmall, L, params):
    copyellipse(ellipses, i, ellipsemerge)
    ellipses[j].area = 0
    issmall[i] = ellipsemerge.area < params.minshape.area
    issmall[j] = False
    L[L == j + 1] = i + 1


def trymerge(ellipses, issmall, i, L, dfore, params):
    closeinds = findclosecenters(ellipses, i, params)
    if len(closeinds) == 0:
        return False
    mergepenalty = ones(len(closeinds))
    mergepenalty[:] = params.maxpenaltymerge
    ellipsesmerge = EllipseList()
    for j in range(len(closeinds)):
        (mergepenalty[j], newellipse) = computemergepenalty(ellipses, i, closeinds[j], L, dfore, params)
        print 'penalty for merging with ellipse:'
        printellipse(ellipses[closeinds[j]])
        print '= %f' % mergepenalty[j]
        ellipsesmerge.append(newellipse)

    bestjmerge = num.argmin(mergepenalty)
    minmergepenalty = mergepenalty[bestjmerge]
    if minmergepenalty > params.maxpenaltymerge:
        print 'merge penalty too large'
        return False
    canmergewith = closeinds[bestjmerge]
    mergeellipses(ellipses, i, canmergewith, ellipsesmerge[bestjmerge], issmall, L, params)
    print 'merged %d with %d' % (i, canmergewith)
    return True


def trydelete(ellipses, i, issmall, params):
    if ellipses[i].area < params.maxareadelete:
        ellipses[i].area = 0
        issmall[i] = False


def deleteellipses(ellipses):
    i = 0
    while True:
        if i >= len(ellipses):
            break
        if ellipses[i].area == 0:
            ellipses.pop(i)
        else:
            i += 1


def printellipse(ellipse):
    print '[x: %f y: %f a: %f b: %f t: %f A: %f]' % (ellipse.center.x, ellipse.center.y, ellipse.major, ellipse.minor, ellipse.angle, ellipse.area)


def fixsmall(ellipses, L, dfore, params):
    issmall = num.zeros(len(ellipses), dtype=bool)
    for i in range(len(ellipses)):
        issmall[i] = ellipses[i].area < params.minshape.area

    while num.any(issmall):
        i = num.where(issmall)[0]
        i = i[0]
        didmerge = False
        print 'trying to fix ellipse %d: ' % i
        printellipse(ellipses[i])
        (issmall[i], ellipselowerthresh) = trylowerthresh(ellipses, i, L, dfore, params)
        if issmall[i] == False:
            print 'Succeeded by lowering threshold:'
            printellipse(ellipselowerthresh)
        if issmall[i]:
            print 'Could not lower threshold. Trying to merge'
            didmerge = trymerge(ellipses, issmall, i, L, dfore, params)
            print 'After attempting to merge, ellipse is now:'
            printellipse(ellipses[i])
            print 'didmerge = '
            print didmerge
        if issmall[i] and didmerge == False:
            print 'Could not merge. Trying to delete.'
            copyellipse(ellipses, i, ellipselowerthresh)
            trydelete(ellipses, i, issmall, params)
            print 'After deleting, ellipse is:'
            printellipse(ellipses[i])
            issmall[i] = False

    deleteellipses(ellipses)


def normpdfln2x2cov(x, y, S):
    invS = num.linalg.inv(S)
    p = -(x ** 2 * invS[(0, 0)] + y ** 2 * invS[(1, 1)] + 2 * x * y * invS[(0, 1)]) * 0.5
    p -= log(2.0 * num.pi * num.sqrt(S[(0, 0)] * S[(1, 1)] - S[(0, 1)] ** 2))
    return p


def trysplit(ellipses, i, isdone, L, dfore, params):
    (r, c) = num.where(L == i + 1)
    x = num.hstack((c.reshape(c.size, 1), r.reshape(r.size, 1)))
    w = dfore[(L == i + 1)]
    w = w / num.mean(w)
    ndata = r.size
    print 'ndata = %d' % ndata
    S0 = ell2cov(ellipses[i].major, ellipses[i].minor, ellipses[i].angle)
    mu0 = num.array([ellipses[i].center.x, ellipses[i].center.y])
    print 'loglik: '
    print normpdfln2x2cov(c - ellipses[i].center.x, r - ellipses[i].center.y, S0)
    loglik = num.sum(w * normpdfln2x2cov(c - ellipses[i].center.x, r - ellipses[i].center.y, S0))
    BIC0 = -2 * loglik + num.log(ndata) * 5 * 1
    print 'BIC0 = %f' % BIC0
    ncomponents = 2
    while True:
        (mu, S, priors, gamma, negloglik) = gmm(x, ncomponents, weights=w)
        print 'for ncomponents = %d:' % ncomponents
        print 'mu = '
        print mu
        print 'S = '
        for j in range(ncomponents):
            print S[:, :, j]

        print 'priors = '
        print priors
        print 'negloglik = %f' % negloglik
        BIC = 2 * negloglik + num.log(ndata) * 5 * ncomponents
        if BIC >= BIC0:
            break
        ncomponents += 1
        mu0 = mu
        S0 = S
        gamma0 = gamma
        BIC0 = BIC

    ncomponents -= 1
    if ncomponents == 1:
        isdone[i] = True
    else:
        idx = num.argmax(gamma0, axis=1)
        ellipses[i].center.x = mu0[(0, 0)]
        ellipses[i].center.y = mu0[(0, 1)]
        (ellipses[i].major, ellipses[i].minor, ellipses[i].angle) = cov2ell(S0[:, :, 0])
        for j in range(1, ncomponents):
            (a, b, angle) = cov2ell(S0[:, :, j])
            area = a * b * angle * 4
            ellipse = Ellipse(mu[(j, 0)], mu[(j, 1)], b, a, angle, area)
            ellipses.append(ellipse)
            L[(r[(idx == j)], c[(idx == j)])] = len(ellipses)

        isdone.append(num.zeros(ncomponents - 1, dtype=bool))


def fixlarge(ellipses, L, dfore, params):
    isdone = num.zeros(len(ellipses), dtype=bool)
    for i in range(len(ellipses)):
        isdone[i] = ellipses[i].area <= params.maxshape.area

    while True:
        i = num.where(isdone)[0]
        if i.size == 0:
            break
        i = i[0]
        trysplit(ellipses, i, isdone, L, dfore, params)


params = EllipseParams()
ellipse1 = Ellipse(100, 100, 20, 50, num.pi / 3.0)
ellipse2 = Ellipse(200, 120, 20, 50, num.pi / 6.0)
bounds = num.array([0, 200, 0, 300])
BW1 = ellipsepixels(ellipse1, bounds)
BW2 = ellipsepixels(ellipse2, bounds)
BW = num.logical_or(BW1, BW2)
dfore = num.double(BW)
L = num.uint16(BW)
ncc = num.max(L)
ellipses = weightedregionprops(L, ncc, dfore)
isdone = num.zeros(len(ellipses), dtype=bool)
trysplit(ellipses, 0, isdone, L, dfore, params)
im = imshow(BW, cmap=cm.gray)
for i in range(len(ellipses)):
    h = drawellipse(ellipses[i], format='w', params={'linewidth': 2})

show()