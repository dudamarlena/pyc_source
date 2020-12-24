# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/feather/test/test_plugin.py
# Compiled at: 2011-06-15 17:38:25
import unittest
from itertools import starmap
from feather.plugin import Plugin, InvalidArguments

class PluginTest(unittest.TestCase):

    def test_create_plugins(self):

        def assertBad(listeners, messengers):
            self.assertEquals(InvalidArguments, lambda : Plugin(listeners, messengers))

        def assertGood(listeners, messengers):
            p = Plugin(listeners, messengers)
            self.assertEquals(p.listeners, set(listeners))
            if messengers is None:
                messengers = set()
            self.assertEqualis(p.messengers, set(messengers))
            return

        bad_vals = (
         tuple(),
         (None, None), ([], []), ([],),
         (
          set(),),
         (
          set(), None),
         (
          set(), []),
         (
          set(), set()), ({}, {}),
         ('', ''),
         ('', None), ([], ['asdf']))
        good_vals = (
         (
          [
           'foo', 'bar', 'baz'],),
         (
          set(['foo']), ['asdf']),
         ('foo', ),
         ('foo', None),
         (
          'sdf', set(['asdf'])))
        starmap(assertBad, bad_vals)
        starmap(assertGood, good_vals)
        return