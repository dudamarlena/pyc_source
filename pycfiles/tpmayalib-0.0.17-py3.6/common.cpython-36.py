# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpMayaLib/core/common.py
# Compiled at: 2020-01-16 21:52:40
# Size of source mod 2**32: 560 bytes
"""
Module that contains common definitions for tpMayaLib
"""
from __future__ import print_function, division, absolute_import
PIVOT_ARGS = dict(rp=['rp', 'r', 'rotate', 'rotatePivot', 'pivot'], sp=['scale', 's', 'scalePivot'], local=[
 'l', 'translate'],
  boundingBox=['bb', 'bbCenter'],
  axisBox=['ab'],
  closestPoint=[
 'cpos', 'closest', 'closestPoint'])
SPACE_ARGS = {'object':[
  'os', 'objectSpace', 'o'], 
 'world':['w', 'worldSpace', 'ws'],  'local':['l', 'translate']}