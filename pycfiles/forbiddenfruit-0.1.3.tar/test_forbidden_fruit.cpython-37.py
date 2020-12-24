# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lincoln/src/github.com/clarete/forbiddenfruit/tests/unit/test_forbidden_fruit.py
# Compiled at: 2019-04-20 09:10:53
# Size of source mod 2**32: 7918 bytes
import sys
from datetime import datetime
from forbiddenfruit import curses, curse, reverse
from types import FunctionType
from nose.tools import nottest, istest
from . import ffruit

def almost_equal(a, b, e=0.001):
    """Helper method to compare floats"""
    return abs(a - b) < e


skip_legacy = nottest if sys.version_info < (3, 3) else istest

def test_cursing_a_builting_class():

    def words_of_wisdom(self):
        return self * 'blah '

    curse(int, 'words_of_wisdom', words_of_wisdom)
    assert (2).words_of_wisdom() == 'blah blah '
    assert 'words_of_wisdom' in dir(int)


def test_cursing_a_builting_class_with_a_class_method():

    def hello(self):
        return 'blah'

    curse(str, 'hello', classmethod(hello))
    assert str.hello() == 'blah'
    assert 'hello' in dir(str)


def test_reversing_a_builtin():
    curse(str, 'stuff', property(lambda s: s * 2))
    reverse(str, 'stuff')
    assert 'stuff' not in dir(str)


def test_dir_filtering():
    curse(str, 'my_stuff', 'blah', hide_from_dir=True)
    assert str.my_stuff == 'blah'
    assert 'my_stuff' not in dir(str)


def test_dir_filtering_same_symbol_different_type():
    curse(str, 'attr_x', 'blah', hide_from_dir=True)
    curse(int, 'attr_x', 'blah')
    assert str.attr_x == 'blah'
    assert 'attr_x' not in dir(str)
    assert int.attr_x == 'blah'
    assert 'attr_x' in dir(int)


def test_dir_filtering_same_symbol_different_instance():
    curse(str, 'attr_y', 'stuff', hide_from_dir=True)
    curse(int, 'attr_y', 'stuff')
    assert 'Hello'.attr_y == 'stuff'
    assert 'attr_y' not in dir('hello')
    assert (1).attr_y == 'stuff'
    assert 'attr_y' in dir(1)


def test_overriding_class_method():
    curse(datetime, 'now', classmethod(lambda *p: False))
    assert '_c_now' in dir(datetime)
    assert datetime.now() is False
    assert datetime(2013, 4, 5).now() is False


def test_overriding_instance_method():
    obj = ffruit.Dummy()
    curse(ffruit.Dummy, 'my_method', lambda *a, **k: 'Yo!')
    assert obj.my_method() == 'Yo!'


def test_overriding_non_c_things():
    """The `curse` function should not blow up on non-c python objs"""

    class Yo(object):
        pass

    obj = Yo()
    curse(Yo, 'my_method', lambda *a, **k: 'YoYo')
    assert obj.my_method() == 'YoYo'


def test_overriding_list_append():
    """The `curse` function should be able to curse existing symbols"""
    obj = []
    fn = lambda self, v: self._c_append(v) or self
    foo = curse(list, 'append', fn)
    assert obj.append(1) == [1]
    assert obj.append(2) == [1, 2]
    assert 1 in obj
    assert 2 in obj


def test_curses_decorator():
    """curses() should curse a given klass with the decorated function"""

    @curses(str, 'md_title')
    def markdown_title(self):
        return '# %s' % self.title()

    assert 'lincoln'.md_title() == '# Lincoln'


def test_dir_without_args_returns_names_in_local_scope():
    """dir() without arguments should return the names from the local scope
    of the calling frame, taking into account any indirection added
    by __filtered_dir__
    """
    z = 1
    some_name = 42
    assert 'some_name' in dir()
    assert dir() == sorted(locals().keys())


@skip_legacy
def test_dunder_func_chaining():
    """Overload * (mul) operator to to chaining between functions"""

    def matmul_chaining(self, other):
        if not isinstance(other, FunctionType):
            raise NotImplementedError()

        def wrapper(*args, **kwargs):
            res = other(*args, **kwargs)
            if hasattr(res, '__iter__'):
                return self(*res)
            return self(res)

        return wrapper

    curse(FunctionType, '__mul__', matmul_chaining)
    f = lambda x, y: x * y
    g = lambda x: (x, x)
    squared = f * g
    for i in range(0, 10, 2):
        assert squared(i) == i ** 2


@skip_legacy
def test_dunder_list_map():
    """Overload * (__mul__) operator to apply function to a list"""

    def map_list(func, list_):
        if not callable(func):
            raise NotImplementedError()
        return map(func, list_)

    curse(list, '__mul__', map_list)
    list_ = list(range(10))
    times_2 = lambda x: x * 2
    assert list(times_2 * list_) == list(range(0, 20, 2))


@skip_legacy
def test_dunder_unary():
    """Overload ~ operator to compute a derivative of function"""

    def derive_func(func):
        e = 0.001

        def wrapper(x):
            x_0 = x - e
            x_1 = x + e
            y_delta = func(x_1) - func(x_0)
            return y_delta / (2 * e)

        return wrapper

    curse(FunctionType, '__inv__', derive_func)
    f = lambda x: x ** 2 + x
    f_ = lambda x: 2 * x + 1
    assert almost_equal(~f(10), f_(10))


@skip_legacy
def test_sequence_dunder():

    def derive_func(func, deriv_grad):
        if deriv_grad == 0:
            return func
        e = 1e-07

        def wrapper(x):
            return (func(x + e) - func(x - e)) / (2 * e)

        if deriv_grad == 1:
            return wrapper
        return wrapper[(deriv_grad - 1)]

    curse(FunctionType, '__getitem__', derive_func)
    f = lambda x: x ** 3 - 2 * x ** 2
    f_1 = lambda x: 3 * x ** 2 - 4 * x
    f_2 = lambda x: 6 * x - 4
    for x in range(0, 10):
        x = float(x) / 10.0
        assert almost_equal(f(x), f[0](x))
        assert almost_equal(f_1(x), f[1](x))
        assert almost_equal((f_2(x)), (f[2](x)), e=0.01)


@skip_legacy
def test_dunder_list_revert():
    """Test reversion of a curse with dunders"""

    def map_list(func, list_):
        if not callable(func):
            raise NotImplementedError()
        return map(func, list_)

    curse(list, '__add__', map_list)
    list_ = list(range(10))
    times_2 = lambda x: x * 2
    assert list(times_2 + list_) == list(range(0, 20, 2))
    reverse(list, '__add__')
    try:
        times_2 + list_
    except TypeError:
        pass
    else:
        assert False