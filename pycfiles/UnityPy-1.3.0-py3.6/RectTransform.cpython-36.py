# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\RectTransform.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 145 bytes
from .Transform import Transform

class RectTransform(Transform):

    def __init__(self, reader):
        super().__init__(reader=reader)