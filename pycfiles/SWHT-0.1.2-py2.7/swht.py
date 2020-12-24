# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/SWHT/swht.py
# Compiled at: 2017-08-08 14:46:57
"""
Functions for producing SWHT-based dirty images
Based on T. Carozzi MATLAB code
"""
import numpy as np, scipy.special, math, time, sys, healpy as hp, Ylm, util
cc = 299792458.0

def sphBj(l, r, autos=True):
    """spherical Bessel function of first kind
    l: int, order
    r: positive float array, radius
    autos: if True, set the 0-baseline (i.e. r=0/auto-correlations) to have a scale factor of 1, else make 0"""
    jl = np.sqrt(np.pi / (2.0 * r)) * scipy.special.jv(l + 0.5, r)
    rorgInd = np.argwhere(r == 0.0)
    if len(rorgInd) > 0:
        if l == 0.0 and autos:
            jl[rorgInd] = 1.0
        else:
            jl[rorgInd] = 0.0
    return jl


def spharm(l, m, theta, phi):
    """Spherical harmonic function with l,m polar and azimuthal quantal numbers
    theta: float array, polar/elevation angle, range (-pi/2, pi/2)
    phi: float array, azimith angle, range (0, 2pi)
    l: positive int
    m: int, -l <= m <= l
    this is just a wrapper scipy.special.sph_harm, we use the convention that phi is the azimuthal angle [0, 2pi], theta is the colatitude/elevation angle [0,pi] where 0 is the norht pole and pi is the south pole
    """
    if m < 0:
        return (-1.0) ** m * np.conjugate(scipy.special.sph_harm(n=l, m=np.abs(m), theta=phi, phi=theta))
    else:
        return scipy.special.sph_harm(n=l, m=m, theta=phi, phi=theta)


def computeVislm(lmax, k, r, theta, phi, vis, lmin=0):
    """Compute the spherical wave harmonics visibility coefficients, Eq. 16 of Carozzi 2015
    lmax: positive int, maximum spherical harmonic l number
    lmin: positive int, minimum spherical harmonic l number, usually 0
    k: [N, 1] float array, wave number, observing frequencies/c (1/meters)
    r, theta, phi: [Q, N] float arrays of visibility positions transformed from (u,v,w) positions, r (meters)
    vis: [Q, N] complex array, observed visibilities

    returns: [lmax+1, 2*lmax+1, nfreq] array of coefficients, only partially filled, see for loops in this function
    """
    nsbs = vis.shape[1]
    vislm = np.zeros((lmax + 1, 2 * lmax + 1, nsbs), dtype=complex)
    kr = r * k.flatten()
    print 'L:',
    for l in np.arange(lmax + 1):
        if l < lmin:
            continue
        print l,
        jvVals = np.reshape(sphBj(l, kr.flatten(), autos=False), kr.shape)
        sys.stdout.flush()
        for m in np.arange(-1 * l, l + 1):
            spharmlm = np.conj(Ylm.Ylm(l, m, phi, theta))
            vislm[(l, l + m)] = 2.0 * k.flatten() ** 2.0 / np.pi * np.sum(vis * jvVals * spharmlm, axis=0)

    vislm = np.mean(vislm, axis=2)
    print 'done'
    return vislm


def computeVisSamples(vislm, k, r, theta, phi):
    """The reverse function to computeVislm, compute the visibilities for give set of (r, theta, phi) from vislm coefficients, Eq. 9 pf Carozzi 2015
    vislm: complex array, spherical wave harmonics visibility coefficients computed from computeVislm()
    k: [N, 1] float array, wave number, observing frequencies/c (1/meters)
    r, theta, phi: [Q, N] float arrays of visibility positions transformed from (u,v,w) positions, r (meters)
    returns: vis [Q, N] complex array of visibilities
    """
    vis = np.zeros(r.shape, dtype='complex')
    nsbs = r.shape[1]
    kr = r * k.flatten()
    lmax = vislm.shape[0] - 1
    print 'L:',
    for l in np.arange(lmax + 1):
        print l,
        jvVals = np.reshape(sphBj(l, kr.flatten(), autos=False), kr.shape)
        sys.stdout.flush()
        for m in np.arange(-1 * l, l + 1):
            vis += vislm[(l, l + m)] * jvVals * Ylm.Ylm(l, m, phi, theta)

    return vis


def computeblm(vislm, reverse=False):
    """Compute the spherical wave harmonics brightness coefficients from the spherical wave harmonics visibility coefficients, Eq. 11 of Carozzi 2015
    vislm: [L+1, 2L+1]complex array, spherical wave harmonics visibility coefficients computed from computeVislm()
    reverse: if true, convert vislm from input blm
    """
    lls = np.repeat(np.arange(vislm.shape[0], dtype=float)[np.newaxis].T, 2 * (vislm.shape[0] - 1) + 1, axis=1)
    if reverse:
        blm = vislm * (4.0 * np.pi * complex(-0.0, -1.0) ** lls)
    else:
        blm = vislm / (4.0 * np.pi * complex(-0.0, -1.0) ** lls)
    return blm


