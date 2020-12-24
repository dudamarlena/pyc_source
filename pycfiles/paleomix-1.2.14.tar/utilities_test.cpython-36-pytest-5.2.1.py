# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/utilities_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 20382 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, operator, pytest, paleomix.common.utilities as utils

def test_safe_coerce_to_tuple__str():
    @py_assert1 = utils.safe_coerce_to_tuple
    @py_assert3 = 'foo'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = ('foo', )
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=37)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_tuple\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_safe_coerce_to_tuple__int():
    @py_assert1 = utils.safe_coerce_to_tuple
    @py_assert3 = 17
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = (17, )
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=41)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_tuple\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_safe_coerce_to_tuple__list():
    @py_assert1 = utils.safe_coerce_to_tuple
    @py_assert3 = [
     1, 3, 2]
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = (1, 3, 2)
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=45)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_tuple\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_safe_coerce_to_tuple__tuple():
    @py_assert1 = utils.safe_coerce_to_tuple
    @py_assert3 = (1, 3, 2)
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = (1, 3, 2)
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=49)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_tuple\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_safe_coerce_to_tuple__iterable():
    @py_assert1 = utils.safe_coerce_to_tuple
    @py_assert5 = 3
    @py_assert7 = range(@py_assert5)
    @py_assert9 = iter(@py_assert7)
    @py_assert11 = @py_assert1(@py_assert9)
    @py_assert14 = (0, 1, 2)
    @py_assert13 = @py_assert11 == @py_assert14
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=53)
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_tuple\n}(%(py10)s\n{%(py10)s = %(py3)s(%(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n})\n})\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter',  'py4':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


def test_safe_coerce_to_tuple__dict():
    @py_assert1 = utils.safe_coerce_to_tuple
    @py_assert3 = {1:2, 
     3:4}
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = (
     {1:2, 
      3:4},)
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=57)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_tuple\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_safe_coerce_to_frozenset__str():
    @py_assert1 = utils.safe_coerce_to_frozenset
    @py_assert3 = 'foo'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = ('foo', )
    @py_assert11 = frozenset(@py_assert9)
    @py_assert7 = @py_assert5 == @py_assert11
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=66)
    if not @py_assert7:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_frozenset\n}(%(py4)s)\n} == %(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n}', ), (@py_assert5, @py_assert11)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_safe_coerce_to_frozenset__unicode():
    @py_assert1 = utils.safe_coerce_to_frozenset
    @py_assert3 = 'foo'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = ('foo', )
    @py_assert11 = frozenset(@py_assert9)
    @py_assert7 = @py_assert5 == @py_assert11
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=70)
    if not @py_assert7:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_frozenset\n}(%(py4)s)\n} == %(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n}', ), (@py_assert5, @py_assert11)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_safe_coerce_to_frozenset__int():
    @py_assert1 = utils.safe_coerce_to_frozenset
    @py_assert3 = 17
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = (17, )
    @py_assert11 = frozenset(@py_assert9)
    @py_assert7 = @py_assert5 == @py_assert11
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=74)
    if not @py_assert7:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_frozenset\n}(%(py4)s)\n} == %(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n}', ), (@py_assert5, @py_assert11)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_safe_coerce_to_frozenset__list():
    @py_assert1 = utils.safe_coerce_to_frozenset
    @py_assert3 = [
     1, 3, 2]
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = (1, 3, 2)
    @py_assert11 = frozenset(@py_assert9)
    @py_assert7 = @py_assert5 == @py_assert11
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=78)
    if not @py_assert7:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_frozenset\n}(%(py4)s)\n} == %(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n}', ), (@py_assert5, @py_assert11)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_safe_coerce_to_frozenset__tuple():
    @py_assert1 = utils.safe_coerce_to_frozenset
    @py_assert3 = (1, 3, 2)
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = (1, 3, 2)
    @py_assert11 = frozenset(@py_assert9)
    @py_assert7 = @py_assert5 == @py_assert11
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=82)
    if not @py_assert7:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_frozenset\n}(%(py4)s)\n} == %(py12)s\n{%(py12)s = %(py8)s(%(py10)s)\n}', ), (@py_assert5, @py_assert11)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_safe_coerce_to_frozenset__iterable():
    @py_assert1 = utils.safe_coerce_to_frozenset
    @py_assert4 = 3
    @py_assert6 = range(@py_assert4)
    @py_assert8 = @py_assert1(@py_assert6)
    @py_assert12 = (0, 1, 2)
    @py_assert14 = frozenset(@py_assert12)
    @py_assert10 = @py_assert8 == @py_assert14
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=86)
    if not @py_assert10:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.safe_coerce_to_frozenset\n}(%(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n} == %(py15)s\n{%(py15)s = %(py11)s(%(py13)s)\n}', ), (@py_assert8, @py_assert14)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(frozenset) if 'frozenset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozenset) else 'frozenset',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_safe_coerce_to_frozenset__dict():
    with pytest.raises(TypeError):
        utils.safe_coerce_to_frozenset({1:2,  3:4})


