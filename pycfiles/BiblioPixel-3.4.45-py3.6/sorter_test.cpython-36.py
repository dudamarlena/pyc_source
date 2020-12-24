# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/animation/reprocess/sorter_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1603 bytes
import unittest
from bibliopixel.animation.reprocess import functions
from bibliopixel.colors.conversions import hsv2rgb_raw
COLORS = {ch:hsv2rgb_raw((ord(ch), 127, 127)) for ch in 'abcdef'}
INVERSE_COLORS = {c:ch for ch, c in COLORS.items()}

def sorter(input):
    s = [COLORS[i] for i in input]
    functions.sorter(s)
    return ''.join(INVERSE_COLORS[c] for c in s)


class SorterTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(sorter(''), '')

    def test_one(self):
        self.assertEqual(sorter('a'), 'a')

    def test_one(self):
        self.assertEqual(sorter('ba'), 'ab')

    def test_sorted(self):
        self.assertEqual(sorter('a'), 'a')
        self.assertEqual(sorter('ab'), 'ab')
        self.assertEqual(sorter('abc'), 'abc')
        self.assertEqual(sorter('abcd'), 'abcd')
        self.assertEqual(sorter('abcde'), 'abcde')

    def test_reverse(self):
        results = [
         'fedcba']
        while True:
            prev = results[(-1)]
            next = sorter(prev)
            if next == prev:
                break
            results.append(next)

        expected = [
         'fedcba',
         'efdcba',
         'edfcba',
         'defcba',
         'decfba',
         'dcefba',
         'cdefba',
         'cdebfa',
         'cdbefa',
         'cbdefa',
         'bcdefa',
         'bcdeaf',
         'bcdaef',
         'bcadef',
         'bacdef',
         'abcdef']
        self.assertEqual(results, expected)