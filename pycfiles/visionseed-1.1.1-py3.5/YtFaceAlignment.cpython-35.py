# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/visionseed/YtFaceAlignment.py
# Compiled at: 2019-07-24 01:04:26
# Size of source mod 2**32: 1840 bytes
from .YtMsg_pb2 import *
import math

class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Point(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Point(self.x - o.x, self.y - o.y)

    def __truediv__(self, o):
        return Point(self.x / o, self.y / o)

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


class YtFaceShape:

    def __init__(self, pose):
        self.leftEyebrow = [
         None] * 8
        self.rightEyebrow = [None] * 8
        self.leftEye = [None] * 8
        self.rightEye = [None] * 8
        self.nose = [None] * 13
        self.mouth = [None] * 22
        self.faceProfile = [None] * 21
        self.pupil = [None] * 2
        idx = 0
        for i in range(len(self.leftEyebrow)):
            self.leftEyebrow[i] = Point(pose.x[idx], pose.y[idx])
            idx += 1

        for i in range(len(self.rightEyebrow)):
            self.rightEyebrow[i] = Point(pose.x[idx], pose.y[idx])
            idx += 1

        for i in range(len(self.leftEye)):
            self.leftEye[i] = Point(pose.x[idx], pose.y[idx])
            idx += 1

        for i in range(len(self.rightEye)):
            self.rightEye[i] = Point(pose.x[idx], pose.y[idx])
            idx += 1

        for i in range(len(self.nose)):
            self.nose[i] = Point(pose.x[idx], pose.y[idx])
            idx += 1

        for i in range(len(self.mouth)):
            self.mouth[i] = Point(pose.x[idx], pose.y[idx])
            idx += 1

        for i in range(len(self.faceProfile)):
            self.faceProfile[i] = Point(pose.x[idx], pose.y[idx])
            idx += 1

        for i in range(len(self.pupil)):
            self.pupil[i] = Point(pose.x[idx], pose.y[idx])
            idx += 1