def test_try_cast__int_to_int():
    @py_assert1 = utils.try_cast
    @py_assert3 = 17
    @py_assert6 = @py_assert1(@py_assert3, int)
    @py_assert9 = 17
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=100)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.try_cast\n}(%(py4)s, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_try_cast__float_to_int():
    @py_assert1 = utils.try_cast
    @py_assert3 = 17.3
    @py_assert6 = @py_assert1(@py_assert3, int)
    @py_assert9 = 17
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=104)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.try_cast\n}(%(py4)s, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_try_cast__good_str_to_int():
    @py_assert1 = utils.try_cast
    @py_assert3 = '17'
    @py_assert6 = @py_assert1(@py_assert3, int)
    @py_assert9 = 17
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=108)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.try_cast\n}(%(py4)s, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_try_cast__bad_str_to_int():
    @py_assert1 = utils.try_cast
    @py_assert3 = 'x17'
    @py_assert6 = @py_assert1(@py_assert3, int)
    @py_assert9 = 'x17'
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=112)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.try_cast\n}(%(py4)s, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_try_cast__list_to_int():
    @py_assert1 = utils.try_cast
    @py_assert3 = [
     1, 2, 3]
    @py_assert6 = @py_assert1(@py_assert3, int)
    @py_assert9 = [
     1, 2, 3]
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=116)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.try_cast\n}(%(py4)s, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_set_in__single_kw_in_empty_dictionary():
    value = {}
    utils.set_in(value, ['Foo'], 17)
    @py_assert2 = {'Foo': 17}
    @py_assert1 = value == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=127)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_set_in__two_kws_in_empty_dictionary():
    value = {}
    utils.set_in(value, ['Foo', 13], 17)
    @py_assert2 = {'Foo': {13: 17}}
    @py_assert1 = value == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=133)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_set_in__three_kws_in_empty_dictionary():
    value = {}
    utils.set_in(value, ['Foo', 13, (1, 2)], 17)
    @py_assert2 = {'Foo': {13: {(1, 2): 17}}}
    @py_assert1 = value == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=139)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_set_in__three_kws_in_partial_dictionary():
    value = {'Foo': {12: 0}}
    utils.set_in(value, ['Foo', 13, (1, 2)], 17)
    @py_assert2 = {'Foo': {12:0,  13:{(1, 2): 17}}}
    @py_assert1 = value == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=145)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    value = {'Foo': {13: {'Bar': None}}}
    utils.set_in(value, ['Foo', 13, (1, 2)], 17)
    @py_assert2 = {'Foo': {13: {(1, 2): 17, 'Bar': None}}}
    @py_assert1 = value == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=149)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_set_in__update_value_one_kw():
    value = {1: None}
    utils.set_in(value, [1], 3.14)
    @py_assert2 = {1: 3.14}
    @py_assert1 = value == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=155)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_set_in__update_value_two_kw():
    value = {1: {2: 3}}
    utils.set_in(value, [1, 2], 365)
    @py_assert2 = {1: {2: 365}}
    @py_assert1 = value == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=161)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_set_in__fail_on_no_kws():
    with pytest.raises(ValueError):
        utils.set_in({}, [], 17)


def test_set_in__fail_on_invalid_sub_dictionary_first_level():
    with pytest.raises(TypeError):
        utils.set_in(None, [1], 17)


def test_set_in__fail_on_invalid_sub_dictionary_second_level():
    with pytest.raises(TypeError):
        utils.set_in({1: None}, [1, 2], 17)


def test_set_in__fail_on_invalid_sub_dictionary_third_level():
    with pytest.raises(TypeError):
        utils.set_in({1: {2: None}}, [1, 2, 3], 17)


