# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_interface.py
# Compiled at: 2019-03-12 12:20:24
# Size of source mod 2**32: 2655 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pkgutil, pytest
from funcy.compat import PY2, PY3
import funcy
from funcy import py2, py3
from funcy.py3 import cat, lcat, count_reps, is_iter, is_list
exclude = ('compat', 'cross', '_inspect', 'py2', 'py3', 'simple_funcs', 'funcmakers')
module_names = list(name for _, name, _ in pkgutil.iter_modules(funcy.__path__) if name not in exclude)
modules = [getattr(funcy, name) for name in module_names]

def test_match():
    @py_assert1 = funcy.__all__
    @py_assert4 = py2 if PY2 else py3
    @py_assert6 = @py_assert4.__all__
    @py_assert3 = @py_assert1 == @py_assert6
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=18)
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__all__\n} == %(py7)s\n{%(py7)s = %(py5)s.__all__\n}', ), (@py_assert1, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(funcy) if 'funcy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(funcy) else 'funcy'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = None


@pytest.mark.skipif(PY2, reason='modules use python 3 internally')
def test_full_py3():
    @py_assert2 = funcy.__all__
    @py_assert4 = sorted(@py_assert2)
    @py_assert9 = (m.__all__ for m in modules)
    @py_assert11 = lcat(@py_assert9)
    @py_assert13 = [
     'lzip']
    @py_assert15 = @py_assert11 + @py_assert13
    @py_assert16 = sorted(@py_assert15)
    @py_assert6 = @py_assert4 == @py_assert16
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=23)
    if not @py_assert6:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.__all__\n})\n} == %(py17)s\n{%(py17)s = %(py7)s((%(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n} + %(py14)s))\n}',), (@py_assert4, @py_assert16)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py17': @pytest_ar._saferepr(@py_assert16), 'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py8': @pytest_ar._saferepr(lcat) if 'lcat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lcat) else 'lcat', 'py1': @pytest_ar._saferepr(funcy) if 'funcy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(funcy) else 'funcy', 'py14': @pytest_ar._saferepr(@py_assert13), 'py12': @pytest_ar._saferepr(@py_assert11), 'py7': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None


def test_full():
    @py_assert2 = py2.__all__
    @py_assert4 = len(@py_assert2)
    @py_assert9 = py3.__all__
    @py_assert11 = len(@py_assert9)
    @py_assert6 = @py_assert4 == @py_assert11
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=27)
    if not @py_assert6:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.__all__\n})\n} == %(py12)s\n{%(py12)s = %(py7)s(%(py10)s\n{%(py10)s = %(py8)s.__all__\n})\n}',), (@py_assert4, @py_assert11)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py8': @pytest_ar._saferepr(py3) if 'py3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py3) else 'py3', 'py1': @pytest_ar._saferepr(py2) if 'py2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py2) else 'py2', 'py12': @pytest_ar._saferepr(@py_assert11), 'py7': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = None


