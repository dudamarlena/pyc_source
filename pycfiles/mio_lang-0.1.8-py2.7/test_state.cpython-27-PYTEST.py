# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/test_state.py
# Compiled at: 2013-12-08 17:19:04
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import raises
from decimal import Decimal
from mio import runtime
from mio.utils import Null
from mio.state import Completer
from mio.errors import AttributeError, Error

class Foo(object):
    """Foo Class

    mio does not support coerving Python user classes, methods or
    objects. Trying to convert these to mio with ``runtime.state.tomio(...)``
    will fail and if a ``default`` value is passed will return that.
    """

    def foo(self):
        """foo method"""
        pass


def test_tomio_class(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.tomio
    @py_assert7 = @py_assert3(Foo, Null)
    @py_assert9 = @py_assert7 is Null
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('is',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.tomio\n}(%(py5)s, %(py6)s)\n} is %(py10)s',), (@py_assert7, Null)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(Foo) if 'Foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Foo) else 'Foo', 'py6': @pytest_ar._saferepr(Null) if 'Null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Null) else 'Null', 'py10': @pytest_ar._saferepr(Null) if 'Null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Null) else 'Null'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert7 = @py_assert9 = None
    return


def test_tomio_object(mio):
    foo = Foo()
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.tomio
    @py_assert7 = @py_assert3(foo, Null)
    @py_assert9 = @py_assert7 is Null
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('is',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.tomio\n}(%(py5)s, %(py6)s)\n} is %(py10)s',), (@py_assert7, Null)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py6': @pytest_ar._saferepr(Null) if 'Null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Null) else 'Null', 'py10': @pytest_ar._saferepr(Null) if 'Null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Null) else 'Null'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert7 = @py_assert9 = None
    return


def test_tomio_method(mio):
    foo = Foo()
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.tomio
    @py_assert6 = foo.foo
    @py_assert9 = @py_assert3(@py_assert6, Null)
    @py_assert11 = @py_assert9 is Null
    if not @py_assert11:
        @py_format13 = @pytest_ar._call_reprcompare(('is',), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.tomio\n}(%(py7)s\n{%(py7)s = %(py5)s.foo\n}, %(py8)s)\n} is %(py12)s',), (@py_assert9, Null)) % {'py8': @pytest_ar._saferepr(Null) if 'Null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Null) else 'Null', 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(Null) if 'Null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Null) else 'Null', 'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert9 = @py_assert11 = None
    return


def test_frommio_Number(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.frommio
    @py_assert6 = mio.eval
    @py_assert8 = '1.0'
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert12 = @py_assert3(@py_assert10)
    @py_assert16 = 1.0
    @py_assert18 = Decimal(@py_assert16)
    @py_assert14 = @py_assert12 == @py_assert18
    if not @py_assert14:
        @py_format20 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.frommio\n}(%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s.eval\n}(%(py9)s)\n})\n} == %(py19)s\n{%(py19)s = %(py15)s(%(py17)s)\n}',), (@py_assert12, @py_assert18)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py19': @pytest_ar._saferepr(@py_assert18), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py7': @pytest_ar._saferepr(@py_assert6), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(Decimal) if 'Decimal' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Decimal) else 'Decimal'}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    return


def test_tomio_Number(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.tomio
    @py_assert5 = 1.0
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert11 = mio.eval
    @py_assert13 = '1.0'
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert9 = @py_assert7 == @py_assert15
    if not @py_assert9:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.tomio\n}(%(py6)s)\n} == %(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py10)s.eval\n}(%(py14)s)\n}',), (@py_assert7, @py_assert15)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py16': @pytest_ar._saferepr(@py_assert15), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(@py_assert13), 'py10': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio'}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    return


def test_frommio_Boolean(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.frommio
    @py_assert6 = mio.eval
    @py_assert8 = 'True'
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert12 = @py_assert3(@py_assert10)
    @py_assert14 = @py_assert12 is True
    if not @py_assert14:
        @py_format16 = @pytest_ar._call_reprcompare(('is',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.frommio\n}(%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s.eval\n}(%(py9)s)\n})\n} is %(py15)s',), (@py_assert12, True)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py7': @pytest_ar._saferepr(@py_assert6), 'py15': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True'}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    return


def test_tomio_Boolean(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.tomio
    @py_assert6 = @py_assert3(True)
    @py_assert10 = mio.eval
    @py_assert12 = 'True'
    @py_assert14 = @py_assert10(@py_assert12)
    @py_assert8 = @py_assert6 == @py_assert14
    if not @py_assert8:
        @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.tomio\n}(%(py5)s)\n} == %(py15)s\n{%(py15)s = %(py11)s\n{%(py11)s = %(py9)s.eval\n}(%(py13)s)\n}',), (@py_assert6, @py_assert14)) % {'py9': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True', 'py7': @pytest_ar._saferepr(@py_assert6), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    return