def test_set_in__iteratable_keywords():
    value = {}
    utils.set_in(value, iter(['Foo', 13, (1, 2)]), 17)
    @py_assert2 = {'Foo': {13: {(1, 2): 17}}}
    @py_assert1 = value == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=187)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (value, @py_assert2)) % {'py0':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_get_in__get_value_one_keyword():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: 2}
    @py_assert5 = [
     1]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 2
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=196)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_get_in__get_value_two_keywords():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: {2: 3}}
    @py_assert5 = [
     1, 2]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 3
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=200)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_get_in__get_value_three_keywords():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: {2: {3: 4}}}
    @py_assert5 = [
     1, 2, 3]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 4
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=204)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_get_in__get_default_one_keyword():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: 2}
    @py_assert5 = [
     2]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 is @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=208)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py6)s)\n} is %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_get_in__get_default_one_keyword_with_default():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: 2}
    @py_assert5 = [
     2]
    @py_assert7 = 'other'
    @py_assert9 = @py_assert1(@py_assert3, @py_assert5, @py_assert7)
    @py_assert12 = 'other'
    @py_assert11 = @py_assert9 == @py_assert12
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=212)
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py6)s, %(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_get_in__get_default_three_keywords_fail_at_first():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: {2: {3: 4}}}
    @py_assert5 = [
     2, 2, 4]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 is @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=216)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py6)s)\n} is %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_get_in__get_default_three_keywords_fail_at_first_with_default():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: {2: {3: 4}}}
    @py_assert5 = [
     2, 2, 4]
    @py_assert7 = 'other'
    @py_assert9 = @py_assert1(@py_assert3, @py_assert5, @py_assert7)
    @py_assert12 = 'other'
    @py_assert11 = @py_assert9 == @py_assert12
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=220)
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py6)s, %(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_get_in__get_default_three_keywords_fail_at_second():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: {2: {3: 4}}}
    @py_assert5 = [
     1, 3, 4]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 is @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=224)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py6)s)\n} is %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_get_in__get_default_three_keywords_fail_at_second_with_default():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: {2: {3: 4}}}
    @py_assert5 = [
     1, 3, 4]
    @py_assert7 = 'other'
    @py_assert9 = @py_assert1(@py_assert3, @py_assert5, @py_assert7)
    @py_assert12 = 'other'
    @py_assert11 = @py_assert9 == @py_assert12
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=228)
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py6)s, %(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_get_in__get_default_three_keywords_fail_at_third():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: {2: {3: 4}}}
    @py_assert5 = [
     1, 2, 4]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 is @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=232)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py6)s)\n} is %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_get_in__get_default_three_keywords_fail_at_third_with_default():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: {2: {3: 4}}}
    @py_assert5 = [
     1, 2, 4]
    @py_assert7 = 'other'
    @py_assert9 = @py_assert1(@py_assert3, @py_assert5, @py_assert7)
    @py_assert12 = 'other'
    @py_assert11 = @py_assert9 == @py_assert12
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=236)
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py6)s, %(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_get_in__iterator_keywords():
    @py_assert1 = utils.get_in
    @py_assert3 = {1: {2: {3: 4}}}
    @py_assert6 = [
     1, 2, 3]
    @py_assert8 = iter(@py_assert6)
    @py_assert10 = @py_assert1(@py_assert3, @py_assert8)
    @py_assert13 = 4
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=240)
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.get_in\n}(%(py4)s, %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def _do_split(lst, key):
    return list(utils.split_before(lst, key))


def test_split_before__split_empty_list():
    @py_assert1 = []
    @py_assert3 = None
    @py_assert5 = _do_split(@py_assert1, @py_assert3)
    @py_assert8 = []
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=255)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_do_split) if '_do_split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_do_split) else '_do_split',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_split_before__split_list_with_no_true_pred():
    @py_assert3 = 10
    @py_assert5 = range(@py_assert3)
    @py_assert7 = list(@py_assert5)
    @py_assert9 = lambda x: False
    @py_assert11 = _do_split(@py_assert7, @py_assert9)
    @py_assert14 = [
     list(range(10))]
    @py_assert13 = @py_assert11 == @py_assert14
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=259)
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n})\n}, %(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(_do_split) if '_do_split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_do_split) else '_do_split',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


def test_split_before__split_list_true_pred_at_first_position():
    @py_assert3 = 4
    @py_assert5 = range(@py_assert3)
    @py_assert7 = list(@py_assert5)
    @py_assert9 = lambda x: x % 2 == 0
    @py_assert11 = _do_split(@py_assert7, @py_assert9)
    @py_assert14 = [
     [
      0, 1], [2, 3]]
    @py_assert13 = @py_assert11 == @py_assert14
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=263)
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n})\n}, %(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(_do_split) if '_do_split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_do_split) else '_do_split',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


def test_split_before__split_list_true_pred_at_second_position():
    @py_assert3 = 4
    @py_assert5 = range(@py_assert3)
    @py_assert7 = list(@py_assert5)
    @py_assert9 = lambda x: x % 2 == 1
    @py_assert11 = _do_split(@py_assert7, @py_assert9)
    @py_assert14 = [
     [
      0], [1, 2], [3]]
    @py_assert13 = @py_assert11 == @py_assert14
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=267)
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n})\n}, %(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(_do_split) if '_do_split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_do_split) else '_do_split',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


def test_split_before__split_consequtive_true_pred():
    @py_assert3 = 0
    @py_assert5 = 5
    @py_assert7 = 2
    @py_assert9 = range(@py_assert3, @py_assert5, @py_assert7)
    @py_assert11 = list(@py_assert9)
    @py_assert13 = lambda x: x % 2 == 0
    @py_assert15 = _do_split(@py_assert11, @py_assert13)
    @py_assert18 = [
     [
      0], [2], [4]]
    @py_assert17 = @py_assert15 == @py_assert18
    if @py_assert17 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=271)
    if not @py_assert17:
        @py_format20 = @pytest_ar._call_reprcompare(('==', ), (@py_assert17,), ('%(py16)s\n{%(py16)s = %(py0)s(%(py12)s\n{%(py12)s = %(py1)s(%(py10)s\n{%(py10)s = %(py2)s(%(py4)s, %(py6)s, %(py8)s)\n})\n}, %(py14)s)\n} == %(py19)s', ), (@py_assert15, @py_assert18)) % {'py0':@pytest_ar._saferepr(_do_split) if '_do_split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_do_split) else '_do_split',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert18 = None


def test_split_before__no_hits():
    @py_assert3 = 1
    @py_assert5 = 5
    @py_assert7 = range(@py_assert3, @py_assert5)
    @py_assert9 = list(@py_assert7)
    @py_assert11 = lambda x: x % 5 == 0
    @py_assert13 = _do_split(@py_assert9, @py_assert11)
    @py_assert16 = [
     list(range(1, 5))]
    @py_assert15 = @py_assert13 == @py_assert16
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=275)
    if not @py_assert15:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py0)s(%(py10)s\n{%(py10)s = %(py1)s(%(py8)s\n{%(py8)s = %(py2)s(%(py4)s, %(py6)s)\n})\n}, %(py12)s)\n} == %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(_do_split) if '_do_split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_do_split) else '_do_split',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None