def test_name_clashes():
    counts = count_reps(cat(m.__all__ for m in modules))
    clashes = [name for name, c in counts.items() if c > 1]
    @py_assert1 = not clashes
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=33)
    if not @py_assert1:
        @py_format2 = (@pytest_ar._format_assertmsg('names clash for ' + ', '.join(clashes)) + '\n>assert not %(py0)s') % {'py0': @pytest_ar._saferepr(clashes) if 'clashes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(clashes) else 'clashes'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None


def test_renames():
    inames = [n for n in py2.__all__ if n.startswith('i')]
    ipairs = [n[1:] for n in inames if n[1:] in py2.__all__]
    for name in inames:
        if name != 'izip':
            @py_assert1 = []
            @py_assert5 = py3.__all__
            @py_assert3 = name in @py_assert5
            @py_assert0 = @py_assert3
            if not @py_assert3:
                @py_assert10 = name[1:]
                @py_assert14 = py3.__all__
                @py_assert12 = @py_assert10 in @py_assert14
                @py_assert0 = @py_assert12
            if @py_assert0 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=42)
            if not @py_assert0:
                @py_format7 = @pytest_ar._call_reprcompare(('in',), (@py_assert3,), ('%(py2)s in %(py6)s\n{%(py6)s = %(py4)s.__all__\n}',), (name, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name', 'py4': @pytest_ar._saferepr(py3) if 'py3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py3) else 'py3'}
                @py_format9 = '%(py8)s' % {'py8': @py_format7}
                @py_assert1.append(@py_format9)
                if not @py_assert3:
                    @py_format16 = @pytest_ar._call_reprcompare(('in',), (@py_assert12,), ('%(py11)s in %(py15)s\n{%(py15)s = %(py13)s.__all__\n}',), (@py_assert10, @py_assert14)) % {'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py13': @pytest_ar._saferepr(py3) if 'py3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py3) else 'py3'}
                    @py_format18 = '%(py17)s' % {'py17': @py_format16}
                    @py_assert1.append(@py_format18)
                @py_format19 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
                @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
                raise AssertionError(@pytest_ar._format_explanation(@py_format21))
            @py_assert0 = @py_assert1 = @py_assert3 = @py_assert5 = @py_assert10 = @py_assert12 = @py_assert14 = None

    for name in ipairs:
        @py_assert3 = py3.__all__
        @py_assert1 = name in @py_assert3
        if @py_assert1 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=45)
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s.__all__\n}',), (name, @py_assert3)) % {'py2': @pytest_ar._saferepr(py3) if 'py3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py3) else 'py3', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name'}
            @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert0 = 'l'
        @py_assert3 = @py_assert0 + name
        @py_assert6 = py3.__all__
        @py_assert4 = @py_assert3 in @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=46)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('in',), (@py_assert4,), ('(%(py1)s + %(py2)s) in %(py7)s\n{%(py7)s = %(py5)s.__all__\n}',), (@py_assert3, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name', 'py5': @pytest_ar._saferepr(py3) if 'py3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py3) else 'py3'}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert3 = @py_assert4 = @py_assert6 = None

    lnames = [n for n in py3.__all__ if n.startswith('l')]
    lpairs = [n[1:] for n in lnames if n[1:] in py3.__all__]
    for name in lnames:
        if name != 'lzip':
            @py_assert1 = []
            @py_assert5 = py2.__all__
            @py_assert3 = name in @py_assert5
            @py_assert0 = @py_assert3
            if not @py_assert3:
                @py_assert10 = name[1:]
                @py_assert14 = py2.__all__
                @py_assert12 = @py_assert10 in @py_assert14
                @py_assert0 = @py_assert12
            if @py_assert0 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=53)
            if not @py_assert0:
                @py_format7 = @pytest_ar._call_reprcompare(('in',), (@py_assert3,), ('%(py2)s in %(py6)s\n{%(py6)s = %(py4)s.__all__\n}',), (name, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name', 'py4': @pytest_ar._saferepr(py2) if 'py2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py2) else 'py2'}
                @py_format9 = '%(py8)s' % {'py8': @py_format7}
                @py_assert1.append(@py_format9)
                if not @py_assert3:
                    @py_format16 = @pytest_ar._call_reprcompare(('in',), (@py_assert12,), ('%(py11)s in %(py15)s\n{%(py15)s = %(py13)s.__all__\n}',), (@py_assert10, @py_assert14)) % {'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py13': @pytest_ar._saferepr(py2) if 'py2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py2) else 'py2'}
                    @py_format18 = '%(py17)s' % {'py17': @py_format16}
                    @py_assert1.append(@py_format18)
                @py_format19 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
                @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
                raise AssertionError(@pytest_ar._format_explanation(@py_format21))
            @py_assert0 = @py_assert1 = @py_assert3 = @py_assert5 = @py_assert10 = @py_assert12 = @py_assert14 = None

    for name in lpairs:
        @py_assert3 = py2.__all__
        @py_assert1 = name in @py_assert3
        if @py_assert1 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=56)
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s.__all__\n}',), (name, @py_assert3)) % {'py2': @pytest_ar._saferepr(py2) if 'py2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py2) else 'py2', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name'}
            @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert0 = 'i'
        @py_assert3 = @py_assert0 + name
        @py_assert6 = py2.__all__
        @py_assert4 = @py_assert3 in @py_assert6
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=57)
        if not @py_assert4:
            @py_format8 = @pytest_ar._call_reprcompare(('in',), (@py_assert4,), ('(%(py1)s + %(py2)s) in %(py7)s\n{%(py7)s = %(py5)s.__all__\n}',), (@py_assert3, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name', 'py5': @pytest_ar._saferepr(py2) if 'py2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py2) else 'py2'}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert3 = @py_assert4 = @py_assert6 = None

    @py_assert2 = py2.__all__
    @py_assert4 = set(@py_assert2)
    @py_assert8 = py3.__all__
    @py_assert10 = set(@py_assert8)
    @py_assert12 = @py_assert4 - @py_assert10
    @py_assert16 = set(inames)
    @py_assert13 = @py_assert12 <= @py_assert16
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=60)
    if not @py_assert13:
        @py_format18 = @pytest_ar._call_reprcompare(('<=',), (@py_assert13,), ('(%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.__all__\n})\n} - %(py11)s\n{%(py11)s = %(py6)s(%(py9)s\n{%(py9)s = %(py7)s.__all__\n})\n}) <= %(py17)s\n{%(py17)s = %(py14)s(%(py15)s)\n}',), (@py_assert12, @py_assert16)) % {'py15': @pytest_ar._saferepr(inames) if 'inames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inames) else 'inames', 'py14': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py17': @pytest_ar._saferepr(@py_assert16), 'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py1': @pytest_ar._saferepr(py2) if 'py2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py2) else 'py2', 'py6': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(py3) if 'py3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py3) else 'py3', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = @py_assert16 = None
    @py_assert2 = py3.__all__
    @py_assert4 = set(@py_assert2)
    @py_assert8 = py2.__all__
    @py_assert10 = set(@py_assert8)
    @py_assert12 = @py_assert4 - @py_assert10
    @py_assert16 = set(lnames)
    @py_assert19 = [
     'zip_values', 'zip_dicts']
    @py_assert21 = set(@py_assert19)
    @py_assert23 = @py_assert16 | @py_assert21
    @py_assert13 = @py_assert12 <= @py_assert23
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=62)
    if not @py_assert13:
        @py_format24 = @pytest_ar._call_reprcompare(('<=',), (@py_assert13,), ('(%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.__all__\n})\n} - %(py11)s\n{%(py11)s = %(py6)s(%(py9)s\n{%(py9)s = %(py7)s.__all__\n})\n}) <= (%(py17)s\n{%(py17)s = %(py14)s(%(py15)s)\n} | %(py22)s\n{%(py22)s = %(py18)s(%(py20)s)\n})',), (@py_assert12, @py_assert23)) % {'py7': @pytest_ar._saferepr(py2) if 'py2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py2) else 'py2', 'py14': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py6': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py22': @pytest_ar._saferepr(@py_assert21), 'py20': @pytest_ar._saferepr(@py_assert19), 'py11': @pytest_ar._saferepr(@py_assert10), 'py17': @pytest_ar._saferepr(@py_assert16), 'py1': @pytest_ar._saferepr(py3) if 'py3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py3) else 'py3', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py15': @pytest_ar._saferepr(lnames) if 'lnames' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lnames) else 'lnames', 'py9': @pytest_ar._saferepr(@py_assert8), 'py18': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = @py_assert16 = @py_assert19 = @py_assert21 = @py_assert23 = None


