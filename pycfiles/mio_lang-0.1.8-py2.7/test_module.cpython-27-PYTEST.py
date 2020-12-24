# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/core/test_module.py
# Compiled at: 2013-12-08 17:19:04
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_module(mio, tmpdir, capfd):
    with tmpdir.ensure('foo.mio').open('w') as (f):
        f.write('\n            hello = block(\n                print("Hello World!")\n            )\n        ')
    foo = mio.eval(('foo = Module clone("foo", "{0:s}")').format(str(tmpdir.join('foo.mio'))))
    @py_assert2 = repr(foo)
    @py_assert5 = 'Module(name={0:s}, file={1:s})'
    @py_assert7 = @py_assert5.format
    @py_assert10 = 'foo'
    @py_assert12 = repr(@py_assert10)
    @py_assert17 = tmpdir.join
    @py_assert19 = 'foo.mio'
    @py_assert21 = @py_assert17(@py_assert19)
    @py_assert23 = str(@py_assert21)
    @py_assert25 = repr(@py_assert23)
    @py_assert27 = @py_assert7(@py_assert12, @py_assert25)
    @py_assert4 = @py_assert2 == @py_assert27
    if not @py_assert4:
        @py_format29 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py28)s\n{%(py28)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(%(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}, %(py26)s\n{%(py26)s = %(py14)s(%(py24)s\n{%(py24)s = %(py15)s(%(py22)s\n{%(py22)s = %(py18)s\n{%(py18)s = %(py16)s.join\n}(%(py20)s)\n})\n})\n})\n}',), (@py_assert2, @py_assert27)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py9': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py18': @pytest_ar._saferepr(@py_assert17), 'py11': @pytest_ar._saferepr(@py_assert10), 'py28': @pytest_ar._saferepr(@py_assert27), 'py24': @pytest_ar._saferepr(@py_assert23), 'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py3': @pytest_ar._saferepr(@py_assert2), 'py16': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir', 'py22': @pytest_ar._saferepr(@py_assert21), 'py6': @pytest_ar._saferepr(@py_assert5), 'py15': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py26': @pytest_ar._saferepr(@py_assert25), 'py14': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py13': @pytest_ar._saferepr(@py_assert12), 'py20': @pytest_ar._saferepr(@py_assert19)}
        @py_format31 = 'assert %(py30)s' % {'py30': @py_format29}
        raise AssertionError(@pytest_ar._format_explanation(@py_format31))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert27 = None
    mio.eval('foo hello()')
    out, err = capfd.readouterr()
    @py_assert2 = 'Hello World!\n'
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (out, @py_assert2)) % {'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    mio.eval('del("foo")')
    return


def test_module_import(mio, tmpdir, capfd):
    with tmpdir.ensure('foo.mio').open('w') as (f):
        f.write('\n            hello = block(\n                print("Hello World!")\n            )\n        ')
    foo = mio.eval(('foo = Module clone("foo", "{0:s}")').format(str(tmpdir.join('foo.mio'))))
    @py_assert2 = repr(foo)
    @py_assert5 = 'Module(name={0:s}, file={1:s})'
    @py_assert7 = @py_assert5.format
    @py_assert10 = 'foo'
    @py_assert12 = repr(@py_assert10)
    @py_assert17 = tmpdir.join
    @py_assert19 = 'foo.mio'
    @py_assert21 = @py_assert17(@py_assert19)
    @py_assert23 = str(@py_assert21)
    @py_assert25 = repr(@py_assert23)
    @py_assert27 = @py_assert7(@py_assert12, @py_assert25)
    @py_assert4 = @py_assert2 == @py_assert27
    if not @py_assert4:
        @py_format29 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py28)s\n{%(py28)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(%(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}, %(py26)s\n{%(py26)s = %(py14)s(%(py24)s\n{%(py24)s = %(py15)s(%(py22)s\n{%(py22)s = %(py18)s\n{%(py18)s = %(py16)s.join\n}(%(py20)s)\n})\n})\n})\n}',), (@py_assert2, @py_assert27)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py9': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py18': @pytest_ar._saferepr(@py_assert17), 'py11': @pytest_ar._saferepr(@py_assert10), 'py28': @pytest_ar._saferepr(@py_assert27), 'py24': @pytest_ar._saferepr(@py_assert23), 'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py3': @pytest_ar._saferepr(@py_assert2), 'py16': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir', 'py22': @pytest_ar._saferepr(@py_assert21), 'py6': @pytest_ar._saferepr(@py_assert5), 'py15': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py26': @pytest_ar._saferepr(@py_assert25), 'py14': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py13': @pytest_ar._saferepr(@py_assert12), 'py20': @pytest_ar._saferepr(@py_assert19)}
        @py_format31 = 'assert %(py30)s' % {'py30': @py_format29}
        raise AssertionError(@pytest_ar._format_explanation(@py_format31))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert27 = None
    mio.eval('foo import("hello")')
    mio.eval('hello()')
    out, err = capfd.readouterr()
    @py_assert2 = 'Hello World!\n'
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (out, @py_assert2)) % {'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    mio.eval('del("foo")')
    return


def test_package(mio, tmpdir, capfd):
    path = tmpdir.ensure('foo', dir=True)
    with path.join('__init__.mio').open('w') as (f):
        f.write('\n            hello = block(\n                print("Hello World!")\n            )\n\n            bar = import(bar)\n        ')
    with path.join('bar.mio').open('w') as (f):
        f.write('\n            foobar = block(\n                print("Foobar!")\n            )\n        ')
    mio.eval(('Importer paths insert(0, "{0:s}")').format(str(tmpdir)))
    foo = mio.eval('foo = import(foo)')
    @py_assert2 = repr(foo)
    @py_assert5 = 'Module(name={0:s}, file={1:s})'
    @py_assert7 = @py_assert5.format
    @py_assert10 = 'foo'
    @py_assert12 = repr(@py_assert10)
    @py_assert17 = path.join
    @py_assert19 = '__init__.mio'
    @py_assert21 = @py_assert17(@py_assert19)
    @py_assert23 = str(@py_assert21)
    @py_assert25 = repr(@py_assert23)
    @py_assert27 = @py_assert7(@py_assert12, @py_assert25)
    @py_assert4 = @py_assert2 == @py_assert27
    if not @py_assert4:
        @py_format29 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py28)s\n{%(py28)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(%(py13)s\n{%(py13)s = %(py9)s(%(py11)s)\n}, %(py26)s\n{%(py26)s = %(py14)s(%(py24)s\n{%(py24)s = %(py15)s(%(py22)s\n{%(py22)s = %(py18)s\n{%(py18)s = %(py16)s.join\n}(%(py20)s)\n})\n})\n})\n}',), (@py_assert2, @py_assert27)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py9': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py18': @pytest_ar._saferepr(@py_assert17), 'py11': @pytest_ar._saferepr(@py_assert10), 'py28': @pytest_ar._saferepr(@py_assert27), 'py24': @pytest_ar._saferepr(@py_assert23), 'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(foo) if 'foo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(foo) else 'foo', 'py3': @pytest_ar._saferepr(@py_assert2), 'py16': @pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path', 'py22': @pytest_ar._saferepr(@py_assert21), 'py6': @pytest_ar._saferepr(@py_assert5), 'py15': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py26': @pytest_ar._saferepr(@py_assert25), 'py14': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py13': @pytest_ar._saferepr(@py_assert12), 'py20': @pytest_ar._saferepr(@py_assert19)}
        @py_format31 = 'assert %(py30)s' % {'py30': @py_format29}
        raise AssertionError(@pytest_ar._format_explanation(@py_format31))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert27 = None
    mio.eval('foo hello()')
    out, err = capfd.readouterr()
    @py_assert2 = 'Hello World!\n'
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (out, @py_assert2)) % {'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    mio.eval('foo bar foobar()')
    out, err = capfd.readouterr()
    @py_assert2 = 'Foobar!\n'
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (out, @py_assert2)) % {'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    mio.eval('del("foo")')
    return