def test_grouper__empty_list():
    result = utils.grouper(3, [])
    @py_assert2 = list(result)
    @py_assert5 = []
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=285)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_grouper__non_empty_list():
    result = utils.grouper(3, list(range(6)))
    expected = [(0, 1, 2), (3, 4, 5)]
    @py_assert2 = list(result)
    @py_assert4 = @py_assert2 == expected
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=291)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_grouper__non_empty_list_with_trailing():
    result = utils.grouper(3, list(range(7)))
    expected = [(0, 1, 2), (3, 4, 5), (6, None, None)]
    @py_assert2 = list(result)
    @py_assert4 = @py_assert2 == expected
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=297)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_grouper__non_empty_list_with_trailing_fill_value():
    result = utils.grouper(3, (list(range(7))), fillvalue='\\0')
    expected = [(0, 1, 2), (3, 4, 5), (6, '\\0', '\\0')]
    @py_assert2 = list(result)
    @py_assert4 = @py_assert2 == expected
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=303)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_group_by_pred__empty_list():
    @py_assert1 = utils.group_by_pred
    @py_assert4 = []
    @py_assert6 = @py_assert1(id, @py_assert4)
    @py_assert9 = ([], [])
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=312)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.group_by_pred\n}(%(py3)s, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_group_by_pred__always_false():
    @py_assert1 = utils.group_by_pred
    @py_assert3 = lambda x: False
    @py_assert5 = [
     1, 2, 3]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = ([], [1, 2, 3])
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=316)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.group_by_pred\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_group_by_pred__always_true():
    @py_assert1 = utils.group_by_pred
    @py_assert3 = lambda x: True
    @py_assert5 = [
     1, 2, 3]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = (
     [
      1, 2, 3], [])
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=320)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.group_by_pred\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_group_by_pred__is_even():
    @py_assert1 = utils.group_by_pred
    @py_assert3 = lambda x: x % 2 == 0
    @py_assert5 = [
     1, 2, 3]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = (
     [
      2], [1, 3])
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=324)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.group_by_pred\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_group_by_pred__iterable():
    @py_assert1 = utils.group_by_pred
    @py_assert3 = lambda x: x % 2 == 0
    @py_assert6 = 1
    @py_assert8 = 4
    @py_assert10 = range(@py_assert6, @py_assert8)
    @py_assert12 = @py_assert1(@py_assert3, @py_assert10)
    @py_assert15 = (
     [
      2], [1, 3])
    @py_assert14 = @py_assert12 == @py_assert15
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=328)
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.group_by_pred\n}(%(py4)s, %(py11)s\n{%(py11)s = %(py5)s(%(py7)s, %(py9)s)\n})\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None


def test_fragment__empty():
    @py_assert2 = utils.fragment
    @py_assert4 = 5
    @py_assert6 = ''
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = list(@py_assert8)
    @py_assert13 = []
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=337)
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.fragment\n}(%(py5)s, %(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = utils.fragment
    @py_assert4 = 5
    @py_assert6 = []
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = list(@py_assert8)
    @py_assert13 = []
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=338)
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.fragment\n}(%(py5)s, %(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_fragment__partial_fragment():
    @py_assert2 = utils.fragment
    @py_assert4 = 3
    @py_assert6 = 'ab'
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = list(@py_assert8)
    @py_assert13 = [
     'ab']
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=342)
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.fragment\n}(%(py5)s, %(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = utils.fragment
    @py_assert4 = 3
    @py_assert6 = [
     'a', 'b']
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = list(@py_assert8)
    @py_assert13 = [
     [
      'a', 'b']]
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=343)
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.fragment\n}(%(py5)s, %(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_fragment__single_fragment():
    @py_assert2 = utils.fragment
    @py_assert4 = 3
    @py_assert6 = 'abc'
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = list(@py_assert8)
    @py_assert13 = [
     'abc']
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=347)
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.fragment\n}(%(py5)s, %(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = utils.fragment
    @py_assert4 = 3
    @py_assert6 = [
     'a', 'b', 'c']
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = list(@py_assert8)
    @py_assert13 = [
     [
      'a', 'b', 'c']]
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=348)
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.fragment\n}(%(py5)s, %(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_fragment__multiple_fragments():
    @py_assert2 = utils.fragment
    @py_assert4 = 3
    @py_assert6 = 'abcdef'
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = list(@py_assert8)
    @py_assert13 = [
     'abc', 'def']
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=352)
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.fragment\n}(%(py5)s, %(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = utils.fragment
    @py_assert4 = 3
    @py_assert7 = 'abcdef'
    @py_assert9 = list(@py_assert7)
    @py_assert11 = @py_assert2(@py_assert4, @py_assert9)
    @py_assert13 = list(@py_assert11)
    @py_assert16 = [
     list('abc'), list('def')]
    @py_assert15 = @py_assert13 == @py_assert16
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=353)
    if not @py_assert15:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py3)s\n{%(py3)s = %(py1)s.fragment\n}(%(py5)s, %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n})\n})\n} == %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None


