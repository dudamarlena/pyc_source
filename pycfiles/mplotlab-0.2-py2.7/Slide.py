# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\models\Slide.py
# Compiled at: 2016-02-07 09:44:32
from AbcModel import AbcModel, MODELS
from AbcType import STRING

class Slide(AbcModel):
    attributeInfos = list(AbcModel.attributeInfos)
    attributeInfos.extend([
     (
      'title', (str, STRING, '', 'figure title')),
     (
      'projections', (list, MODELS, [], 'projections'))])