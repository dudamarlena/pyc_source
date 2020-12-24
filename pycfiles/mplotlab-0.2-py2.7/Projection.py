# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\models\Projection.py
# Compiled at: 2016-02-07 09:44:32
from AbcModel import AbcModel, MODELS
from AbcType import FLOAT, STRING, BOOL

class Projection(AbcModel):
    attributeInfos = list(AbcModel.attributeInfos)
    attributeInfos.extend([
     (
      'collections', (list, MODELS, [], 'collections')),
     (
      'xlabel', (str, STRING, '', 'axes xlabel')),
     (
      'ylabel', (str, STRING, '', 'axes ylabel')),
     (
      'autolim', (bool, BOOL, False, "Auto lim axis. Doesn't use x,y min/max")),
     (
      'xmin', (float, FLOAT, 0.0, 'axes xmin')),
     (
      'xmax', (float, FLOAT, 5.0, 'axes xmax')),
     (
      'ymin', (float, FLOAT, 0.0, 'axes ymin')),
     (
      'ymax', (float, FLOAT, 5.0, 'axes ymax'))])