def test_fragment__multiple_fragments_partial():
    @py_assert2 = utils.fragment
    @py_assert4 = 3
    @py_assert6 = 'abcdefgh'
    @py_assert8 = @py_assert2(@py_assert4, @py_assert6)
    @py_assert10 = list(@py_assert8)
    @py_assert13 = [
     'abc', 'def', 'gh']
    @py_assert12 = @py_assert10 == @py_assert13
    if @py_assert12 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=357)
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py1)s.fragment\n}(%(py5)s, %(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = utils.fragment
    @py_assert4 = 3
    @py_assert7 = 'abcdefgh'
    @py_assert9 = list(@py_assert7)
    @py_assert11 = @py_assert2(@py_assert4, @py_assert9)
    @py_assert13 = list(@py_assert11)
    @py_assert16 = [
     list('abc'), list('def'), list('gh')]
    @py_assert15 = @py_assert13 == @py_assert16
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=358)
    if not @py_assert15:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py3)s\n{%(py3)s = %(py1)s.fragment\n}(%(py5)s, %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n})\n})\n} == %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None


def test_fragment__range():
    @py_assert2 = utils.fragment
    @py_assert4 = 3
    @py_assert7 = 6
    @py_assert9 = range(@py_assert7)
    @py_assert11 = @py_assert2(@py_assert4, @py_assert9)
    @py_assert13 = list(@py_assert11)
    @py_assert16 = [
     range(3), range(3, 6)]
    @py_assert15 = @py_assert13 == @py_assert16
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=366)
    if not @py_assert15:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py3)s\n{%(py3)s = %(py1)s.fragment\n}(%(py5)s, %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n})\n})\n} == %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None


def test_fragment__iterable():
    with pytest.raises(TypeError):
        list(utils.fragment(3, iter(range(6))))


def test_fragment__set():
    with pytest.raises(TypeError):
        list(utils.fragment(3, set(range(6))))


def test_cumsum__empty():
    @py_assert2 = utils.cumsum
    @py_assert4 = []
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert11 = []
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=385)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.cumsum\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_cumsum__integers():
    @py_assert2 = utils.cumsum
    @py_assert6 = 4
    @py_assert8 = -@py_assert6
    @py_assert9 = 5
    @py_assert11 = range(@py_assert8, @py_assert9)
    @py_assert13 = list(@py_assert11)
    @py_assert15 = @py_assert2(@py_assert13)
    @py_assert17 = list(@py_assert15)
    @py_assert20 = [
     -4, -7, -9, -10, -10, -9, -7, -4, 0]
    @py_assert19 = @py_assert17 == @py_assert20
    if @py_assert19 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=389)
    if not @py_assert19:
        @py_format22 = @pytest_ar._call_reprcompare(('==', ), (@py_assert19,), ('%(py18)s\n{%(py18)s = %(py0)s(%(py16)s\n{%(py16)s = %(py3)s\n{%(py3)s = %(py1)s.cumsum\n}(%(py14)s\n{%(py14)s = %(py4)s(%(py12)s\n{%(py12)s = %(py5)s(-%(py7)s, %(py10)s)\n})\n})\n})\n} == %(py21)s', ), (@py_assert17, @py_assert20)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py5':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py21':@pytest_ar._saferepr(@py_assert20)}
        @py_format24 = 'assert %(py23)s' % {'py23': @py_format22}
        raise AssertionError(@pytest_ar._format_explanation(@py_format24))
    @py_assert2 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert20 = None


def test_cumsum__float():
    @py_assert2 = utils.cumsum
    @py_assert4 = (1.0, 2.0, 3.0)
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert11 = [
     1.0, 3.0, 6.0]
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=403)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.cumsum\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_cumsum__initial():
    @py_assert2 = utils.cumsum
    @py_assert6 = 5
    @py_assert8 = range(@py_assert6)
    @py_assert10 = list(@py_assert8)
    @py_assert12 = 10
    @py_assert14 = -@py_assert12
    @py_assert15 = @py_assert2(@py_assert10, @py_assert14)
    @py_assert17 = list(@py_assert15)
    @py_assert20 = [
     -10, -9, -7, -4, 0]
    @py_assert19 = @py_assert17 == @py_assert20
    if @py_assert19 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=407)
    if not @py_assert19:
        @py_format22 = @pytest_ar._call_reprcompare(('==', ), (@py_assert19,), ('%(py18)s\n{%(py18)s = %(py0)s(%(py16)s\n{%(py16)s = %(py3)s\n{%(py3)s = %(py1)s.cumsum\n}(%(py11)s\n{%(py11)s = %(py4)s(%(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n})\n}, -%(py13)s)\n})\n} == %(py21)s', ), (@py_assert17, @py_assert20)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py5':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py21':@pytest_ar._saferepr(@py_assert20)}
        @py_format24 = 'assert %(py23)s' % {'py23': @py_format22}
        raise AssertionError(@pytest_ar._format_explanation(@py_format24))
    @py_assert2 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert20 = None


