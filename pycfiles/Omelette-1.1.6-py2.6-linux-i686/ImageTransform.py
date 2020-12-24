# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/ImageTransform.py
# Compiled at: 2007-09-25 20:00:35
import Image

class Transform:

    def __init__(self, data):
        self.data = data

    def getdata(self):
        return (self.method, self.data)


class AffineTransform(Transform):
    method = Image.AFFINE


class ExtentTransform(Transform):
    method = Image.EXTENT


class QuadTransform(Transform):
    method = Image.QUAD


class MeshTransform(Transform):
    method = Image.MESH