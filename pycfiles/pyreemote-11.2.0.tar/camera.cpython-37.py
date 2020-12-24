# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PyreeEngine/camera.py
# Compiled at: 2018-11-17 16:39:43
# Size of source mod 2**32: 2423 bytes
import numpy as np, math
from PyreeEngine.util import Vec3

class Camera:

    def __init__(self) -> None:
        self.projectionMatrix = np.identity(4)
        self.viewMatrix = None
        self.pos = Vec3()
        self.lookAt(np.array([0, 0, 0], np.float32), np.array([0, 0, -1], np.float32))

    def lookAt(self, eye: np.array, target: np.array, up: np.array=np.array([0, 1, 0], np.float32)) -> None:
        forward = target - eye
        forward /= np.linalg.norm(forward)
        up /= np.linalg.norm(up)
        side = np.cross(forward, up)
        up = np.cross(side, forward)
        orientMat = np.transpose(np.matrix([[side[0], up[0], -forward[0], 0],
         [
          side[1], up[1], -forward[1], 0],
         [
          side[2], up[2], -forward[2], 0],
         [
          0, 0, 0, 1]], np.float32))
        translMat = np.matrix([[1, 0, 0, -eye[0]],
         [
          0, 1, 0, -eye[1]],
         [
          0, 0, 1, -eye[2]],
         [
          0, 0, 0, 1]], np.float32)
        self.viewMatrix = orientMat * translMat


class PerspectiveCamera(Camera):

    def __init__(self):
        super(PerspectiveCamera, self).__init__()
        self.setPerspective(60, 1.3333333333333333, 0.01, 100.0)

    def setPerspective(self, fovY, aspect, nearZ, farZ) -> None:
        s = 1.0 / math.tan(math.radians(fovY) / 2.0)
        sx, sy = s / aspect, s
        zz = (farZ + nearZ) / (nearZ - farZ)
        zw = 2 * farZ * nearZ / (nearZ - farZ)
        self.projectionMatrix = np.matrix([[sx, 0, 0, 0],
         [
          0, sy, 0, 0],
         [
          0, 0, zz, zw],
         [
          0, 0, -1, 0]])


class OrthoCamera(Camera):

    def __init__(self):
        super(OrthoCamera, self).__init__()
        self.setOrtho(1, 1.3333333333333333, 0.01, 100.0)

    def setOrtho(self, sizeY, aspect, nearZ, farZ):
        t, b = sizeY / 2, -sizeY / 2
        r, l = t * aspect, b * aspect
        self.projectionMatrix = np.matrix([[2 / (r - l), 0, 0, -(r + l) / (r - l)],
         [
          0, 2 / (t - b), 0, -(t + b) / (t - b)],
         [
          0, 0, -2 / (farZ - nearZ), -(farZ + nearZ) / (farZ - nearZ)],
         [
          0, 0, 0, 1]])