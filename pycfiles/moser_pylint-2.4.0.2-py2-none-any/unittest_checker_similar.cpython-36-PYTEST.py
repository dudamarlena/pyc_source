# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_similar.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 4712 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys
from contextlib import redirect_stdout
from io import StringIO
from os.path import abspath, dirname, join
import pytest
from pylint.checkers import similar
SIMILAR1 = join(dirname(abspath(__file__)), 'input', 'similar1')
SIMILAR2 = join(dirname(abspath(__file__)), 'input', 'similar2')
MULTILINE = join(dirname(abspath(__file__)), 'input', 'multiline-import')
HIDE_CODE_WITH_IMPORTS = join(dirname(abspath(__file__)), 'input', 'hide_code_with_imports.py')

def test_ignore_comments():
    output = StringIO()
    with redirect_stdout(output):
        with pytest.raises(SystemExit) as (ex):
            similar.Run(['--ignore-comments', SIMILAR1, SIMILAR2])
    @py_assert1 = ex.value
    @py_assert3 = @py_assert1.code
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=33)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(ex) if 'ex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ex) else 'ex',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = output.getvalue
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.strip
    @py_assert7 = @py_assert5()
    @py_assert10 = "\n10 similar lines in 2 files\n==%s:0\n==%s:0\n   import one\n   from two import two\n   three\n   four\n   five\n   six\n   seven\n   eight\n   nine\n   ''' ten\nTOTAL lines=60 duplicates=10 percent=16.67\n"
    @py_assert12 = (
     SIMILAR1, SIMILAR2)
    @py_assert14 = @py_assert10 % @py_assert12
    @py_assert15 = @py_assert14.strip
    @py_assert17 = @py_assert15()
    @py_assert9 = @py_assert7 == @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=34)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n}.strip\n}()\n} == %(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = (%(py11)s %% %(py13)s).strip\n}()\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = @py_assert17 = None


def test_ignore_docsrings():
    output = StringIO()
    with redirect_stdout(output):
        with pytest.raises(SystemExit) as (ex):
            similar.Run(['--ignore-docstrings', SIMILAR1, SIMILAR2])
    @py_assert1 = ex.value
    @py_assert3 = @py_assert1.code
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=62)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(ex) if 'ex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ex) else 'ex',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = output.getvalue
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.strip
    @py_assert7 = @py_assert5()
    @py_assert10 = "\n8 similar lines in 2 files\n==%s:6\n==%s:6\n   seven\n   eight\n   nine\n   ''' ten\n   ELEVEN\n   twelve '''\n   thirteen\n   fourteen\n\n5 similar lines in 2 files\n==%s:0\n==%s:0\n   import one\n   from two import two\n   three\n   four\n   five\nTOTAL lines=60 duplicates=13 percent=21.67\n"
    @py_assert12 = (
     SIMILAR1, SIMILAR2)
    @py_assert14 = 2
    @py_assert16 = @py_assert12 * @py_assert14
    @py_assert17 = @py_assert10 % @py_assert16
    @py_assert18 = @py_assert17.strip
    @py_assert20 = @py_assert18()
    @py_assert9 = @py_assert7 == @py_assert20
    if @py_assert9 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=63)
    if not @py_assert9:
        @py_format22 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n}.strip\n}()\n} == %(py21)s\n{%(py21)s = %(py19)s\n{%(py19)s = (%(py11)s %% (%(py13)s * %(py15)s)).strip\n}()\n}', ), (@py_assert7, @py_assert20)) % {'py0':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py19':@pytest_ar._saferepr(@py_assert18),  'py21':@pytest_ar._saferepr(@py_assert20)}
        @py_format24 = 'assert %(py23)s' % {'py23': @py_format22}
        raise AssertionError(@pytest_ar._format_explanation(@py_format24))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = @py_assert18 = @py_assert20 = None


