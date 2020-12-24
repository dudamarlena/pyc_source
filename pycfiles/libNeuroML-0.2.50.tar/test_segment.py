# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/padraig/libNeuroML/neuroml/test/test_segment.py
# Compiled at: 2017-07-07 13:05:49
"""
Unit tests for the Segment class

"""
import math
from neuroml import Segment
from neuroml import Point3DWithDiam
try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestSingleSegment(unittest.TestCase):

    def test_proximal_diameter(self):
        proximal_point = Point3DWithDiam(diameter=3.21)
        seg = Segment(proximal=proximal_point)
        self.assertEqual(seg.proximal.diameter, 3.21)

    def test_distal_diameter(self):
        distal_point = Point3DWithDiam(diameter=3.21)
        seg = Segment(distal=distal_point)
        self.assertEqual(seg.distal.diameter, 3.21)

    def test_proximal_coordinates(self):
        proximal_point = Point3DWithDiam(x=0.1, y=0.2, z=0.3)
        seg = Segment(proximal=proximal_point)
        self.assertEqual(seg.proximal.x, 0.1)
        self.assertEqual(seg.proximal.y, 0.2)
        self.assertEqual(seg.proximal.z, 0.3)

    def test_distal_coordinates(self):
        distal_point = Point3DWithDiam(x=0.1, y=0.2, z=0.3)
        seg = Segment(distal=distal_point)
        self.assertEqual(seg.distal.x, 0.1)
        self.assertEqual(seg.distal.y, 0.2)
        self.assertEqual(seg.distal.z, 0.3)


class TestHelperProperties(unittest.TestCase):
    """
    Tests for helper properties for volume, area etc

    These are not part of the neuroML schema itself
    """

    def test_length0(self):
        diam = 1.0
        len = 1.0
        d = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=len, z=0, diameter=diam)
        seg = Segment(proximal=p, distal=d)
        self.assertAlmostEqual(seg.length, 1, places=7)

    def test_length(self):
        d = Point3DWithDiam(x=0.2, y=2.4, z=3.5, diameter=0.6)
        p = Point3DWithDiam(x=0.5, y=2.0, z=1.8, diameter=0.9)
        seg = Segment(proximal=p, distal=d)
        self.assertAlmostEqual(seg.length, 1.772004514, places=7)

    def test_area0(self):
        diam = 1.0
        len = 1.0
        d = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=len, z=0, diameter=diam)
        seg = Segment(proximal=p, distal=d)
        self.assertAlmostEqual(seg.surface_area, math.pi * diam * len, places=7)

    def test_area1(self):
        diam = 1.0
        len = 1.0
        d = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=len, z=0, diameter=diam * 1.01)
        seg = Segment(proximal=p, distal=d)
        self.assertAlmostEqual(seg.surface_area, 3.15734008, places=7)

    def test_area(self):
        d = Point3DWithDiam(x=0.2, y=2.4, z=3.5, diameter=0.6)
        p = Point3DWithDiam(x=0.5, y=2.0, z=1.8, diameter=0.9)
        seg = Segment(proximal=p, distal=d)
        self.assertAlmostEqual(seg.surface_area, 4.19011944, places=7)

    def test_volume0(self):
        diam = 1.0
        len = 1.0
        d = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=len, z=0, diameter=diam)
        seg = Segment(proximal=p, distal=d)
        self.assertAlmostEqual(seg.volume, math.pi * (diam / 2) ** 2 * len, places=7)

    def test_volume1(self):
        diam = 1.0
        len = 1.0
        d = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=len, z=0, diameter=diam * 1.01)
        seg = Segment(proximal=p, distal=d)
        self.assertAlmostEqual(seg.volume, 0.793278324, places=7)

    def test_volume(self):
        d = Point3DWithDiam(x=0.2, y=2.4, z=3.5, diameter=0.6)
        p = Point3DWithDiam(x=0.5, y=2.0, z=1.8, diameter=0.9)
        seg = Segment(proximal=p, distal=d)
        self.assertAlmostEqual(seg.volume, 0.7932855820702964, places=7)

    def runTest(self):
        print 'Running tests in TestHelperProperties'


class TestAttachedSegments(unittest.TestCase):
    pass


if __name__ == '__main__':
    ta = TestHelperProperties()
    ta.test_length0()
    ta.test_length()
    ta.test_area0()
    ta.test_area1()
    ta.test_area()
    ta.test_volume0()
    ta.test_volume1()
    ta.test_volume()