def swhtImageCoeffs(vis, uvw, freqs, lmax, lmin=0):
    """Generate brightness coefficients by transforming visibilities with the SWHT
    vis: complex array [Q, F], Q observed visibilities at F frequencies, can be size [Q] if only using 1 frequency
    uvw: float array [Q, 3, F], meters, has a F frequency axis because of the time steps in LOFAR station obsevrations changes uvw with respect to the frequency
    freqs: float array [F, 1] or [F], observing frequencies in Hz
    lmax: positive int, maximum spherical harmonic l number
    lmin: positive int, minimum spherical harmonic l number, usually 0
    """
    start_time = time.time()
    if vis.ndim == 1:
        vis = vis[np.newaxis].T
    if uvw.ndim == 2:
        uvw = uvw.reshape(uvw.shape[0], uvw.shape[1], 1)
    if freqs.ndim == 1:
        freqs = freqs[np.newaxis].T
    k = 2.0 * np.pi * freqs / cc
    r, phi, theta = util.cart2sph(uvw[:, 0], uvw[:, 1], uvw[:, 2])
    if r.ndim == 1:
        r = r[np.newaxis].T
        phi = phi[np.newaxis].T
        theta = theta[np.newaxis].T
    phi = phi - np.pi
    theta = np.pi - theta
    vislm = computeVislm(lmax, k, r, theta, phi, vis, lmin=lmin)
    blm = computeblm(vislm)
    print 'Run time: %f s' % (time.time() - start_time)
    return blm


def iswhtVisibilities(blm, uvw, freqs):
    """Generate visibilities by inverse transforming brightness coefficients with the iSWHT
    blm: [LMAX+1, 2*LMAX + 1] array, brightness coefficients
    uvw: float array [Q, 3, F], meters, has a F frequency axis because of the time steps in LOFAR station obsevrations changes uvw with respect to the frequency
    freqs: float array [F, 1] or [F], observing frequencies in Hz
    """
    start_time = time.time()
    vislm = computeblm(blm, reverse=True)
    if uvw.ndim == 2:
        uvw = uvw.reshape(uvw.shape[0], uvw.shape[1], 1)
    if freqs.ndim == 1:
        freqs = freqs[np.newaxis].T
    k = 2.0 * np.pi * freqs / cc
    r, phi, theta = util.cart2sph(uvw[:, 0], uvw[:, 1], uvw[:, 2])
    if r.ndim == 1:
        r = r[np.newaxis].T
        phi = phi[np.newaxis].T
        theta = theta[np.newaxis].T
    phi = phi - np.pi
    theta = np.pi - theta
    vis = computeVisSamples(vislm, k, r, theta, phi)
    print 'Run time: %f s' % (time.time() - start_time)
    return vis


def make2Dimage(coeffs, res, px=[
 64, 64], phs=[0.0, 0.0]):
    """Make a flat image of a single hemisphere from SWHT image coefficients
    coeffs: SWHT brightness coefficients
    px: [int, int], number of pixels, note these are equivalent to the l,m coordinates in FT imaging
    res: float, resolution of the central pixel in radians
    phs: [float, float], RA and Dec (radians) position at the center of the image
    """
    start_time = time.time()
    lrange = np.linspace(-1.0 * px[0] * res / 2.0, px[0] * res / 2.0, num=px[0], endpoint=True) / (np.pi / 2.0)
    mrange = np.linspace(-1.0 * px[1] * res / 2.0, px[1] * res / 2.0, num=px[1], endpoint=True) / (np.pi / 2.0)
    xx, yy = np.meshgrid(lrange, mrange)
    img = np.zeros(xx.shape, dtype='complex')
    r = np.sqrt(xx ** 2.0 + yy ** 2.0)
    phi = np.arctan2(yy, xx)
    rflat = r.flatten()
    phiflat = phi.flatten()
    maxRcond = r.flatten() > 1
    idx = np.argwhere(maxRcond)
    rflat[idx] = 0.0
    phiflat[idx] = 0.0
    r = np.reshape(rflat, r.shape)
    phi = np.reshape(phiflat, phi.shape)
    thetap = np.arccos(r) - np.pi / 2.0
    phip = np.pi - phi
    X, Y, Z = util.sph2cart(thetap, phip)
    ra = phs[0]
    raRotation = np.array([[np.cos(ra), -1.0 * np.sin(ra), 0.0],
     [
      np.sin(ra), np.cos(ra), 0.0],
     [
      0.0, 0.0, 1.0]])
    dec = np.pi - phs[1]
    print 'dec', dec, 'phs', phs[1]
    decRotation = np.array([[1.0, 0.0, 0.0],
     [
      0.0, np.cos(dec), -1.0 * np.sin(dec)],
     [
      0.0, np.sin(dec), np.cos(dec)]])
    XYZ = np.vstack((X.flatten(), Y.flatten(), Z.flatten()))
    rotMatrix = np.dot(decRotation, raRotation)
    XYZ0 = np.dot(rotMatrix, XYZ)
    r0, phi0, theta0 = util.cart2sph(XYZ0[0, :], XYZ0[1, :], XYZ0[2, :])
    r0 = r0.reshape(thetap.shape)
    phi0 = phi0.reshape(thetap.shape)
    theta0 = theta0.reshape(thetap.shape)
    lmax = coeffs.shape[0]
    print 'L:',
    for l in np.arange(lmax):
        print l,
        sys.stdout.flush()
        for m in np.arange(-1 * l, l + 1):
            img += coeffs[(l, l + m)] * Ylm.Ylm(l, m, phi0, theta0)

    print 'done'
    print 'Run time: %f s' % (time.time() - start_time)
    return np.ma.array(img, mask=maxRcond)


