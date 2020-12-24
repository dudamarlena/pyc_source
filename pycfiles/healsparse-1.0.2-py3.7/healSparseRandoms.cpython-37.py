# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healsparse/healSparseRandoms.py
# Compiled at: 2020-02-20 14:19:15
# Size of source mod 2**32: 4788 bytes
from __future__ import division, absolute_import, print_function
import numpy as np, healpy as hp, copy

def make_uniform_randoms_fast(sparse_map, n_random, nside_randoms=8388608, rng=None):
    """
    Make an array of uniform randoms.

    Parameters
    ----------
    sparse_map: `healsparse.HealSparseMap`
       Sparse map object
    n_random: `int`
       Number of randoms to generate
    nside_randoms: `int`, optional
       Nside for pixel centers to select random points
    rng: `np.random.RandomState`, optional
       Pre-set Random number generator.  Default is None.

    Returns
    -------
    ra_array: `np.array`
       Float array of RAs (degrees)
    dec_array: `np.array`
       Float array of declinations (degrees)
    """
    if rng is None:
        rng = np.random.RandomState()
    valid_pixels = sparse_map.valid_pixels
    ipnest_coarse = rng.choice(valid_pixels, size=n_random, replace=True)
    bit_shift = 2 * int(np.round(np.log(nside_randoms / sparse_map.nside_sparse) / np.log(2)))
    sub_pixels = rng.randint(0, high=(2 ** bit_shift - 1), size=n_random)
    ra_rand, dec_rand = hp.pix2ang(nside_randoms, (np.left_shift(ipnest_coarse, bit_shift) + sub_pixels),
      lonlat=True,
      nest=True)
    return (
     ra_rand, dec_rand)


def make_uniform_randoms(sparse_map, n_random, rng=None):
    """
    Make an array of uniform randoms.

    Parameters
    ----------
    sparse_map: `healsparse.HealSparseMap`
       Sparse map object
    n_random: `int`
       Number of randoms to generate
    rng: `np.random.RandomState`, optional
       Pre-set Random number generator.  Default is None.

    Returns
    -------
    ra_array: `np.array`
       Float array of RAs (degrees)
    dec_array: `np.array`
       Float array of declinations (degrees)
    """
    if rng is None:
        rng = np.random.RandomState()
    r = 1.0
    min_gen = 10000
    max_gen = 1000000
    cov_mask = sparse_map.coverage_mask
    cov_pix, = np.where(cov_mask)
    cov_theta, cov_phi = hp.pix2ang((sparse_map.nside_coverage), cov_pix, nest=True)
    extra_boundary = 2.0 * hp.nside2resol(sparse_map.nside_coverage)
    ra_range = np.clip([np.min(cov_phi - extra_boundary),
     np.max(cov_phi + extra_boundary)], 0.0, 2.0 * np.pi)
    dec_range = np.clip([np.min(np.pi / 2.0 - cov_theta - extra_boundary),
     np.max(np.pi / 2.0 - cov_theta + extra_boundary)], -np.pi / 2.0, np.pi / 2.0)
    rotated = False
    cov_phi_rot = cov_phi + np.pi
    test, = np.where(cov_phi_rot > 2.0 * np.pi)
    cov_phi_rot[test] -= 2.0 * np.pi
    ra_range_rot = np.clip([np.min(cov_phi_rot - extra_boundary),
     np.max(cov_phi_rot + extra_boundary)], 0.0, 2.0 * np.pi)
    if ra_range_rot[1] - ra_range_rot[0] < ra_range[1] - ra_range[0] - 0.1:
        ra_range = ra_range_rot
        rotated = True
    z_range = r * np.sin(dec_range)
    phi_range = ra_range
    ra_rand = np.zeros(n_random)
    dec_rand = np.zeros(n_random)
    n_left = copy.copy(n_random)
    ctr = 0
    while n_left > 0:
        n_gen = np.clip(n_left * 2, min_gen, max_gen)
        z = rng.uniform(low=(z_range[0]), high=(z_range[1]), size=n_gen)
        phi = rng.uniform(low=(phi_range[0]), high=(phi_range[1]), size=n_gen)
        theta = np.arcsin(z / r)
        ra_rand_temp = np.degrees(phi)
        dec_rand_temp = np.degrees(theta)
        if rotated:
            ra_rand_temp -= 180.0
            ra_rand_temp[(ra_rand_temp < 0.0)] += 360.0
        valid, = np.where(sparse_map.get_values_pos(ra_rand_temp, dec_rand_temp, lonlat=True,
          valid_mask=True))
        n_valid = valid.size
        if n_valid > n_left:
            n_valid = n_left
        ra_rand[ctr:ctr + n_valid] = ra_rand_temp[valid[0:n_valid]]
        dec_rand[ctr:ctr + n_valid] = dec_rand_temp[valid[0:n_valid]]
        ctr += n_valid
        n_left -= n_valid

    return (ra_rand, dec_rand)