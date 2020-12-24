# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/models/numba/ma_uniform_nb.py
# Compiled at: 2020-03-22 18:42:45
# Size of source mod 2**32: 6390 bytes
from numba import njit, prange
from numpy import pi, sqrt, arccos, abs, zeros_like, sign, sin, cos, abs, atleast_2d, zeros, atleast_1d, isnan, inf, nan
from orbits.orbits_py import z_ip_s
TWO_PI = 2.0 * pi
HALF_PI = 0.5 * pi
FOUR_PI = 4.0 * pi
INV_PI = 1 / pi

@njit(cache=False, fastmath=True)
def uniform_z_v(zs, k):
    flux = zeros_like(zs)
    if abs(k - 0.5) < 0.001:
        k = 0.5
    for i in range(len(zs)):
        z = zs[i]
        if not z < 0.0:
            if z > 1.0 + k:
                flux[i] = 1.0
        elif k > 1.0:
            if z < k - 1.0:
                flux[i] = 0.0
        if z > abs(1.0 - k):
            if z < 1.0 + k:
                kap1 = arccos(min((1.0 - k * k + z * z) / 2.0 / z, 1.0))
                kap0 = arccos(min((k * k + z * z - 1.0) / 2.0 / k / z, 1.0))
                lambdae = k * k * kap0 + kap1
                lambdae = (lambdae - 0.5 * sqrt(max(4.0 * z * z - (1.0 + z * z - k * k) ** 2, 0.0))) / pi
                flux[i] = 1.0 - lambdae
        if z < 1.0 - k:
            flux[i] = 1.0 - k * k

    return flux


@njit(fastmath=True)
def uniform_z_s(z, k):
    if abs(k - 0.5) < 0.001:
        k = 0.5
    if z < 0.0 or z > 1.0 + k:
        flux = 1.0
    else:
        if k > 1.0 and z < k - 1.0:
            flux = 0.0
        else:
            if z > abs(1.0 - k) and z < 1.0 + k:
                kap1 = arccos(min((1.0 - k * k + z * z) / 2.0 / z, 1.0))
                kap0 = arccos(min((k * k + z * z - 1.0) / 2.0 / k / z, 1.0))
                lambdae = k * k * kap0 + kap1
                lambdae = (lambdae - 0.5 * sqrt(max(4.0 * z * z - (1.0 + z * z - k * k) ** 2, 0.0))) / pi
                flux = 1.0 - lambdae
            else:
                if z < 1.0 - k:
                    flux = 1.0 - k * k
                return flux


@njit(parallel=True, fastmath=True)
def uniform_model_v(t, k, t0, p, a, i, e, w, lcids, pbids, nsamples, exptimes, es, ms, tae):
    t0, p, a, i, e, w = (atleast_1d(t0), atleast_1d(p), atleast_1d(a), atleast_1d(i), atleast_1d(e), atleast_1d(w))
    k = atleast_2d(k)
    npv = k.shape[0]
    npt = t.size
    flux = zeros((npv, npt))
    for j in prange(npt):
        for ipv in range(npv):
            ilc = lcids[j]
            ipb = pbids[ilc]
            if k.shape[1] == 1:
                _k = k[(ipv, 0)]
            else:
                _k = k[(ipv, ipb)]
            for isample in range(1, nsamples[ilc] + 1):
                time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)
                z = z_ip_s(t[j] + time_offset, t0[ipv], p[ipv], a[ipv], i[ipv], e[ipv], w[ipv], es, ms, tae)
                if z > 1.0 + _k:
                    flux[(ipv, j)] += 1.0
                else:
                    flux[(ipv, j)] += uniform_z_s(z, _k)

            flux[(ipv, j)] /= nsamples[ilc]

    return flux


@njit(parallel=True, fastmath=True)
def uniform_model_s(t, k, t0, p, a, i, e, w, lcids, pbids, nsamples, exptimes, es, ms, tae):
    k = atleast_1d(k)
    npt = t.size
    flux = zeros(npt)
    for j in prange(npt):
        ilc = lcids[j]
        ipb = pbids[ilc]
        _k = k[0] if k.size == 1 else k[ipb]
        for isample in range(1, nsamples[ilc] + 1):
            time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)
            z = z_ip_s(t[j] + time_offset, t0, p, a, i, e, w, es, ms, tae)
            if z > 1.0 + _k:
                flux[j] += 1.0
            else:
                flux[j] += uniform_z_s(z, _k)

        flux[j] /= nsamples[ilc]

    return flux


@njit(parallel=True, fastmath=True)
def uniform_model_pv(t, pvp, lcids, pbids, nsamples, exptimes, es, ms, tae):
    pvp = atleast_2d(pvp)
    npv = pvp.shape[0]
    npt = t.size
    nk = pvp.shape[1] - 6
    flux = zeros((npv, npt))
    for j in prange(npt):
        for ipv in range(npv):
            t0, p, a, i, e, w = pvp[ipv, nk:]
            ilc = lcids[j]
            ipb = pbids[ilc]
            if nk == 1:
                k = pvp[(ipv, 0)]
            else:
                if ipb < nk:
                    k = pvp[(ipv, ipb)]
                else:
                    k = nan
            for isample in range(1, nsamples[ilc] + 1):
                time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)
                z = z_ip_s(t[j] + time_offset, t0, p, a, i, e, w, es, ms, tae)
                if z > 1.0 + k:
                    flux[(ipv, j)] += 1.0
                else:
                    flux[(ipv, j)] += uniform_z_s(z, k)

            flux[(ipv, j)] /= nsamples[ilc]

    return flux