def test_fill_dict__empty_dicts():
    result = utils.fill_dict({}, {})
    @py_assert2 = {}
    @py_assert1 = result == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=417)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_fill_dict__filling_empty_dict():
    source = {'a':1, 
     'b':{'c':2,  'd':3}}
    expected = {'a':1,  'b':{'c':2,  'd':3}}
    result = utils.fill_dict({}, source)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=424)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_fill_dict__filling_full_dict():
    source = {'a':1, 
     'b':{'c':2,  'd':3}}
    destination = {'a':2,  'b':{'c':3,  'd':4}}
    expected = {'a':2,  'b':{'c':3,  'd':4}}
    result = utils.fill_dict(destination, source)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=432)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_fill_dict__destination_not_modified():
    source = {'a':1, 
     'b':{'c':2,  'd':3}}
    destination = {'b': {'d': 0}}
    utils.fill_dict(destination, source)
    @py_assert2 = {'b': {'d': 0}}
    @py_assert1 = destination == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=439)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (destination, @py_assert2)) % {'py0':@pytest_ar._saferepr(destination) if 'destination' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(destination) else 'destination',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_fill_dict__source_not_modified():
    expected = {'a':1, 
     'b':{'c':2,  'd':3}}
    source = {'a':1,  'b':{'c':2,  'd':3}}
    destination = {'b': {'d': 0}}
    utils.fill_dict(destination, source)
    @py_assert1 = source == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=447)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (source, expected)) % {'py0':@pytest_ar._saferepr(source) if 'source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source) else 'source',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_fill_dict__destination_must_be_dict():
    with pytest.raises(TypeError):
        utils.fill_dict([], {})


def test_fill_dict__source_must_be_dict():
    with pytest.raises(TypeError):
        utils.fill_dict({}, [])


def test_chain_sorted__no_sequences():
    expected = ()
    result = tuple(utils.chain_sorted())
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=468)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_chain_sorted__single_sequence():
    sequence = (1, 2, 3)
    result = tuple(utils.chain_sorted(sequence))
    @py_assert1 = sequence == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=474)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (sequence, result)) % {'py0':@pytest_ar._saferepr(sequence) if 'sequence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sequence) else 'sequence',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


_SEQUENTIAL_CONTENT_1 = (1, 2, 3)
_SEQUENTIAL_CONTENT_2 = (4, 5, 6)
_SEQUENTIAL_CONTENT_PERMUTATIONS = (
 (
  _SEQUENTIAL_CONTENT_1, _SEQUENTIAL_CONTENT_2),
 (
  _SEQUENTIAL_CONTENT_2, _SEQUENTIAL_CONTENT_1))

@pytest.mark.parametrize('seq_a, seq_b', _SEQUENTIAL_CONTENT_PERMUTATIONS)
def test_chain_sorted__sequential_contents(seq_a, seq_b):
    expected = (1, 2, 3, 4, 5, 6)
    result = tuple(utils.chain_sorted(seq_a, seq_b))
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=489)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_chain_sorted__mixed_contents():
    sequence_a = (3, 4, 8)
    sequence_c = (0, 1, 6)
    sequence_b = (2, 5, 7)
    expected = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    result = tuple(utils.chain_sorted(sequence_a, sequence_b, sequence_c))
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=498)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_chain_sorted__mixed_length_contents():
    sequence_a = (1, )
    sequence_c = (0, 2)
    sequence_b = ()
    expected = (0, 1, 2)
    result = tuple(utils.chain_sorted(sequence_a, sequence_b, sequence_c))
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=507)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_chain_sorted__mixed_contents__key():
    sequence_a = (-2, -3, -5)
    sequence_b = (0, -1, -4)
    expected = (0, -1, -2, -3, -4, -5)
    result = tuple(utils.chain_sorted(sequence_a, sequence_b, key=abs))
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=515)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_chain_sorted__identical_objects_are_preserved():
    object_a = [
     1]
    object_b = [1]
    @py_assert1 = object_a is not object_b
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=521)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py2)s', ), (object_a, object_b)) % {'py0':@pytest_ar._saferepr(object_a) if 'object_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(object_a) else 'object_a',  'py2':@pytest_ar._saferepr(object_b) if 'object_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(object_b) else 'object_b'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    expected = (object_a, object_b)
    result = tuple(utils.chain_sorted([object_a], [object_b]))
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=524)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = []
    @py_assert4 = result[0]
    @py_assert3 = object_a is @py_assert4
    @py_assert0 = @py_assert3
    if not @py_assert3:
        @py_assert11 = result[1]
        @py_assert10 = object_a is @py_assert11
        @py_assert0 = @py_assert10
    if @py_assert0 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=525)
    if not @py_assert0:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s is %(py5)s', ), (object_a, @py_assert4)) % {'py2':@pytest_ar._saferepr(object_a) if 'object_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(object_a) else 'object_a',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = '%(py7)s' % {'py7': @py_format6}
        @py_assert1.append(@py_format8)
        if not @py_assert3:
            @py_format13 = @pytest_ar._call_reprcompare(('is', ), (@py_assert10,), ('%(py9)s is %(py12)s', ), (object_a, @py_assert11)) % {'py9':@pytest_ar._saferepr(object_a) if 'object_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(object_a) else 'object_a',  'py12':@pytest_ar._saferepr(@py_assert11)}
            @py_format15 = '%(py14)s' % {'py14': @py_format13}
            @py_assert1.append(@py_format15)
        @py_format16 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert0 = @py_assert1 = @py_assert3 = @py_assert4 = @py_assert10 = @py_assert11 = None
    @py_assert1 = []
    @py_assert4 = result[0]
    @py_assert3 = object_b is @py_assert4
    @py_assert0 = @py_assert3
    if not @py_assert3:
        @py_assert11 = result[1]
        @py_assert10 = object_b is @py_assert11
        @py_assert0 = @py_assert10
    if @py_assert0 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=526)
    if not @py_assert0:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s is %(py5)s', ), (object_b, @py_assert4)) % {'py2':@pytest_ar._saferepr(object_b) if 'object_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(object_b) else 'object_b',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = '%(py7)s' % {'py7': @py_format6}
        @py_assert1.append(@py_format8)
        if not @py_assert3:
            @py_format13 = @pytest_ar._call_reprcompare(('is', ), (@py_assert10,), ('%(py9)s is %(py12)s', ), (object_b, @py_assert11)) % {'py9':@pytest_ar._saferepr(object_b) if 'object_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(object_b) else 'object_b',  'py12':@pytest_ar._saferepr(@py_assert11)}
            @py_format15 = '%(py14)s' % {'py14': @py_format13}
            @py_assert1.append(@py_format15)
        @py_format16 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert0 = @py_assert1 = @py_assert3 = @py_assert4 = @py_assert10 = @py_assert11 = None


def test_chain_sorted__stable_sort():
    object_a = [
     1]
    object_b = [1]
    object_c = [2]
    object_d = [2]
    seq_a = [object_a, object_c]
    seq_b = [object_b, object_d]
    expected = (
     object_a, object_b, object_c, object_d)
    result = tuple(utils.chain_sorted(seq_a, seq_b))
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=539)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = (a is b for a, b in zip(expected, result))
    @py_assert3 = all(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=540)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    expected = (
     object_b, object_a, object_d, object_c)
    result = tuple(utils.chain_sorted(seq_b, seq_a))
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=544)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = (a is b for a, b in zip(expected, result))
    @py_assert3 = all(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=545)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_chain_sorted__runs_of_values():
    object_a = [
     1]
    object_b = [1]
    object_c = [2]
    object_d = [2]
    seq_a = [object_a, object_b]
    seq_b = [object_c, object_d]
    expected = (
     object_a, object_b, object_c, object_d)
    result = tuple(utils.chain_sorted(seq_a, seq_b))
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=558)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = (a is b for a, b in zip(expected, result))
    @py_assert3 = all(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=559)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_chain_sorted__invalid_keywords():
    with pytest.raises(TypeError):
        tuple(utils.chain_sorted((1, 2, 3), foobar=None))


