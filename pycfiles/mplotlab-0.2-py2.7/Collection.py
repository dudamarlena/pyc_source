# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\models\Collection.py
# Compiled at: 2016-02-07 09:44:32
from AbcModel import AbcModel
from Variable import Variable
from AbcType import COLOR, STRING, BOOL

class Collection(AbcModel):
    attributeInfos = list(AbcModel.attributeInfos)
    attributeInfos.extend([
     (
      'X', (Variable, Variable, Variable(), 'var X')),
     (
      'Y', (Variable, Variable, Variable(), 'var Y')),
     (
      'color', (str, COLOR, 'blue', 'artist color')),
     (
      'linestyle', (str, STRING, '-', 'linestyle')),
     (
      'animation', (bool, BOOL, False, 'enable artist animation'))])