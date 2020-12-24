# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/core/test_path.py
# Compiled at: 2013-12-04 07:18:22
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import raises
from os import getcwd, path
from mio.errors import TypeError
from mio.core.path import listdir

def test_path(mio):
    p = mio.eval('Path')
    @py_assert1 = p.value
    @py_assert5 = getcwd()
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py6)s\n{%(py6)s = %(py4)s()\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(getcwd) if 'getcwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getcwd) else 'getcwd', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    return


def test_repr(mio):
    @py_assert2 = mio.eval
    @py_assert4 = 'Path'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = repr(@py_assert6)
    @py_assert11 = 'Path({0:s})'
    @py_assert13 = @py_assert11.format
    @py_assert18 = getcwd()
    @py_assert20 = unicode(@py_assert18)
    @py_assert22 = repr(@py_assert20)
    @py_assert24 = @py_assert13(@py_assert22)
    @py_assert10 = @py_assert8 == @py_assert24
    if not @py_assert10:
        @py_format26 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} == %(py25)s\n{%(py25)s = %(py14)s\n{%(py14)s = %(py12)s.format\n}(%(py23)s\n{%(py23)s = %(py15)s(%(py21)s\n{%(py21)s = %(py16)s(%(py19)s\n{%(py19)s = %(py17)s()\n})\n})\n})\n}',), (@py_assert8, @py_assert24)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py19': @pytest_ar._saferepr(@py_assert18), 'py23': @pytest_ar._saferepr(@py_assert22), 'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py25': @pytest_ar._saferepr(@py_assert24), 'py3': @pytest_ar._saferepr(@py_assert2), 'py16': @pytest_ar._saferepr(unicode) if 'unicode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(unicode) else 'unicode', 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11), 'py17': @pytest_ar._saferepr(getcwd) if 'getcwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getcwd) else 'getcwd', 'py15': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py21': @pytest_ar._saferepr(@py_assert20)}
        @py_format28 = 'assert %(py27)s' % {'py27': @py_format26}
        raise AssertionError(@pytest_ar._format_explanation(@py_format28))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert18 = @py_assert20 = @py_assert22 = @py_assert24 = None
    return


def test_str(mio):
    @py_assert2 = mio.eval
    @py_assert4 = 'Path'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = str(@py_assert6)
    @py_assert13 = getcwd()
    @py_assert15 = str(@py_assert13)
    @py_assert10 = @py_assert8 == @py_assert15
    if not @py_assert10:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.eval\n}(%(py5)s)\n})\n} == %(py16)s\n{%(py16)s = %(py11)s(%(py14)s\n{%(py14)s = %(py12)s()\n})\n}',), (@py_assert8, @py_assert15)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py0': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py1': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py3': @pytest_ar._saferepr(@py_assert2), 'py16': @pytest_ar._saferepr(@py_assert15), 'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(getcwd) if 'getcwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getcwd) else 'getcwd'}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert13 = @py_assert15 = None
    return


def test_clone1(mio):
    p = mio.eval('Path clone("/tmp/foo.txt")')
    @py_assert1 = p.value
    @py_assert4 = '/tmp/foo.txt'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_clone2(mio):
    p = mio.eval('Path clone("~/foo.txt", True)')
    @py_assert1 = p.value
    @py_assert5 = path.expanduser
    @py_assert7 = '~/foo.txt'
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert3 = @py_assert1 == @py_assert9
    if not @py_assert3:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s.expanduser\n}(%(py8)s)\n}', ), (@py_assert1, @py_assert9)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path', 'py6': @pytest_ar._saferepr(@py_assert5), 'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    return


def test_join(mio):
    p = mio.eval('p = Path clone("/tmp/foo")')
    @py_assert1 = p.value
    @py_assert4 = '/tmp/foo'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    pp = mio.eval('pp = p join("bar.txt")')
    @py_assert1 = pp.value
    @py_assert4 = '/tmp/foo/bar.txt'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(pp) if 'pp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pp) else 'pp', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_open1(mio, tmpdir):
    foo = tmpdir.ensure('foo.txt')
    with foo.open('w') as (f):
        f.write('Hello World!')
    p = mio.eval(('p = Path clone("{0:s}")').format(str(foo)))
    @py_assert1 = p.value
    @py_assert6 = str(foo)
    @py_assert3 = @py_assert1 == @py_assert6
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}', ), (@py_assert1, @py_assert6)) % {'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py5': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    f = mio.eval('f = p open("r")')
    s = mio.eval('s = f read()')
    @py_assert2 = 'Hello World!'
    @py_assert1 = s == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (s, @py_assert2)) % {'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_open2(mio, tmpdir):
    p = mio.eval(('p = Path clone("{0:s}")').format(str(tmpdir)))
    @py_assert1 = p.value
    @py_assert6 = str(tmpdir)
    @py_assert3 = @py_assert1 == @py_assert6
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}', ), (@py_assert1, @py_assert6)) % {'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py5': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    with raises(TypeError):
        mio.eval('f = p open("r")', reraise=True)
    return


