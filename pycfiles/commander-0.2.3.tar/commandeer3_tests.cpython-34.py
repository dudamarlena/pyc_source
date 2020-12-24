# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/js/prog/commandeer/env/lib/python3.4/site-packages/tests/commandeer3_tests.py
# Compiled at: 2015-05-21 14:32:43
# Size of source mod 2**32: 1921 bytes
__doc__ = '\nTests specific to commandeer under Python3\n'
import unittest, commandeer

class TestFuncSpec3(unittest.TestCase):

    def test_one_arg_vararg_one_kwarg(self):

        def f(a1, *args, a2=None):
            pass

        accepts_args, args, defaults, kwargs, all_args = commandeer._funcspec(f)
        self.assertTrue(accepts_args)
        self.assertEqual(args, ['a1'])
        self.assertDictEqual(defaults, dict())
        self.assertDictEqual(kwargs, {'a2': None})
        self.assertEqual(all_args, ['a1', 'a2'])

    def test_one_arg_vararg_one_kwarg_kwargs(self):

        def f(a1, *args, a2=None, **kwargs):
            pass

        accepts_args, args, defaults, kwargs, all_args = commandeer._funcspec(f)
        self.assertTrue(accepts_args)
        self.assertEqual(args, ['a1'])
        self.assertDictEqual(defaults, dict())
        self.assertDictEqual(kwargs, {'a2': None}, 'f does not accept kwargs')
        self.assertEqual(all_args, ['a1', 'a2'])

    def test_one_arg_defaults_vararg_one_kwarg_kwargs(self):

        def f(a1, a2=None, *args, a3=None, **kwargs):
            pass

        accepts_args, args, defaults, kwargs, all_args = commandeer._funcspec(f)
        self.assertTrue(accepts_args)
        self.assertEqual(args, ['a1'])
        self.assertDictEqual(defaults, {'a2': None})
        self.assertDictEqual(kwargs, {'a3': None})
        self.assertEqual(all_args, ['a1', 'a2', 'a3'])

    def test_one_arg_defaults_one_kwarg_vararg_kwargs(self):

        def f(a1, a2=None, a3=None, *args, **kwargs):
            pass

        accepts_args, args, defaults, kwargs, all_args = commandeer._funcspec(f)
        self.assertTrue(accepts_args)
        self.assertEqual(args, ['a1'])
        self.assertDictEqual(defaults, {'a2': None,  'a3': None})
        self.assertDictEqual(kwargs, dict(), 'f does not accept kwargs')
        self.assertEqual(all_args, ['a1', 'a2', 'a3'])