# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/color/color_space.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 6072 bytes
from __future__ import division
import numpy as np
from ..ext.six import string_types

def _check_color_dim(val):
    """Ensure val is Nx(n_col), usually Nx3"""
    val = np.atleast_2d(val)
    if val.shape[1] not in (3, 4):
        raise RuntimeError('Value must have second dimension of size 3 or 4')
    return (
     val, val.shape[1])


def _hex_to_rgba(hexs):
    """Convert hex to rgba, permitting alpha values in hex"""
    hexs = np.atleast_1d(np.array(hexs, '|U9'))
    out = np.ones((len(hexs), 4), np.float32)
    for hi, h in enumerate(hexs):
        assert isinstance(h, string_types)
        off = 1 if h[0] == '#' else 0
        assert len(h) in (6 + off, 8 + off)
        e = (len(h) - off) // 2
        out[hi, :e] = [int(h[i:i + 2], 16) / 255.0 for i in range(off, len(h), 2)]

    return out


def _rgb_to_hex(rgbs):
    """Convert rgb to hex triplet"""
    rgbs, n_dim = _check_color_dim(rgbs)
    return np.array(['#%02x%02x%02x' % tuple((255 * rgb[:3]).astype(np.uint8)) for rgb in rgbs], '|U7')


def _rgb_to_hsv(rgbs):
    """Convert Nx3 or Nx4 rgb to hsv"""
    rgbs, n_dim = _check_color_dim(rgbs)
    hsvs = list()
    for rgb in rgbs:
        rgb = rgb[:3]
        idx = np.argmax(rgb)
        val = rgb[idx]
        c = val - np.min(rgb)
        if c == 0:
            hue = 0
            sat = 0
        else:
            if idx == 0:
                hue = (rgb[1] - rgb[2]) / c % 6
            else:
                if idx == 1:
                    hue = (rgb[2] - rgb[0]) / c + 2
                else:
                    hue = (rgb[0] - rgb[1]) / c + 4
                hue *= 60
                sat = c / val
        hsv = [
         hue, sat, val]
        hsvs.append(hsv)

    hsvs = np.array(hsvs, dtype=np.float32)
    if n_dim == 4:
        hsvs = np.concatenate((hsvs, rgbs[:, 3]), axis=1)
    return hsvs


def _hsv_to_rgb(hsvs):
    """Convert Nx3 or Nx4 hsv to rgb"""
    hsvs, n_dim = _check_color_dim(hsvs)
    rgbs = list()
    for hsv in hsvs:
        c = hsv[1] * hsv[2]
        m = hsv[2] - c
        hp = hsv[0] / 60
        x = c * (1 - abs(hp % 2 - 1))
        if 0 <= hp < 1:
            r, g, b = c, x, 0
        else:
            if hp < 2:
                r, g, b = x, c, 0
            else:
                if hp < 3:
                    r, g, b = 0, c, x
                else:
                    if hp < 4:
                        r, g, b = 0, x, c
                    else:
                        if hp < 5:
                            r, g, b = x, 0, c
                        else:
                            r, g, b = c, 0, x
        rgb = [
         r + m, g + m, b + m]
        rgbs.append(rgb)

    rgbs = np.array(rgbs, dtype=np.float32)
    if n_dim == 4:
        rgbs = np.concatenate((rgbs, hsvs[:, 3]), axis=1)
    return rgbs


_rgb2xyz_norm = np.array([[0.43395276, 0.212671, 0.01775791],
 [
  0.37621941, 0.71516, 0.10947652],
 [
  0.18982783, 0.072169, 0.87276557]])
_xyz2rgb_norm = np.array([[3.07993271, -1.53715, -0.54278198],
 [
  -0.92123518, 1.875992, 0.04524426],
 [
  0.05289098, -0.204043, 1.15115158]])

def _rgb_to_lab(rgbs):
    rgbs, n_dim = _check_color_dim(rgbs)
    xyz = rgbs[:, :3].copy()
    over = xyz > 0.04045
    xyz[over] = ((xyz[over] + 0.055) / 1.055) ** 2.4
    xyz[(~over)] /= 12.92
    xyz = np.dot(xyz, _rgb2xyz_norm)
    over = xyz > 0.008856
    xyz[over] = xyz[over] ** 0.3333333333333333
    xyz[~over] = 7.787 * xyz[(~over)] + 0.13793103448275862
    L = 116.0 * xyz[:, 1] - 16
    a = 500 * (xyz[:, 0] - xyz[:, 1])
    b = 200 * (xyz[:, 1] - xyz[:, 2])
    labs = [L, a, b]
    if n_dim == 4:
        labs.append(np.atleast1d(rgbs[:, 3]))
    labs = np.array(labs, order='F').T
    return labs


def _lab_to_rgb(labs):
    """Convert Nx3 or Nx4 lab to rgb"""
    labs, n_dim = _check_color_dim(labs)
    y = (labs[:, 0] + 16.0) / 116.0
    x = labs[:, 1] / 500.0 + y
    z = y - labs[:, 2] / 200.0
    xyz = np.concatenate(([x], [y], [z]))
    over = xyz > 0.2068966
    xyz[over] = xyz[over] ** 3.0
    xyz[~over] = (xyz[(~over)] - 0.13793103448275862) / 7.787
    rgbs = np.dot(_xyz2rgb_norm, xyz).T
    over = rgbs > 0.0031308
    rgbs[over] = 1.055 * rgbs[over] ** 0.4166666666666667 - 0.055
    rgbs[(~over)] *= 12.92
    if n_dim == 4:
        rgbs = np.concatenate((rgbs, labs[:, 3]), axis=1)
    rgbs = np.clip(rgbs, 0.0, 1.0)
    return rgbs