def test_docs():
    exports = [(name, getattr(funcy, name)) for name in funcy.__all__ if name not in ('print_errors',
                                                                                      'print_durations',
                                                                                      'ErrorRateExceeded') and getattr(funcy, name).__module__ not in ('funcy.types',
                                                                                                                                                       'funcy.primitives')]
    @py_assert0 = [name for name, f in exports if f.__name__ in ('<lambda>', '_decorator')]
    @py_assert3 = []
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=70)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = [name for name, f in exports if f.__doc__ is None]
    @py_assert3 = []
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=71)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_list_iter():
    @py_assert2 = py2.map
    @py_assert4 = None
    @py_assert6 = []
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = is_list(@py_assert8)
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=75)
    if not @py_assert10:
        @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.map\n}(%(py5)s, %(py7)s)\n})\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(is_list) if 'is_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_list) else 'is_list', 'py1': @pytest_ar._saferepr(py2) if 'py2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py2) else 'py2', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert2 = py3.map
    @py_assert4 = None
    @py_assert6 = []
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = is_iter(@py_assert8)
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=76)
    if not @py_assert10:
        @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.map\n}(%(py5)s, %(py7)s)\n})\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(is_iter) if 'is_iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_iter) else 'is_iter', 'py1': @pytest_ar._saferepr(py3) if 'py3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(py3) else 'py3', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert2 = funcy.map
    @py_assert4 = None
    @py_assert6 = []
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = is_list(@py_assert8)
    @py_assert12 = @py_assert10 == PY2
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=77)
    if not @py_assert12:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.map\n}(%(py5)s, %(py7)s)\n})\n} == %(py13)s',), (@py_assert10, PY2)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(is_list) if 'is_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_list) else 'is_list', 'py13': @pytest_ar._saferepr(PY2) if 'PY2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(PY2) else 'PY2', 'py1': @pytest_ar._saferepr(funcy) if 'funcy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(funcy) else 'funcy', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert2 = funcy.map
    @py_assert4 = None
    @py_assert6 = []
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = is_iter(@py_assert8)
    @py_assert12 = @py_assert10 == PY3
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/suor/projects/funcy/tests/test_interface.py', lineno=78)
    if not @py_assert12:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.map\n}(%(py5)s, %(py7)s)\n})\n} == %(py13)s',), (@py_assert10, PY3)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(is_iter) if 'is_iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_iter) else 'is_iter', 'py13': @pytest_ar._saferepr(PY3) if 'PY3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(PY3) else 'PY3', 'py1': @pytest_ar._saferepr(funcy) if 'funcy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(funcy) else 'funcy', 'py9': @pytest_ar._saferepr(@py_assert8), 'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None