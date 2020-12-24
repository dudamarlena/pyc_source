# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/recurse_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1386 bytes
import unittest
from bibliopixel.project import fields, recurse
from bibliopixel.colors import COLORS

class Tester:

    @staticmethod
    def post_recursion(x):
        for k, v in x.items():
            if k != 'typename' and isinstance(v, str):
                x[k] = 'post-' + x[k]

    CHILDREN = ('foo', )


class RecurseTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(recurse.recurse({}), {})

    def test_trivial(self):
        self.assertEqual(recurse.recurse({'a': {}}), {'a': {}})

    post_recursion = staticmethod(fields.default_converter)

    def test_simple(self):
        source = {'datatype':RecurseTest, 
         'foo':'bar',  'color':'red'}
        expected = {'datatype':RecurseTest,  'foo':'bar',  'color':COLORS.Red}
        actual = recurse.recurse(source, post='post_recursion')
        self.assertEqual(expected, actual)

    def test_complex(self):
        source = {'typename':'%s.%s' % (Tester.__module__, Tester.__name__), 
         'foo':{'datatype':RecurseTest, 
          'foo':'bar',  'color':'red'}, 
         'bing':'bang'}
        expected = {'datatype':Tester, 
         'foo':{'datatype':RecurseTest, 
          'foo':'bar',  'color':COLORS.Red}, 
         'bing':'post-bang'}
        actual = recurse.recurse(source, post='post_recursion')
        self.assertEqual(expected, actual)