def test_ignore_imports():
    output = StringIO()
    with redirect_stdout(output):
        with pytest.raises(SystemExit) as (ex):
            similar.Run(['--ignore-imports', SIMILAR1, SIMILAR2])
    @py_assert1 = ex.value
    @py_assert3 = @py_assert1.code
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=98)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(ex) if 'ex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ex) else 'ex',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = output.getvalue
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.strip
    @py_assert7 = @py_assert5()
    @py_assert10 = '\nTOTAL lines=60 duplicates=0 percent=0.00\n'
    @py_assert12 = @py_assert10.strip
    @py_assert14 = @py_assert12()
    @py_assert9 = @py_assert7 == @py_assert14
    if @py_assert9 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=99)
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n}.strip\n}()\n} == %(py15)s\n{%(py15)s = %(py13)s\n{%(py13)s = %(py11)s.strip\n}()\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_multiline_imports():
    output = StringIO()
    with redirect_stdout(output):
        with pytest.raises(SystemExit) as (ex):
            similar.Run([MULTILINE, MULTILINE])
    @py_assert1 = ex.value
    @py_assert3 = @py_assert1.code
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=111)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(ex) if 'ex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ex) else 'ex',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = output.getvalue
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.strip
    @py_assert7 = @py_assert5()
    @py_assert10 = '\n8 similar lines in 2 files\n==%s:0\n==%s:0\n   from foo import (\n     bar,\n     baz,\n     quux,\n     quuux,\n     quuuux,\n     quuuuux,\n   )\nTOTAL lines=16 duplicates=8 percent=50.00\n'
    @py_assert12 = (
     MULTILINE, MULTILINE)
    @py_assert14 = @py_assert10 % @py_assert12
    @py_assert15 = @py_assert14.strip
    @py_assert17 = @py_assert15()
    @py_assert9 = @py_assert7 == @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=112)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n}.strip\n}()\n} == %(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = (%(py11)s %% %(py13)s).strip\n}()\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = @py_assert17 = None


def test_ignore_multiline_imports():
    output = StringIO()
    with redirect_stdout(output):
        with pytest.raises(SystemExit) as (ex):
            similar.Run(['--ignore-imports', MULTILINE, MULTILINE])
    @py_assert1 = ex.value
    @py_assert3 = @py_assert1.code
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=138)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(ex) if 'ex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ex) else 'ex',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = output.getvalue
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.strip
    @py_assert7 = @py_assert5()
    @py_assert10 = '\nTOTAL lines=16 duplicates=0 percent=0.00\n'
    @py_assert12 = @py_assert10.strip
    @py_assert14 = @py_assert12()
    @py_assert9 = @py_assert7 == @py_assert14
    if @py_assert9 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=139)
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n}.strip\n}()\n} == %(py15)s\n{%(py15)s = %(py13)s\n{%(py13)s = %(py11)s.strip\n}()\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_no_hide_code_with_imports():
    output = StringIO()
    with redirect_stdout(output):
        with pytest.raises(SystemExit) as (ex):
            similar.Run(['--ignore-imports'] + 2 * [HIDE_CODE_WITH_IMPORTS])
    @py_assert1 = ex.value
    @py_assert3 = @py_assert1.code
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=151)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(ex) if 'ex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ex) else 'ex',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = 'TOTAL lines=32 duplicates=16 percent=50.00'
    @py_assert4 = output.getvalue
    @py_assert6 = @py_assert4()
    @py_assert2 = @py_assert0 in @py_assert6
    if @py_assert2 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=152)
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.getvalue\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_ignore_nothing():
    output = StringIO()
    with redirect_stdout(output):
        with pytest.raises(SystemExit) as (ex):
            similar.Run([SIMILAR1, SIMILAR2])
    @py_assert1 = ex.value
    @py_assert3 = @py_assert1.code
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=159)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.code\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(ex) if 'ex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ex) else 'ex',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = output.getvalue
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.strip
    @py_assert7 = @py_assert5()
    @py_assert10 = '\n5 similar lines in 2 files\n==%s:0\n==%s:0\n   import one\n   from two import two\n   three\n   four\n   five\nTOTAL lines=60 duplicates=5 percent=8.33\n'
    @py_assert12 = (
     SIMILAR1, SIMILAR2)
    @py_assert14 = @py_assert10 % @py_assert12
    @py_assert15 = @py_assert14.strip
    @py_assert17 = @py_assert15()
    @py_assert9 = @py_assert7 == @py_assert17
    if @py_assert9 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=160)
    if not @py_assert9:
        @py_format19 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n}.strip\n}()\n} == %(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = (%(py11)s %% %(py13)s).strip\n}()\n}', ), (@py_assert7, @py_assert17)) % {'py0':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = @py_assert17 = None


def test_help():
    output = StringIO()
    with redirect_stdout(output):
        try:
            similar.Run(['--help'])
        except SystemExit as ex:
            @py_assert1 = ex.code
            @py_assert4 = 0
            @py_assert3 = @py_assert1 == @py_assert4
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=185)
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(ex) if 'ex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ex) else 'ex',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None
        else:
            pytest.fail('not system exit')


def test_no_args():
    output = StringIO()
    with redirect_stdout(output):
        try:
            similar.Run([])
        except SystemExit as ex:
            @py_assert1 = ex.code
            @py_assert4 = 1
            @py_assert3 = @py_assert1 == @py_assert4
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_similar.py', lineno=196)
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(ex) if 'ex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ex) else 'ex',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None
        else:
            pytest.fail('not system exit')