# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paczesiowa/projects/tvu/tests/tvus_test.py
# Compiled at: 2017-02-15 05:59:21
from test_utils import TestCase
from test_compat import text
import tvu, tvu.tvus as tvus

class BoundedIntTest(TestCase):

    def unbounded_int_test(self):

        @tvu(x=tvus.bounded_int())
        def foo(x):
            return x

        self.assertEqual(foo(100), 100)
        self.assertEqual(foo(-100), -100)
        self.assertEqual(foo(1.0), 1)
        self.assertTrue(isinstance(foo(1.0), int))
        self.assertEqual(foo(-1.0), -1)
        self.assertTrue(isinstance(foo(-1.0), int))
        with self.assertRaises(TypeError, 'x must be int or float, not None'):
            foo(None)
        with self.assertRaises(ValueError, 'x must be a round number, not: 0.5'):
            foo(0.5)
        return

    def lower_bound_int_test(self):

        @tvu(x=tvus.bounded_int(minimum=0))
        def foo(x):
            return x

        self.assertEqual(foo(100), 100)
        self.assertEqual(foo(0), 0)
        self.assertEqual(foo(1.0), 1)
        self.assertTrue(isinstance(foo(1.0), int))
        with self.assertRaises(TypeError, 'x must be int or float, not None'):
            foo(None)
        with self.assertRaises(ValueError, 'x must be a round number, not: 0.5'):
            foo(0.5)
        err_msg = 'x must be an integer greater or equal to 0, not: -1'
        with self.assertRaises(ValueError, err_msg):
            foo(-1)
        err_msg = 'x must be an integer greater or equal to 0, not: -1.0'
        with self.assertRaises(ValueError, err_msg):
            foo(-1.0)
        return

    def upper_bound_int_test(self):

        @tvu(x=tvus.bounded_int(maximum=0))
        def foo(x):
            return x

        self.assertEqual(foo(-100), -100)
        self.assertEqual(foo(0), 0)
        self.assertEqual(foo(-1.0), -1)
        self.assertTrue(isinstance(foo(-1.0), int))
        with self.assertRaises(TypeError, 'x must be int or float, not None'):
            foo(None)
        with self.assertRaises(ValueError, 'x must be a round number, not: 0.5'):
            foo(0.5)
        err_msg = 'x must be an integer lesser or equal to 0, not: 1'
        with self.assertRaises(ValueError, err_msg):
            foo(1)
        err_msg = 'x must be an integer lesser or equal to 0, not: 1.0'
        with self.assertRaises(ValueError, err_msg):
            foo(1.0)
        return

    def bound_int_test(self):

        @tvu(x=tvus.bounded_int(minimum=0, maximum=10))
        def foo(x):
            return x

        self.assertEqual(foo(0), 0)
        self.assertEqual(foo(10), 10)
        self.assertEqual(foo(1.0), 1)
        self.assertTrue(isinstance(foo(1.0), int))
        with self.assertRaises(TypeError, 'x must be int or float, not None'):
            foo(None)
        with self.assertRaises(ValueError, 'x must be a round number, not: 0.5'):
            foo(0.5)
        err_msg = 'x must be an integer between 0 and 10 (inclusive), not: 11'
        with self.assertRaises(ValueError, err_msg):
            foo(11)
        err_msg = 'x must be an integer between 0 and 10 (inclusive), not: -1.0'
        with self.assertRaises(ValueError, err_msg):
            foo(-1.0)
        return

    def positive_int_test(self):

        @tvu(x=tvus.PositiveInt)
        def foo(x):
            return x

        self.assertEqual(foo(100), 100)
        self.assertEqual(foo(1.0), 1)
        self.assertTrue(isinstance(foo(1.0), int))
        with self.assertRaises(TypeError, 'x must be int or float, not None'):
            foo(None)
        with self.assertRaises(ValueError, 'x must be a round number, not: 0.5'):
            foo(0.5)
        err_msg = 'x must be an integer greater or equal to 1, not: -1'
        with self.assertRaises(ValueError, err_msg):
            foo(-1)
        err_msg = 'x must be an integer greater or equal to 1, not: 0.0'
        with self.assertRaises(ValueError, err_msg):
            foo(0.0)
        return


class IterableTest(TestCase):

    def iterable_test(self):

        @tvu(x=tvus.iterable())
        def foo(x):
            pass

        foo([])
        foo(iter({1, 2, 3}))
        with self.assertRaises(TypeError, 'x must be iterable, not None'):
            foo(None)
        return

    def not_stealing_test(self):

        @tvu(x=tvus.iterable())
        def foo(x):
            return next(iter(x))

        self.assertEqual(foo([1, 2]), 1)

        def bar():
            yield 1
            yield 2

        self.assertEqual(foo(bar()), 1)

    def iterable_with_elem_test(self):

        @tvu(x=tvus.iterable(tvus.PositiveInt))
        def foo(x):
            pass

        foo([])
        foo(iter({1, 2, 3}))
        with self.assertRaises(TypeError, 'x must be iterable, not None'):
            foo(None)
        err_msg = "x[0] must be int or float, not 'bar'"
        with self.assertRaises(TypeError, err_msg):
            foo(['bar'])
        err_msg = 'x[0] must be an integer greater or equal to 1, not: 0'
        with self.assertRaises(ValueError, err_msg):
            foo([0])
        err_msg = "x[1] must be int or float, not 'bar'"
        with self.assertRaises(TypeError, err_msg):
            foo([1, 'bar'])
        err_msg = 'x[1] must be an integer greater or equal to 1, not: 0'
        with self.assertRaises(ValueError, err_msg):
            foo([1, 0])
        return


class TextTest(TestCase):

    def text_test(self):

        @tvu(x=tvus.Text)
        def foo(x):
            return x

        self.assertEqual(foo(''), '')
        self.assertTrue(isinstance(foo(''), text))
        self.assertEqual(foo(''), '')
        self.assertTrue(isinstance(foo(''), text))
        self.assertEqual(foo('foo'), 'foo')
        self.assertTrue(isinstance(foo('foo'), text))
        self.assertEqual(foo('bar'), 'bar')
        self.assertTrue(isinstance(foo('bar'), text))
        err_msg = 'x must be %s or %s, not None' % (text.__name__,
         bytes.__name__)
        with self.assertRaises(TypeError, err_msg):
            foo(None)
        err_msg = 'x must be unicode text, or ascii-only bytestring'
        with self.assertRaises(ValueError, err_msg):
            foo(('żółw').encode('utf-8'))
        return


class NonEmptyTextTest(TestCase):

    def non_empty_text_test(self):

        @tvu(x=tvus.NonEmptyText)
        def foo(x):
            return x

        self.assertEqual(foo('foo'), 'foo')
        self.assertTrue(isinstance(foo('foo'), type('')))
        self.assertEqual(foo('bar'), 'bar')
        self.assertTrue(isinstance(foo('bar'), type('')))
        err_msg = 'x must be %s or %s, not None' % (text.__name__,
         bytes.__name__)
        with self.assertRaises(TypeError, err_msg):
            foo(None)
        err_msg = 'x must be unicode text, or ascii-only bytestring'
        with self.assertRaises(ValueError, err_msg):
            foo(('żółw').encode('utf-8'))
        with self.assertRaises(ValueError, 'x must be non-empty string'):
            foo('')
        with self.assertRaises(ValueError, 'x must be non-empty string'):
            foo('')
        return