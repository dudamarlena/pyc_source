# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\electricpy\constants.py
# Compiled at: 2019-11-18 09:45:32
# Size of source mod 2**32: 3930 bytes
import numpy as _np, cmath as _c
pi = _np.pi
a = _c.rect(1, _np.radians(120))
p = 1e-12
n = 1e-09
u = 1e-06
m = 0.001
k = 1000.0
M = 1000000.0
G = 1000000000.0
u0 = 4 * _np.pi * 1e-07
e0 = 8.8541878128e-12
carson_r = 9.869e-07
De0 = 2160
NAN = float('nan')
VLLcVLN = _c.rect(_np.sqrt(3), _np.radians(30))
ILcIP = _c.rect(_np.sqrt(3), _np.radians(-30))
Aabc = 0.3333333333333333 * _np.array([[1, 1, 1],
 [
  1, a, a ** 2],
 [
  1, a ** 2, a]])
A012 = _np.array([[1, 1, 1],
 [
  1, a ** 2, a],
 [
  1, a, a ** 2]])
Cabc = _np.sqrt(0.6666666666666666) * _np.array([[1, -0.5, -0.5],
 [
  0, _np.sqrt(3) / 2, -_np.sqrt(3) / 2],
 [
  1 / _np.sqrt(2), 1 / _np.sqrt(2), 1 / _np.sqrt(2)]])
Cxyz = _np.array([[2 / _np.sqrt(6), 0, 1 / _np.sqrt(3)],
 [
  -1 / _np.sqrt(6), 1 / _np.sqrt(2), 1 / _np.sqrt(3)],
 [
  -1 / _np.sqrt(6), -1 / _np.sqrt(2), 1 / _np.sqrt(3)]])
_rad = lambda th: _np.radians(th)
Pdq0_im = lambda th: _np.sqrt(0.6666666666666666) * _np.array([[_np.cos(_rad(th)), _np.cos(_rad(th) - 2 * pi / 3), _np.cos(_rad(th) + 2 * pi / 3)],
 [
  -_np.sin(_rad(th)), -_np.sin(_rad(th) - 2 * pi / 3), -_np.sin(_rad(th) + 2 * pi / 3)],
 [
  _np.sqrt(2) / 2, _np.sqrt(2) / 2, _np.sqrt(2) / 2]])
Pabc_im = lambda th: _np.sqrt(0.6666666666666666) * _np.array([[_np.cos(_rad(th)), -_np.sin(_rad(th)), _np.sqrt(2) / 2],
 [
  _np.cos(_rad(th) - 2 * pi / 3), -_np.sin(_rad(th) - 2 * pi / 3), _np.sqrt(2) / 2],
 [
  _np.cos(_rad(th) + 2 * pi / 3), -_np.sin(_rad(th) + 2 * pi / 3), _np.sqrt(2) / 2]])
Pdq0 = 0.6666666666666666 * _np.array([[0, -_np.sqrt(1.5), _np.sqrt(1.5)],
 [
  1, -0.5, -0.5],
 [
  0.5, 0.5, 0.5]])
Pqd0 = 0.6666666666666666 * _np.array([[1, -0.5, -0.5],
 [
  0, -_np.sqrt(1.5), _np.sqrt(1.5)],
 [
  0.5, 0.5, 0.5]])
XFMY0 = _np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
XFMD1 = 1 / _np.sqrt(3) * _np.array([[1, -1, 0], [0, 1, -1], [-1, 0, 1]])
XFMD11 = 1 / _np.sqrt(3) * _np.array([[1, 0, -1], [-1, 1, 0], [0, -1, 1]])
XFM12 = 0.3333333333333333 * _np.array([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]])
e30 = _c.rect(1, _np.radians(30))
en30 = _c.rect(1, _np.radians(-30))
e60 = _c.rect(1, _np.radians(60))
en60 = _c.rect(1, _np.radians(-60))
e90 = _c.rect(1, _np.radians(90))
en90 = _c.rect(1, _np.radians(-90))
e45 = _c.rect(1, _np.radians(45))
en45 = _c.rect(1, _np.radians(-45))