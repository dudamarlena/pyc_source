# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iarot90.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iarot90(img, axis='X'):
    from ia636 import iaffine
    PIVAL = math.pi
    g = 0
    if axis == 'X':
        Trx = array([[cos(PIVAL / 2), -sin(PIVAL / 2), 0, img.shape[1] - 1],
         [
          sin(PIVAL / 2), cos(PIVAL / 2), 0, 0],
         [
          0, 0, 1, 0],
         [
          0, 0, 0, 1]]).astype(float)
        g = iaffine(img, Trx, [img.shape[1], img.shape[0], img.shape[2]])
    elif axis == 'Y':
        Try = array([[cos(PIVAL / 2), 0, sin(PIVAL / 2), 0],
         [
          0, 1, 0, 0],
         [
          -sin(PIVAL / 2), 0, cos(PIVAL / 2), img.shape[0] - 1],
         [
          0, 0, 0, 1]])
        g = iaffine(img, Try, [img.shape[2], img.shape[1], img.shape[0]])
    elif axis == 'Z':
        Trz = array([[1, 0, 0, 0],
         [
          0, cos(PIVAL / 2), -sin(PIVAL / 2), img.shape[2] - 1],
         [
          0, sin(PIVAL / 2), cos(PIVAL / 2), 0],
         [
          0, 0, 0, 1]]).astype(float)
        g = iaffine(img, Trz, [img.shape[0], img.shape[2], img.shape[1]])
    return g