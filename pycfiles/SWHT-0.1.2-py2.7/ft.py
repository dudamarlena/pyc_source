# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/SWHT/ft.py
# Compiled at: 2017-08-08 14:46:57
"""
Fourier Transform Functions

functions phsCenterSrc, eq2top_m, get_baseline, gen_uvw, xyz2uvw are taken from AIPY (https://github.com/AaronParsons/aipy), used to compute (U,V,W) from ITRF (X,Y,Z)
"""
import numpy as np, ephem, sys, os, struct, time

def phsCenterSrc(obs, t):
    """return an ephem FixedBody source based on the time offset from the obs"""
    src = ephem.FixedBody()
    t0 = obs.date
    obs.date = t
    src._ra = obs.sidereal_time()
    src._dec = obs.lat
    obs.date = t0
    return src


def eq2top_m(ha, dec):
    """Return the 3x3 matrix converting equatorial coordinates to topocentric
    at the given hour angle (ha) and declination (dec)."""
    sin_H, cos_H = np.sin(ha), np.cos(ha)
    sin_d, cos_d = np.sin(dec), np.cos(dec)
    zero = np.zeros_like(ha)
    map = np.array([[sin_H, cos_H, zero],
     [
      -sin_d * cos_H, sin_d * sin_H, cos_d],
     [
      cos_d * cos_H, -cos_d * sin_H, sin_d]])
    if len(map.shape) == 3:
        map = map.transpose([2, 0, 1])
    return map


def get_baseline(i, j, src, obs):
    """Return the baseline corresponding to i,j"""
    bl = j - i
    try:
        if src.alt < 0:
            raise PointingError('Phase center below horizon')
        m = src.map
    except AttributeError:
        ra, dec = src._ra, src._dec
        m = eq2top_m(ra - obs.sidereal_time(), dec)

    return np.dot(m, bl).transpose()


def gen_uvw(i, j, src, obs, f):
    """Compute uvw coordinates of baseline relative to provided FixedBody"""
    x, y, z = get_baseline(i, j, src, obs)
    afreqs = np.reshape(f, (1, f.size))
    afreqs = afreqs / ephem.c
    if len(x.shape) == 0:
        return np.array([x * afreqs, y * afreqs, z * afreqs]).T
    x.shape += (1, )
    y.shape += (1, )
    z.shape += (1, )
    return np.array([np.dot(x, afreqs), np.dot(y, afreqs), np.dot(z, afreqs)]).T


def xyz2uvw(xyz, src, obs, f):
    """Return an array of UVW values"""
    uvw = np.zeros((f.shape[0], xyz.shape[0], xyz.shape[0], 3))
    for i in range(xyz.shape[0]):
        for j in range(xyz.shape[0]):
            if i == j:
                continue
            uvw[:, i, j, :] = gen_uvw(xyz[i], xyz[j], src, obs, f)[:, 0, :]

    return uvw


def dft2(d, l, m, u, v, psf=False):
    """compute the 2d DFT for position (m,l) based on (d,uvw)"""
    if psf:
        return np.sum(np.exp(2.0 * np.pi * complex(0.0, 1.0) * (u * l + v * m))) / u.size
    else:
        return np.sum(d * np.exp(2.0 * np.pi * complex(0.0, 1.0) * (u * l + v * m))) / u.size


def dftImage(d, uvw, px, res, mask=False, rescale=False, stokes=False):
    """return a DFT image
    d: complex visibilities [F, Q] F frequency subbands, Q samples
    uvw: visibility sampling in units of wavelengths [Q, 3]
    px: [int, int], number of pixels in image
    res: float, resolution of central pixel in radians
    rescale: account for missing np.sqrt(1-l^2-m^2) in flat-field approximation
    """
    if stokes:
        im = np.zeros((px[0], px[1], 4), dtype=complex)
    else:
        im = np.zeros((px[0], px[1]), dtype=complex)
    maskIm = np.zeros((px[0], px[1]), dtype=bool)
    mid_m = int(px[0] / 2.0)
    mid_l = int(px[1] / 2.0)
    u = np.array(uvw[:, 0])
    v = np.array(uvw[:, 1])
    w = np.array(uvw[:, 2])
    lrange = np.linspace(-1.0 * px[0] * res / 2.0, px[0] * res / 2.0, num=px[0], endpoint=True) / (np.pi / 2.0)
    mrange = np.linspace(-1.0 * px[1] * res / 2.0, px[1] * res / 2.0, num=px[1], endpoint=True) / (np.pi / 2.0)
    start_time = time.time()
    for mid, m in enumerate(mrange):
        for lid, l in enumerate(lrange):
            if rescale:
                scale = np.sqrt(1.0 - l ** 2.0 - m ** 2.0)
            else:
                scale = 1.0
            if stokes:
                im[(lid, mid, 0)] = dft2(d[0], l, m, u, v) * scale
                im[(lid, mid, 1)] = dft2(d[1], l, m, u, v) * scale
                im[(lid, mid, 2)] = dft2(d[2], l, m, u, v) * scale
                im[(lid, mid, 3)] = dft2(d[3], l, m, u, v) * scale
            else:
                im[(lid, mid)] = dft2(d, m, l, u, v) * scale
            if mask:
                rad = (m ** 2 + l ** 2) ** 0.5
                if rad > 1.0:
                    maskIm[(lid, mid)] = True

    print time.time() - start_time
    im = np.flipud(np.fliplr(im))
    maskIm = np.flipud(np.fliplr(maskIm))
    if mask:
        return (im, maskIm)
    else:
        return im


