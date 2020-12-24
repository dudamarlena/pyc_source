# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/tests/ycollections/test_tagmaps.py
# Compiled at: 2016-07-19 10:55:32
from unittest import TestCase
from ycyc.ycollections import tagmaps

class TestTagMaps(TestCase):

    def test_uasge(self):
        maps = tagmaps.TagMaps()

        @maps.register('add')
        def add(x, y):
            return x + y

        @maps.register('sub')
        def sub(x, y):
            return x - y

        self.assertEqual(maps['add'](1, 2), add(1, 2))
        self.assertEqual(maps['sub'](4, 5), sub(4, 5))
        with self.assertRaises(KeyError):
            self.assertEqual(maps['noexist'](6, 7), None)

        @maps.register(maps.DefaultKey)
        def default(x, y):
            return

        self.assertEqual(maps['noexist'](8, 9), default(8, 9))
        self.assertListEqual(list(maps), ['', 'add', 'sub'])
        self.assertEqual(list(maps)[0], '')
        self.assertEqual(list(maps)[1], 'add')
        self.assertEqual(list(maps)[2], 'sub')
        return