def make3Dimage(coeffs, dim=[
 64, 64]):
    """Make a 3D sphere from SWHT image coefficients
    coeffs: SWHT brightness coefficients
    dim: [int, int] number of steps in theta and phi
    """
    theta, phi = np.meshgrid(np.linspace(0, np.pi, num=dim[0], endpoint=True), np.linspace(0, 2.0 * np.pi, num=dim[1], endpoint=True))
    img = np.zeros(theta.shape, dtype='complex')
    lmax = coeffs.shape[0]
    print 'L:',
    for l in np.arange(lmax):
        print l,
        sys.stdout.flush()
        for m in np.arange(-1 * l, l + 1):
            img += coeffs[(l, l + m)] * Ylm.Ylm(l, m, phi, theta)

    print 'done'
    return (
     img, phi, theta)


def makeHEALPix(coeffs, nside=64):
    """Make a HEALPix map from SWHT image coefficients, comparable to healpy.alm2map()
    coeffs: SWHT brightness coefficients
    nside: int, HEALPix NSIDE
    """
    hpIdx = np.arange(hp.nside2npix(nside))
    hpmap = np.zeros(hp.nside2npix(nside), dtype=complex)
    theta, phi = hp.pix2ang(nside, hpIdx)
    lmax = coeffs.shape[0] - 1
    print 'L:',
    for l in np.arange(lmax + 1):
        print l,
        sys.stdout.flush()
        for m in np.arange(-1 * l, l + 1):
            hpmap += coeffs[(l, l + m)] * Ylm.Ylm(l, m, phi, theta)

    print 'done'
    return hpmap


if __name__ == '__main__':
    print 'Running test cases'
    import matplotlib.pyplot as plt
    jl0 = sphBj(0, np.linspace(0, 50, num=256))
    jl1 = sphBj(1, np.linspace(0, 50, num=256))
    jl2 = sphBj(2, np.linspace(0, 50, num=256))
    theta, phi = np.meshgrid(np.linspace(0, np.pi, 100), np.linspace(0, 2.0 * np.pi, 100))
    l = 1
    m = -1
    Y = spharm(l=l, m=m, theta=theta, phi=phi)
    Yp = 0.5 * np.sqrt(3.0 / (2.0 * np.pi)) * np.sin(theta) * np.exp(phi * complex(0.0, -1.0))
    print np.allclose(Y, Yp, atol=1e-08)
    theta = np.random.rand(100) * np.pi
    theta = theta[np.newaxis].T
    phi = np.random.rand(100) * np.pi * 2.0
    phi = phi[np.newaxis].T
    r = np.random.rand(100) * 60.0
    r = r[np.newaxis].T
    k = np.array([100.0, 110.0, 120.0]) * 1000000.0 / 299792458.0
    k = k[np.newaxis].T
    vis = np.random.rand(300) * 2.0 - 1.0 + complex(0.0, 1.0) * (np.random.rand(300) * 2.0 - 1.0)
    vis = np.reshape(vis, (100, 3))
    lmax = 5
    vislm = computeVislm(lmax, k, r, theta, phi, vis)
    print vislm.shape
    blm = computeblm(vislm)
    print blm.shape
    freqs = np.array([100.0, 110.0, 120.0]) * 1000000.0
    uvw = (np.random.rand(300) * 60.0 - 30.0).reshape(100, 3)
    blm = swhtImageCoeffs(vis, uvw, freqs, lmax)
    print blm.shape
    phi, theta = np.ogrid[0:2 * np.pi:complex(0.0, 10.0), -np.pi / 2:np.pi / 2:complex(0.0, 10.0)]
    print 'l', 'm', 'max|Ylm-sph_harm|'
    for l in np.arange(0, 10):
        for m in np.arange(-l, l + 1):
            a = spharm(l, m, theta, phi)
            b = scipy.special.sph_harm(m=m, n=l, theta=phi, phi=theta)
            print l, m, np.amax(np.abs(a - b))

    print 'Made it through without any errors.'