def test_immutable__properties_set():

    class ImmutableCls(utils.Immutable):

        def __init__(self, value):
            utils.Immutable.__init__(self, value=value)

    obj = ImmutableCls(17)
    @py_assert1 = obj.value
    @py_assert4 = 17
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=578)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.parametrize('key, value', (('value', 13), ('new_value', 'foo')))
def test_immutable__properties_immutable(key, value):

    class ImmutableCls(utils.Immutable):

        def __init__(self, value):
            utils.Immutable.__init__(self, value=value)

    obj = ImmutableCls(17)
    with pytest.raises(NotImplementedError):
        setattr(obj, key, value)


def test_immutable__properties_del():

    class ImmutableCls(utils.Immutable):

        def __init__(self, value):
            utils.Immutable.__init__(self, value=value)

    def _del_property(obj):
        del obj.value

    obj = ImmutableCls(17)
    with pytest.raises(NotImplementedError):
        _del_property(obj)


class SomethingOrdered(utils.TotallyOrdered):

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        if not isinstance(other, SomethingOrdered):
            return NotImplemented
        else:
            return self.value < other.value


def test_totally_ordered__lt_vs_lt():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 2
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 < @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=623)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('<', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} < %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_totally_ordered__lt_vs_gt():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 0
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 < @py_assert9
    @py_assert13 = not @py_assert5
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=627)
    if not @py_assert13:
        @py_format11 = @pytest_ar._call_reprcompare(('<', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} < %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format14 = 'assert not %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = None


def test_totally_ordered__lt_vs_wrong_type():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert5 = @py_assert3.__lt__
    @py_assert7 = 'Foo'
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert11 = @py_assert9 == NotImplemented
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=631)
    if not @py_assert11:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.__lt__\n}(%(py8)s)\n} == %(py12)s', ), (@py_assert9, NotImplemented)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(NotImplemented) if 'NotImplemented' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NotImplemented) else 'NotImplemented'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_totally_ordered__le_vs_le():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 1
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 <= @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=636)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} <= %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_totally_ordered__le_vs_gt():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 0
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 <= @py_assert9
    @py_assert13 = not @py_assert5
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=640)
    if not @py_assert13:
        @py_format11 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} <= %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format14 = 'assert not %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = None