def test_list1(mio, tmpdir):
    tmpdir.ensure('foo.txt')
    tmpdir.ensure('bar.txt')
    p = mio.eval(('p = Path clone("{0:s}")').format(str(tmpdir)))
    @py_assert1 = p.value
    @py_assert6 = str(tmpdir)
    @py_assert3 = @py_assert1 == @py_assert6
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}',), (@py_assert1, @py_assert6)) % {'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py5': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    fs = mio.eval('fs = p list()')
    @py_assert2 = list(fs)
    @py_assert9 = str(tmpdir)
    @py_assert11 = listdir(@py_assert9)
    @py_assert13 = list(@py_assert11)
    @py_assert4 = @py_assert2 == @py_assert13
    if not @py_assert4:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py14)s\n{%(py14)s = %(py5)s(%(py12)s\n{%(py12)s = %(py6)s(%(py10)s\n{%(py10)s = %(py7)s(%(py8)s)\n})\n})\n}',), (@py_assert2, @py_assert13)) % {'py8': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir', 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(fs) if 'fs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fs) else 'fs', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py6': @pytest_ar._saferepr(listdir) if 'listdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(listdir) else 'listdir', 'py7': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert9 = @py_assert11 = @py_assert13 = None
    return


def test_list2(mio, tmpdir):
    tmpdir.ensure('foo.txt')
    tmpdir.ensure('bar.txt')
    tmpdir.ensure('baz.csv')
    p = mio.eval(('p = Path clone("{0:s}")').format(str(tmpdir)))
    @py_assert1 = p.value
    @py_assert6 = str(tmpdir)
    @py_assert3 = @py_assert1 == @py_assert6
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}',), (@py_assert1, @py_assert6)) % {'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py5': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    fs = mio.eval('fs = p list("*.txt")')
    @py_assert2 = list(fs)
    @py_assert9 = str(tmpdir)
    @py_assert11 = '*.txt'
    @py_assert13 = listdir(@py_assert9, @py_assert11)
    @py_assert15 = list(@py_assert13)
    @py_assert4 = @py_assert2 == @py_assert15
    if not @py_assert4:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py16)s\n{%(py16)s = %(py5)s(%(py14)s\n{%(py14)s = %(py6)s(%(py10)s\n{%(py10)s = %(py7)s(%(py8)s)\n}, %(py12)s)\n})\n}',), (@py_assert2, @py_assert15)) % {'py8': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir', 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(fs) if 'fs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fs) else 'fs', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py16': @pytest_ar._saferepr(@py_assert15), 'py5': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py6': @pytest_ar._saferepr(listdir) if 'listdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(listdir) else 'listdir', 'py7': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    return


def test_list3(mio, tmpdir):
    tmpdir.ensure('foo.txt')
    tmpdir.ensure('bar', dir=True).ensure('bar.txt')
    tmpdir.ensure('baz', dir=True).ensure('baz.txt')
    p = mio.eval(('p = Path clone("{0:s}")').format(str(tmpdir)))
    @py_assert1 = p.value
    @py_assert6 = str(tmpdir)
    @py_assert3 = @py_assert1 == @py_assert6
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}',), (@py_assert1, @py_assert6)) % {'py0': @pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py5': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    fs = mio.eval('fs = p list(None, True)')
    @py_assert2 = list(fs)
    @py_assert9 = str(tmpdir)
    @py_assert12 = listdir(@py_assert9, rec=True)
    @py_assert14 = list(@py_assert12)
    @py_assert4 = @py_assert2 == @py_assert14
    if not @py_assert4:
        @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py15)s\n{%(py15)s = %(py5)s(%(py13)s\n{%(py13)s = %(py6)s(%(py10)s\n{%(py10)s = %(py7)s(%(py8)s)\n}, rec=%(py11)s)\n})\n}',), (@py_assert2, @py_assert14)) % {'py8': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir', 'py11': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True', 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(fs) if 'fs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fs) else 'fs', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py6': @pytest_ar._saferepr(listdir) if 'listdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(listdir) else 'listdir', 'py7': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py13': @pytest_ar._saferepr(@py_assert12), 'py15': @pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert4 = @py_assert9 = @py_assert12 = @py_assert14 = None
    return