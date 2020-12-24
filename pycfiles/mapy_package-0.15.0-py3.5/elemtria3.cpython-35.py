# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\elements\elemtria\elemtria3.py
# Compiled at: 2017-04-20 23:25:12
# Size of source mod 2**32: 276 bytes
from mapy.model.elements.elem2d import Elem2D
from mapy.reader import user_setattr

class ElemTria3(Elem2D):

    def __init__(self, inputs):
        Elem2D.__init__(self)
        self = user_setattr(self, inputs)

    def rebuild(self):
        Elem2D.rebuild(self)