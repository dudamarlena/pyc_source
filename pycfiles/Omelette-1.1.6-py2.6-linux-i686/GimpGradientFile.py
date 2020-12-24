# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/GimpGradientFile.py
# Compiled at: 2007-09-25 20:00:35
from math import pi, log, sin, sqrt
import string
EPSILON = 1e-10

def linear(middle, pos):
    if pos <= middle:
        if middle < EPSILON:
            return 0.0
        else:
            return 0.5 * pos / middle
    else:
        pos = pos - middle
        middle = 1.0 - middle
        if middle < EPSILON:
            return 1.0
        return 0.5 + 0.5 * pos / middle


def curved(middle, pos):
    return pos ** (log(0.5) / log(max(middle, EPSILON)))


def sine(middle, pos):
    return (sin(-pi / 2.0 + pi * linear(middle, pos)) + 1.0) / 2.0


def sphere_increasing(middle, pos):
    return sqrt(1.0 - (linear(middle, pos) - 1.0) ** 2)


def sphere_decreasing(middle, pos):
    return 1.0 - sqrt(1.0 - linear(middle, pos) ** 2)


SEGMENTS = [
 linear, curved, sine, sphere_increasing, sphere_decreasing]

class GradientFile:
    gradient = None

    def getpalette(self, entries=256):
        palette = []
        ix = 0
        (x0, x1, xm, rgb0, rgb1, segment) = self.gradient[ix]
        for i in range(entries):
            x = i / float(entries - 1)
            while x1 < x:
                ix = ix + 1
                (x0, x1, xm, rgb0, rgb1, segment) = self.gradient[ix]

            w = x1 - x0
            if w < EPSILON:
                scale = segment(0.5, 0.5)
            else:
                scale = segment((xm - x0) / w, (x - x0) / w)
            r = chr(int(255 * ((rgb1[0] - rgb0[0]) * scale + rgb0[0]) + 0.5))
            g = chr(int(255 * ((rgb1[1] - rgb0[1]) * scale + rgb0[1]) + 0.5))
            b = chr(int(255 * ((rgb1[2] - rgb0[2]) * scale + rgb0[2]) + 0.5))
            a = chr(int(255 * ((rgb1[3] - rgb0[3]) * scale + rgb0[3]) + 0.5))
            palette.append(r + g + b + a)

        return (string.join(palette, ''), 'RGBA')


class GimpGradientFile(GradientFile):

    def __init__(self, fp):
        if fp.readline()[:13] != 'GIMP Gradient':
            raise SyntaxError, 'not a GIMP gradient file'
        count = int(fp.readline())
        gradient = []
        for i in range(count):
            s = string.split(fp.readline())
            w = map(float, s[:11])
            x0, x1 = w[0], w[2]
            xm = w[1]
            rgb0 = w[3:7]
            rgb1 = w[7:11]
            segment = SEGMENTS[int(s[11])]
            cspace = int(s[12])
            if cspace != 0:
                raise IOError, 'cannot handle HSV colour space'
            gradient.append((x0, x1, xm, rgb0, rgb1, segment))

        self.gradient = gradient