def test_frommio_String(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.frommio
    @py_assert6 = mio.eval
    @py_assert8 = 'String clone()'
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert12 = @py_assert3(@py_assert10)
    @py_assert15 = ''
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.frommio\n}(%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s.eval\n}(%(py9)s)\n})\n} == %(py16)s',), (@py_assert12, @py_assert15)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py7': @pytest_ar._saferepr(@py_assert6), 'py16': @pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    return


def test_tomio_String(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.tomio
    @py_assert5 = ''
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert11 = mio.eval
    @py_assert13 = 'String clone()'
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert9 = @py_assert7 == @py_assert15
    if not @py_assert9:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.tomio\n}(%(py6)s)\n} == %(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py10)s.eval\n}(%(py14)s)\n}',), (@py_assert7, @py_assert15)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py16': @pytest_ar._saferepr(@py_assert15), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(@py_assert13), 'py10': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio'}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    return


def test_frommio_List(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.frommio
    @py_assert6 = mio.eval
    @py_assert8 = 'List clone()'
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert12 = @py_assert3(@py_assert10)
    @py_assert15 = []
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.frommio\n}(%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s.eval\n}(%(py9)s)\n})\n} == %(py16)s',), (@py_assert12, @py_assert15)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py7': @pytest_ar._saferepr(@py_assert6), 'py16': @pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    return


def test_tomio_List(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.tomio
    @py_assert5 = []
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert11 = mio.eval
    @py_assert13 = 'List clone()'
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert9 = @py_assert7 == @py_assert15
    if not @py_assert9:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.tomio\n}(%(py6)s)\n} == %(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py10)s.eval\n}(%(py14)s)\n}',), (@py_assert7, @py_assert15)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py16': @pytest_ar._saferepr(@py_assert15), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(@py_assert13), 'py10': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio'}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    return


def test_frommio_Tuple(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.frommio
    @py_assert6 = mio.eval
    @py_assert8 = 'Tuple clone()'
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert12 = @py_assert3(@py_assert10)
    @py_assert15 = ()
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.frommio\n}(%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s.eval\n}(%(py9)s)\n})\n} == %(py16)s',), (@py_assert12, @py_assert15)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py7': @pytest_ar._saferepr(@py_assert6), 'py16': @pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    return


def test_tomio_Tuple(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.tomio
    @py_assert5 = ()
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert11 = mio.eval
    @py_assert13 = 'Tuple clone()'
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert9 = @py_assert7 == @py_assert15
    if not @py_assert9:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.tomio\n}(%(py6)s)\n} == %(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py10)s.eval\n}(%(py14)s)\n}',), (@py_assert7, @py_assert15)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py16': @pytest_ar._saferepr(@py_assert15), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(@py_assert13), 'py10': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio'}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    return


def test_frommio_Dict(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.frommio
    @py_assert6 = mio.eval
    @py_assert8 = 'Dict clone()'
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert12 = @py_assert3(@py_assert10)
    @py_assert15 = {}
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.frommio\n}(%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s.eval\n}(%(py9)s)\n})\n} == %(py16)s',), (@py_assert12, @py_assert15)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py7': @pytest_ar._saferepr(@py_assert6), 'py16': @pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    return


def test_tomio_Dict(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.tomio
    @py_assert5 = {}
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert11 = mio.eval
    @py_assert13 = 'Dict clone()'
    @py_assert15 = @py_assert11(@py_assert13)
    @py_assert9 = @py_assert7 == @py_assert15
    if not @py_assert9:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.tomio\n}(%(py6)s)\n} == %(py16)s\n{%(py16)s = %(py12)s\n{%(py12)s = %(py10)s.eval\n}(%(py14)s)\n}',), (@py_assert7, @py_assert15)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py16': @pytest_ar._saferepr(@py_assert15), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(@py_assert13), 'py10': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio'}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    return


