# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\plugins\netblocker\netblock\test_ranges.py
# Compiled at: 2016-03-08 18:42:10
import unittest
from b3.plugins.netblocker.netblock import ranges

class basicTests(unittest.TestCase):

    def testStrResults(self):
        """Test the result of str() of a Ranges on known values."""
        self.assertEqual(str(ranges.Ranges()), '<Ranges: >')
        self.assertEqual(str(ranges.Ranges(1, 10)), '<Ranges: 1-10>')
        self.assertEqual(str(ranges.Ranges(1, 1)), '<Ranges: 1>')
        r = ranges.Ranges()
        r.addrange(5, 10)
        r.addnum(1)
        self.assertEqual(str(r), '<Ranges: 1 5-10>')

    knownAddValues = (
     (
      (
       (1, 1), (2, 2)), [[1, 2]]),
     (
      (
       (10, 10), (5, 9)), [[5, 10]]),
     (
      (
       (10, 10), (11, 15)), [[10, 15]]),
     (
      (
       (1, 5), (7, 7), (9, 10), (8, 8)), [[1, 5], [7, 10]]),
     (
      (
       (1, 10), (4, 6)), [[1, 10]]),
     (
      (
       (1, 2), (4, 5)), [[1, 2], [4, 5]]),
     (
      (
       (1, 2), (7, 8), (4, 5)), [[1, 2], [4, 5], [7, 8]]),
     (
      (
       (1, 2), (7, 8), (4, 5), (10, 11)),
      [
       [
        1, 2], [4, 5], [7, 8], [10, 11]]),
     (
      (
       (3000000000, 3000000099), (3000001000, 3000001099)),
      [
       [
        3000000000, 3000000099], [3000001000, 3000001099]]),
     (
      (
       (3000000000, 3000000099), (3000000090, 3000000200)),
      [
       [
        3000000000, 3000000200]]),
     (
      (
       (1, 10), (20, 30), (40, 50), (20, 25)),
      [
       [
        1, 10], [20, 30], [40, 50]]),
     (
      (
       (1, 10), (1, 10)), [[1, 10]]),
     (
      (
       (1, 10), (5, 8)), [[1, 10]]),
     (
      (
       (1, 10), (1, 5)), [[1, 10]]),
     (
      (
       (1, 10), (5, 10)), [[1, 10]]))

    def testAddSubValues(self):
        """Test that adding up a series of ranges results in a known list and that subtracting them again yields an empty list."""
        for elist, rval in self.knownAddValues:
            r = ranges.Ranges()
            r.addlist(elist)
            self.assertEqual(r._l, rval)
            r.dellist(elist)
            self.assertEqual(r._l, [])
            r.addlist(elist)
            elist = list(elist)
            elist.reverse()
            r.dellist(elist)
            self.assertEqual(r._l, [])
            r.addlist(elist)
            self.assertEqual(r._l, rval)

    def testInOperator(self):
        """Test the 'in' operator of Ranges."""
        r = ranges.Ranges(2, 10)
        self.assertEqual(0 in r, 0)
        self.assertEqual(2 in r, 1)
        for elist, ign in self.knownAddValues:
            r = ranges.Ranges()
            r.addlist(elist)
            for e in r:
                self.assertEqual(e in r, 1)

        rl = ((2, 10), (15, 17), (20, 25), (30, 35), (40, 45),
         (50, 60), (70, 75), (80, 85), (90, 95), (100, 105),
         (110, 120), (125, 128), (130, 135), (140, 150))
        r = ranges.Ranges()
        r.addlist(rl)
        for i in (2, 10, 16, 20, 144, 91, 85):
            self.assertEqual(i in r, 1)

        for i in (1, 11, 151, 200, 0, 88):
            self.assertEqual(i in r, 0)

    knownIterValues = (
     (
      ((1, 1), ), (1, )),
     (
      ((1, 3), ), (1, 2, 3)),
     (
      (
       (1, 3), (6, 8)), (1, 2, 3, 6, 7, 8)),
     (
      (
       (1, 2), (6, 8), (10, 11)), (1, 2, 6, 7, 8, 10, 11)),
     (
      ((3000000000, 3000000003), ),
      (3000000000, 3000000001, 3000000002, 3000000003)))

    def testIterOperation(self):
        """Test that Ranges iteration yields known values."""
        for initlist, restup in self.knownIterValues:
            r = ranges.Ranges()
            r.addlist(initlist)
            self.assertEqual(tuple(r), restup)

    def testLenOperation(self):
        """Test len(Ranges) for basic proper operation."""
        r = ranges.Ranges()
        self.assertEqual(len(r), 0)
        r.addnum(1)
        self.assertEqual(len(r), 1)
        r.addnum(2)
        self.assertEqual(len(r), 2)
        r.addrange(10, 15)
        self.assertEqual(len(r), 8)

    def testSubsetOperator(self):
        """Test Ranges.subset() for basic proper operation."""
        e = ranges.Ranges()
        mr = ranges.Ranges(-10, -5)
        self.assertEqual(e.subset(e), 1)
        for il, res in self.knownAddValues:
            r = ranges.Ranges()
            r.addlist(il)
            self.assertEqual(r.subset(e), 1)
            self.assertEqual(r.subset(r), 1)
            self.assertEqual(r.subset(mr), 0)
            r1 = r.copy()
            r1.addnum(1000)
            self.assertEqual(r.subset(r1), 0)
            self.assertEqual(r1.subset(r), 1)

    knownSubsetValues = (
     (
      (
       (1, 10), (20, 30), (40, 50)),
      (
       (25, 28), (41, 41)), 1),
     (
      (
       (1, 10), (20, 30), (40, 50)),
      ((2, 11), ), 0),
     (
      (
       (1, 10), (20, 30), (40, 50)),
      (
       (15, 15), (20, 30)), 0),
     (
      ((2, 20), ), ((1, 25), ), 0),
     (
      ((1, 25), ), ((2, 20), ), 1))

    def testSubsetKnown(self):
        """Test Ranges.subset() against some known values."""
        for l1, l2, res in self.knownSubsetValues:
            r1 = ranges.Ranges()
            r1.addlist(l1)
            r2 = ranges.Ranges()
            r2.addlist(l2)
            self.assertEqual(r1.subset(r2), res)

    knownIntersectRanges = (
     (
      ((1, 10), ), ((5, 5), ), 1),
     (
      ((1, 10), ), ((5, 8), ), 1),
     (
      ((1, 10), ), ((5, 15), ), 1),
     (
      ((1, 10), ), ((10, 15), ), 1),
     (
      ((1, 10), ), ((11, 15), ), 0),
     (
      (
       (1, 10), (20, 30), (40, 50)),
      ((35, 43), ), 1),
     (
      (
       (1, 10), (20, 30), (40, 50)),
      (
       (15, 19), (31, 39), (51, 51)), 0),
     (
      (
       (1, 10), (20, 30), (40, 50)),
      ((25, 28), ), 1))

    def testIntersectBasics(self):
        """Test for basic correctness of Ranges.intersect()."""
        e = ranges.Ranges()
        self.assertEqual(e.intersect(e), 0)
        for l1, l2, res in self.knownIntersectRanges:
            r1 = ranges.Ranges()
            r1.addlist(l1)
            r2 = ranges.Ranges()
            r2.addlist(l2)
            self.assertEqual(e.intersect(r1), 0)
            self.assertEqual(r2.intersect(e), 0)
            self.assertEqual(r1.intersect(r2), res, 'failed on %s versus %s' % (str(r1), str(r2)))
            self.assertEqual(r2.intersect(r1), res)

    knownAdjacents = (
     (
      (10, 20), (1, 9), 1),
     (
      (10, 20), (1, 10), 0),
     (
      (10, 20), (1, 8), 0),
     (
      (10, 20), (21, 35), 1))

    def testAdjacentFunc(self):
        """Test Ranges.adjacent() with known values."""
        e = ranges.Ranges()
        for al, bl, res in self.knownAdjacents:
            r1 = ranges.Ranges(al[0], al[1])
            r2 = ranges.Ranges(bl[0], bl[1])
            self.assertEqual(r1.adjacent(r2), res)
            self.assertEqual(r2.adjacent(r1), res)
            for r in (r1, r2):
                self.assertEqual(e.adjacent(r), 0)
                self.assertEqual(r.adjacent(e), 0)

    knownAddSubs = (
     (
      (1, 10), (11, 20), '<Ranges: 1-20>', '<Ranges: 1-10>'),
     (
      (1, 10), (5, 15), '<Ranges: 1-15>', '<Ranges: 1-4>'),
     (
      (1, 10), (20, 30), '<Ranges: 1-10 20-30>', '<Ranges: 1-10>'),
     (
      (10, 20), (1, 30), '<Ranges: 1-30>', '<Ranges: >'),
     (
      (1, 30), (10, 20), '<Ranges: 1-30>', '<Ranges: 1-9 21-30>'))

    def testAddSubFunc(self):
        """Test that object addition and subtraction work."""
        e = ranges.Ranges()
        for al, bl, ares, sres in self.knownAddSubs:
            r1 = ranges.Ranges(al[0], al[1])
            r2 = ranges.Ranges(bl[0], bl[1])
            for r in (r1, r2):
                self.assertEqual(r == r + r, 1)
                self.assertEqual(e == r - r, 1)

            ra = r1 + r2
            rs = r1 - r2
            self.assertEqual(str(ra), ares)
            self.assertEqual(str(rs), sres)

    def testAddSubRanges(self):
        """Test that addRanges and delRanges work right."""
        for al, bl, ares, sres in self.knownAddSubs:
            r1 = ranges.Ranges(al[0], al[1])
            r2 = ranges.Ranges(bl[0], bl[1])
            r1.addRanges(r2)
            self.assertEqual(str(r1), ares)
            r1.delRanges(r2)
            self.assertEqual(str(r1), sres)


class failureTests(unittest.TestCase):

    def testKnownInitfailures(self):
        """Test that Ranges fail to initialize for certain known bad inputs."""
        self.assertRaises(TypeError, ranges.Ranges, 1, 2, 3, 4)
        self.assertRaises(TypeError, ranges.Ranges, 1)
        self.assertRaises(ranges.BadRange, ranges.Ranges, 10, 9)
        r = ranges.Ranges()
        self.assertRaises(ranges.BadRange, r.addrange, 10, 9)
        self.assertRaises(ranges.BadRange, r.delrange, 10, 9)


if __name__ == '__main__':
    unittest.main()