def fftImage(d, uvw, px, res, mask=False, conv='fast', wgt='natural'):
    """Grid visibilities and perform an FFT to return an image
    d: complex visibilities
    uvw: visibility sampling in units of wavelengths
    px: [int, int], number of pixels in image
    res: float, resolution of central pixel in radians
    """
    start_time = time.time()
    im = np.zeros((px[0], px[1]), dtype=complex)
    maskIm = np.zeros((px[0], px[1]), dtype=bool)
    mid_m = int(px[0] / 2.0)
    mid_l = int(px[1] / 2.0)
    u = np.array(uvw[:, 0])
    v = np.array(uvw[:, 1])
    w = np.array(uvw[:, 2])
    gridVis = np.zeros((px[0], px[1]), dtype=complex)
    gridWgt = np.ones((px[0], px[1]), dtype=float)
    deltau = np.pi / 2.0 * 1.0 / (px[0] * res)
    deltav = np.pi / 2.0 * 1.0 / (px[1] * res)
    if conv.startswith('fast'):
        for did, dd in enumerate(d):
            uu = int(u[did] / deltau)
            vv = int(v[did] / deltav)
            gridVis[((uu + px[0] / 2) % px[0], (vv + px[1] / 2) % px[1])] += dd

    else:
        gridUV = np.mgrid[-0.5 * px[0] * deltau:0.5 * px[0] * deltau:deltau, -0.5 * px[1] * deltav:0.5 * px[1] * deltav:deltav]
        if conv.startswith('rect'):
            convFunc = convRect(deltau, deltav)
            truncDist = deltau / 2.0
        if conv.startswith('gauss'):
            convFunc = convGauss(deltau / 2.0, deltav / 2.0)
            truncDist = deltau * 5.0
        if conv.startswith('prolate'):
            convFunc = convProlate(deltau, deltav)
            truncDist = deltau
        for uid in range(px[0]):
            for vid in range(px[1]):
                ucentre, vcentre = gridUV[:, uid, vid]
                udiff = u - ucentre
                vdiff = v - vcentre
                idx = np.argwhere(np.sqrt(udiff ** 2.0 + vdiff ** 2.0) < truncDist)
                if idx.size > 0:
                    gridWgt[(uid, vid)] = np.sum(convFunc(udiff[idx], vdiff[idx]))
                    gridVis[(uid, vid)] = np.sum(convFunc(udiff[idx], vdiff[idx]) * d[idx])

    if wgt.startswith('uni'):
        gridVis /= gridWgt
    gridVis = np.fft.ifftshift(gridVis)
    im = np.fft.ifftshift(np.fft.ifft2(gridVis))
    im = np.fliplr(np.rot90(im))
    print time.time() - start_time
    if mask:
        return (im, maskIm)
    else:
        return im


def convGauss(ures, vres, alpha=1.0):
    """Return a Gaussian convolution function
    ures,vres: distance from centre to half power point in uv distance
    alpha: scaling factor"""
    return lambda uu, vv: (1.0 / (alpha * np.sqrt(ures * vres * np.pi))) ** 2.0 * np.exp(-1.0 * (uu / (alpha * ures)) ** 2.0) * np.exp(-1.0 * (vv / (alpha * vres)) ** 2.0)


def convRect(ures, vres):
    """Return a boxcar/rectangle convolution function"""
    return lambda uu, vv: np.ones_like(uu)


def convProlate(ures, vres, aa=1.0, cc=1.0):
    """Return a prolate spheroid function which returns the function z(uu, vv) = sqrt( cc**2. * ( 1. - (((uu*ures)**2. + (vv*vres)**2.)/aa**2.))), c > a for a prolate function"""
    return lambda uu, vv: np.sqrt(cc ** 2.0 * (1.0 - ((uu / ures) ** 2.0 + (vv / vres) ** 2.0) / aa ** 2.0))


if __name__ == '__main__':
    print 'Running test cases'
    print 'Made it through without any errors.'