def test_tomio_default(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.frommio
    @py_assert6 = runtime.state
    @py_assert8 = @py_assert6.tomio
    @py_assert12 = type(None)
    @py_assert14 = @py_assert8(@py_assert12)
    @py_assert16 = @py_assert3(@py_assert14)
    @py_assert18 = @py_assert16 is None
    if not @py_assert18:
        @py_format20 = @pytest_ar._call_reprcompare(('is',), (@py_assert18,), ('%(py17)s\n{%(py17)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.frommio\n}(%(py15)s\n{%(py15)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.state\n}.tomio\n}(%(py13)s\n{%(py13)s = %(py10)s(%(py11)s)\n})\n})\n} is %(py19)s',), (@py_assert16, None)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py19': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None', 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None', 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py7': @pytest_ar._saferepr(@py_assert6), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(@py_assert14), 'py10': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type'}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    return


def test_error(mio, capfd):
    with raises(AttributeError):
        mio.eval('foobar()', reraise=True)
    out, err = capfd.readouterr()
    @py_assert2 = "\n  AttributeError: Object has no attribute 'foobar'\n  ---------------\n  foobar\n\n"
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (out, @py_assert2)) % {'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_usererror(mio, capfd):
    with raises(Error):
        mio.eval('raise TypeError', reraise=True)
    out, err = capfd.readouterr()
    @py_assert2 = '\n  TypeError: \n  ----------\n  raise(TypeError)\n\n'
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (out, @py_assert2)) % {'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_runsource(mio):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.runsource
    @py_assert5 = '(1 + 2'
    @py_assert7 = @py_assert3(@py_assert5)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.runsource\n}(%(py6)s)\n}' % {'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    return


def test_runsource2(mio, capfd):
    @py_assert1 = runtime.state
    @py_assert3 = @py_assert1.runsource
    @py_assert5 = '(1 + 2)'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert9 = @py_assert7 is None
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.state\n}.runsource\n}(%(py6)s)\n} is %(py10)s', ), (@py_assert7, None)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(runtime) if 'runtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(runtime) else 'runtime', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py10': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    out, err = capfd.readouterr()
    @py_assert2 = '===> 3\n'
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (out, @py_assert2)) % {'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_completer(mio):
    completer = Completer(mio)
    @py_assert1 = completer.complete
    @py_assert3 = ''
    @py_assert5 = 0
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 'Core'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.complete\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(completer) if 'completer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(completer) else 'completer', 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    return


def test_completer2(mio):
    completer = Completer(mio)
    @py_assert1 = completer.complete
    @py_assert3 = 'Root '
    @py_assert5 = 0
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 'Root Core'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.complete\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(completer) if 'completer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(completer) else 'completer', 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    return


def test_completer3(mio):
    completer = Completer(mio)
    @py_assert1 = completer.complete
    @py_assert3 = 'Root bu'
    @py_assert5 = 0
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 'Root builtins'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.complete\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(completer) if 'completer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(completer) else 'completer', 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    return


def test_completer4(mio):
    completer = Completer(mio)
    @py_assert1 = completer.complete
    @py_assert3 = 'Root asdf '
    @py_assert5 = 0
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert9 = @py_assert7 is None
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.complete\n}(%(py4)s, %(py6)s)\n} is %(py10)s', ), (@py_assert7, None)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(completer) if 'completer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(completer) else 'completer', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py10': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    return


def test_completer5(mio):
    completer = Completer(mio)
    @py_assert1 = completer.complete
    @py_assert3 = ''
    @py_assert5 = 0
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 'Core'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.complete\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(completer) if 'completer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(completer) else 'completer', 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = completer.complete
    @py_assert3 = ''
    @py_assert7 = completer.matches
    @py_assert9 = len(@py_assert7)
    @py_assert11 = @py_assert1(@py_assert3, @py_assert9)
    @py_assert13 = @py_assert11 is None
    if not @py_assert13:
        @py_format15 = @pytest_ar._call_reprcompare(('is',), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py2)s\n{%(py2)s = %(py0)s.complete\n}(%(py4)s, %(py10)s\n{%(py10)s = %(py5)s(%(py8)s\n{%(py8)s = %(py6)s.matches\n})\n})\n} is %(py14)s',), (@py_assert11, None)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(completer) if 'completer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(completer) else 'completer', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(completer) if 'completer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(completer) else 'completer', 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None', 'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    return


def test_completer6(mio, capfd):
    completer = Completer(mio)
    completer.display_matches('Root', ['Root Core', 'Root Types'], 10)
    out, err = capfd.readouterr()
    @py_assert2 = '\n Core        Types      \nmio> '
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (out, @py_assert2)) % {'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_completer7(mio, capfd):
    completer = Completer(mio)
    completer.display_matches('Root', ['Root Core'] * 100, 9)
    out, err = capfd.readouterr()
    @py_assert1 = out.split()[:-1]
    @py_assert3 = set(@py_assert1)
    @py_assert7 = ['Core']
    @py_assert9 = set(@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    return