# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/octoprint_prometheus/gcodeparser.py
# Compiled at: 2019-02-23 13:17:04
import re

class Gcode_parser(object):
    MOVE_RE = re.compile('^G0\\s+|^G1\\s+')
    X_COORD_RE = re.compile('.*\\s+X([-]*\\d+\\.*\\d*)')
    Y_COORD_RE = re.compile('.*\\s+Y([-]*\\d+\\.*\\d*)')
    E_COORD_RE = re.compile('.*\\s+E([-]*\\d+\\.*\\d*)')
    Z_COORD_RE = re.compile('.*\\s+Z([-]*\\d+\\.*\\d*)')
    SPEED_VAL_RE = re.compile('.*\\s+F(\\d+\\.*\\d*)')

    def __init__(self):
        self.reset()

    def reset(self):
        self.last_extrusion_move = None
        self.extrusion_counter = 0
        self.x = None
        self.y = None
        self.z = None
        self.e = None
        self.speed = None
        return

    def is_extrusion_move(self, m):
        """ args are a tuple (x,y,z,e,speed)
        """
        if m and (m[0] is not None or m[1] is not None) and m[3] is not None and m[3] != 0:
            return True
        else:
            return False
            return

    def parse_move_args(self, line):
        """ returns a tuple (x,y,z,e,speed) or None
        """
        m = self.MOVE_RE.match(line)
        if m:
            x = None
            y = None
            z = None
            e = None
            speed = None
            m = self.X_COORD_RE.match(line)
            if m:
                x = float(m.groups()[0])
            m = self.Y_COORD_RE.match(line)
            if m:
                y = float(m.groups()[0])
            m = self.Z_COORD_RE.match(line)
            if m:
                z = float(m.groups()[0])
            m = self.E_COORD_RE.match(line)
            if m:
                e = float(m.groups()[0])
            m = self.SPEED_VAL_RE.match(line)
            if m:
                speed = float(m.groups()[0])
            return (
             x, y, z, e, speed)
        else:
            return

    def process_line(self, line):
        movement = self.parse_move_args(line)
        if movement:
            x, y, z, e, speed = movement
            if e is not None:
                self.extrusion_counter += e
                self.e = e
            if y is not None:
                self.y = y
            if z is not None:
                self.z = z
            if x is not None:
                self.x = x
            if speed is not None:
                self.speed = speed
            return True
        return False
        return