def test_totally_ordered__le_vs_wrong_type():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert5 = @py_assert3.__le__
    @py_assert7 = 'Foo'
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert11 = @py_assert9 == NotImplemented
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=644)
    if not @py_assert11:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.__le__\n}(%(py8)s)\n} == %(py12)s', ), (@py_assert9, NotImplemented)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(NotImplemented) if 'NotImplemented' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NotImplemented) else 'NotImplemented'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_totally_ordered__ge_vs_ge():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 1
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 >= @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=649)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} >= %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_totally_ordered__ge_vs_lt():
    @py_assert1 = 0
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 1
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 >= @py_assert9
    @py_assert13 = not @py_assert5
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=653)
    if not @py_assert13:
        @py_format11 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} >= %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format14 = 'assert not %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = None


def test_totally_ordered__ge_vs_wrong_type():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert5 = @py_assert3.__ge__
    @py_assert7 = 'Foo'
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert11 = @py_assert9 == NotImplemented
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=657)
    if not @py_assert11:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.__ge__\n}(%(py8)s)\n} == %(py12)s', ), (@py_assert9, NotImplemented)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(NotImplemented) if 'NotImplemented' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NotImplemented) else 'NotImplemented'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_totally_ordered__gt_vs_gt():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 0
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 > @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=662)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('>', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} > %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_totally_ordered__gt_vs_eq():
    @py_assert1 = 0
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 0
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 > @py_assert9
    @py_assert13 = not @py_assert5
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=666)
    if not @py_assert13:
        @py_format11 = @pytest_ar._call_reprcompare(('>', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} > %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format14 = 'assert not %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = None


def test_totally_ordered__gt_vs_wrong_type():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert5 = @py_assert3.__gt__
    @py_assert7 = 'Foo'
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert11 = @py_assert9 == NotImplemented
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=670)
    if not @py_assert11:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.__gt__\n}(%(py8)s)\n} == %(py12)s', ), (@py_assert9, NotImplemented)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(NotImplemented) if 'NotImplemented' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NotImplemented) else 'NotImplemented'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_totally_ordered__eq_vs_eq():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 1
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=675)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_totally_ordered__eq_vs_ne():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 2
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    @py_assert13 = not @py_assert5
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=679)
    if not @py_assert13:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format14 = 'assert not %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = None


def test_totally_ordered__eq_vs_wrong_type():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert5 = @py_assert3.__eq__
    @py_assert7 = 'Foo'
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert11 = @py_assert9 == NotImplemented
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=683)
    if not @py_assert11:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.__eq__\n}(%(py8)s)\n} == %(py12)s', ), (@py_assert9, NotImplemented)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(NotImplemented) if 'NotImplemented' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NotImplemented) else 'NotImplemented'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_totally_ordered__ne_vs_ne():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 2
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 != @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=688)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} != %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_totally_ordered__ne_vs_eq():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert7 = 1
    @py_assert9 = SomethingOrdered(@py_assert7)
    @py_assert5 = @py_assert3 != @py_assert9
    @py_assert13 = not @py_assert5
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=692)
    if not @py_assert13:
        @py_format11 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} != %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format14 = 'assert not %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = None


def test_totally_ordered__ne_vs_wrong_type():
    @py_assert1 = 1
    @py_assert3 = SomethingOrdered(@py_assert1)
    @py_assert5 = @py_assert3.__ne__
    @py_assert7 = 'Foo'
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert11 = @py_assert9 == NotImplemented
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/utilities_test.py', lineno=696)
    if not @py_assert11:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.__ne__\n}(%(py8)s)\n} == %(py12)s', ), (@py_assert9, NotImplemented)) % {'py0':@pytest_ar._saferepr(SomethingOrdered) if 'SomethingOrdered' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SomethingOrdered) else 'SomethingOrdered',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(NotImplemented) if 'NotImplemented' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NotImplemented) else 'NotImplemented'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None


class SomethingBadlyOrdered(utils.TotallyOrdered):

    def __init__(self, value):
        self.value = value


def test_totally_ordered__missing_implementation():
    obj_a = SomethingBadlyOrdered(1)
    obj_b = SomethingBadlyOrdered(2)
    with pytest.raises(NotImplementedError):
        operator.gt(obj_a, obj_b)