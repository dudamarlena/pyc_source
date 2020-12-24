# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/core/test_ffi.py
# Compiled at: 2013-11-11 04:41:49
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from datetime import date

def test_ffi(mio):
    mio.eval('\ndate = FFI clone("date", """\nfrom datetime import date\n\n\n__all__ = ("today",)\n\n\ndef today():\n    return date.today().strftime("%B %d, %Y")\n""")\n    ')
    today = date.today().strftime('%B %d, %Y')
    @py_assert1 = mio.eval
    @py_assert3 = 'date today()'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == today
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, today)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py8': @pytest_ar._saferepr(today) if 'today' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(today) else 'today', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    mio.eval('del("date")')
    return


def test_ffi_repr(mio):
    mio.eval('\nfoo = FFI clone("foo", """\ndef foo():\n    return "Foobar!"\n""")\n    ')
    @py_assert2 = mio.eval
    @py_assert4 = 'foo'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = repr(@py_assert6)
    @py_assert11 = "FFI(name='foo', file=None)"
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    return


def test_ffi_attrs(mio):
    mio.eval('\nfoo = FFI clone("foo", """\nx = 1\n\n\ndef foo():\n    return "Foobar!"\n""")\n    ')
    @py_assert1 = mio.eval
    @py_assert3 = 'foo foo()'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'Foobar!'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = mio.eval
    @py_assert3 = 'foo x'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 1
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_ffi_fromfile(mio, tmpdir):
    with tmpdir.ensure('foo.py').open('w') as (f):
        f.write('\nx = 1\n\n\ndef foo():\n    return "Foobar!"\n')
    foo = mio.eval(('foo = FFI fromfile("{0:s}")').format(str(tmpdir.join('foo.py'))))
    @py_assert1 = foo.type
    @py_assert4 = 'FFI'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = foo.module
    @py_assert3 = @py_assert1 is not None
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is not',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.module\n} is not %(py4)s',), (@py_assert1, None)) % {'py0': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = foo.name
    @py_assert4 = 'foo'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = foo.file
    @py_assert6 = tmpdir.join
    @py_assert8 = 'foo.py'
    @py_assert10 = @py_assert6(@py_assert8)
    @py_assert12 = str(@py_assert10)
    @py_assert3 = @py_assert1 == @py_assert12
    if not @py_assert3:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.file\n} == %(py13)s\n{%(py13)s = %(py4)s(%(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s.join\n}(%(py9)s)\n})\n}',), (@py_assert1, @py_assert12)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py5': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = mio.eval
    @py_assert3 = 'foo foo()'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'Foobar!'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = mio.eval
    @py_assert3 = 'foo x'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 1
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_ffi_importall(mio):
    mio.eval('\ndate = FFI clone("date", """\nfrom datetime import date\n\n\ndef foo():\n    return "foo"\n\n\ndef today():\n    return date.today().strftime("%B %d, %Y")\n\n\n__all__ = ("today",)\n""")\n    ')
    @py_assert1 = mio.eval
    @py_assert3 = 'date keys'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = ['today']
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return