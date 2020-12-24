# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/dicttokv/test.py
# Compiled at: 2014-01-01 08:27:59
from __future__ import unicode_literals, print_function
import unittest
from main import DictToKeyValue as D
from collections import OrderedDict
from_object = D.from_object
restore = D.restore

class SimpleTest(unittest.TestCase):
    example = {b'menu': {b'header': b'SVG Viewer', 
                 b'items': [{b'id': b'Open'}, {b'id': b'OpenNew', b'label': b'Open New'},
                          None, {b'id': b'ZoomIn', b'label': b'Zoom In'}, {b'id': b'ZoomOut', b'label': b'Zoom Out'}, {b'id': b'OriginalView', b'label': b'Original View'},
                          None, {b'id': b'Quality'}, {b'id': b'Pause'}, {b'id': b'Mute'},
                          None, {b'id': b'Find', b'label': b'Find...'}, {b'id': b'FindAgain', b'label': b'Find Again'}, {b'id': b'Copy'}, {b'id': b'CopyAgain', b'label': b'Copy Again'}, {b'id': b'CopySVG', b'label': b'Copy SVG'}, {b'id': b'ViewSVG', b'label': b'View SVG'}, {b'id': b'ViewSource', b'label': b'View Source'}, {b'id': b'SaveAs', b'label': b'Save As'},
                          None, {b'id': b'Help'}, {b'id': b'About', b'label': b'About Adobe CVG Viewer...'}]}}
    converted = [
     (('menu', 'header'), 'SVG Viewer'),
     (('menu', 'items', 0, 'id'), 'Open'),
     (('menu', 'items', 1, 'id'), 'OpenNew'),
     (('menu', 'items', 1, 'label'), 'Open New'),
     (('menu', 'items', 2), None),
     (('menu', 'items', 3, 'id'), 'ZoomIn'),
     (('menu', 'items', 3, 'label'), 'Zoom In'),
     (('menu', 'items', 4, 'id'), 'ZoomOut'),
     (('menu', 'items', 4, 'label'), 'Zoom Out'),
     (('menu', 'items', 5, 'id'), 'OriginalView'),
     (('menu', 'items', 5, 'label'), 'Original View'),
     (('menu', 'items', 6), None),
     (('menu', 'items', 7, 'id'), 'Quality'),
     (('menu', 'items', 8, 'id'), 'Pause'),
     (('menu', 'items', 9, 'id'), 'Mute'),
     (('menu', 'items', 10), None),
     (('menu', 'items', 11, 'id'), 'Find'),
     (('menu', 'items', 11, 'label'), 'Find...'),
     (('menu', 'items', 12, 'id'), 'FindAgain'),
     (('menu', 'items', 12, 'label'), 'Find Again'),
     (('menu', 'items', 13, 'id'), 'Copy'),
     (('menu', 'items', 14, 'id'), 'CopyAgain'),
     (('menu', 'items', 14, 'label'), 'Copy Again'),
     (('menu', 'items', 15, 'id'), 'CopySVG'),
     (('menu', 'items', 15, 'label'), 'Copy SVG'),
     (('menu', 'items', 16, 'id'), 'ViewSVG'),
     (('menu', 'items', 16, 'label'), 'View SVG'),
     (('menu', 'items', 17, 'id'), 'ViewSource'),
     (('menu', 'items', 17, 'label'), 'View Source'),
     (('menu', 'items', 18, 'id'), 'SaveAs'),
     (('menu', 'items', 18, 'label'), 'Save As'),
     (('menu', 'items', 19), None),
     (('menu', 'items', 20, 'id'), 'Help'),
     (('menu', 'items', 21, 'id'), 'About'),
     (('menu', 'items', 21, 'label'), 'About Adobe CVG Viewer...')]

    def test_example_json(self):
        self.assertEquals(list(from_object(self.example)), self.converted)

    def test_list(self):
        self.assertEquals(list(from_object({b'a': [0, 1]})), [
         (('a', 0), 0), (('a', 1), 1)])

    def test_listroot(self):
        self.assertEquals(list(from_object([3, 4, 5])), [
         ((0,), 3), ((1,), 4), ((2,), 5)])
        self.assertEquals([
         3, 4, 5], restore([((0,), 3), ((1,), 4), ((2,), 5)]))

    def test_nested_dict(self):
        result = list(from_object({b'a': {b'b': b'c'}}))
        self.assertEquals(result, [(('a', 'b'), 'c')])

    def test_dict(self):
        result = list(from_object({b'a': b'b'}))
        self.assertEquals(result, [(('a',), 'b')])

    def test_ordereddict(self):
        od = OrderedDict([
         ('a', 'b'),
         ('c', 'd'),
         ('x', 'y')])
        result = list(from_object(od))
        self.assertEquals(result, [(('a',), 'b'), (('c',), 'd'), (('x',), 'y')])

    def test_restore(self):
        converted = [
         (('a',), 1),
         (('b',), 'x'),
         (('c', 'd'), 'y'),
         (('e', 0), 'first'),
         (('e', 1), 'second'),
         (('e', 2), 'third')]
        restored = restore(converted)
        self.assertEquals(len(restored), 4)
        self.assertEquals(restored[b'a'], 1)
        self.assertEquals(restored[b'b'], b'x')
        self.assertEquals(restored[b'c'][b'd'], b'y')
        self.assertEquals(restored[b'e'][0], b'first')
        self.assertEquals(restored[b'e'][1], b'second')
        self.assertEquals(restored[b'e'][2], b'third')

    def test_restore2(self):
        converted = [
         (('a', 0, 'b'), '1'),
         (('a', 1, 'b'), '2'),
         (('a', 1, 'c'), '4'),
         (('a', 2, 'b'), '3'),
         (('a', 2, 'c'), '5')]
        restored = restore(converted)
        self.assertEquals(restored[b'a'][0][b'b'], b'1')
        self.assertEquals(restored[b'a'][1][b'b'], b'2')
        self.assertEquals(restored[b'a'][2][b'b'], b'3')

    def test_restore3(self):
        self.assertDictEqual(self.example, restore(self.converted))
        self.assertDictEqual(restore(from_object(self.example)), restore(self.converted))


if __name__ == b'__main__':
    unittest.main()