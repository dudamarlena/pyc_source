# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/versions_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 23379 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, operator, pickle, pytest, paleomix.common.versions as versions

def test_check__func_must_be_callable():
    with pytest.raises(TypeError):
        versions.Check('FooBar', 3, 7, 5)


def test_check_str():
    obj = versions.Check('FooBar', operator.lt, 3, 7, 5)
    @py_assert2 = str(obj)
    @py_assert5 = 'FooBar'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=42)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_check__eq_same_func_desc_and_version():
    obj_1 = versions.Check('Desc {}', operator.lt, 1, 2, 3)
    obj_2 = versions.Check('Desc {}', operator.lt, 1, 2, 3)
    @py_assert2 = hash(obj_1)
    @py_assert7 = hash(obj_2)
    @py_assert4 = @py_assert2 == @py_assert7
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=53)
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(obj_1) if 'obj_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_1) else 'obj_1',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py6':@pytest_ar._saferepr(obj_2) if 'obj_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_2) else 'obj_2',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert1 = obj_1 == obj_2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=54)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (obj_1, obj_2)) % {'py0':@pytest_ar._saferepr(obj_1) if 'obj_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_1) else 'obj_1',  'py2':@pytest_ar._saferepr(obj_2) if 'obj_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_2) else 'obj_2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_check__not_eq_for_diff_func_same_desc_and_version():
    obj_1 = versions.Check('Desc {}', operator.gt, 1, 2, 3)
    obj_2 = versions.Check('Desc {}', operator.lt, 1, 2, 3)
    @py_assert2 = hash(obj_1)
    @py_assert7 = hash(obj_2)
    @py_assert4 = @py_assert2 != @py_assert7
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=60)
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} != %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(obj_1) if 'obj_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_1) else 'obj_1',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py6':@pytest_ar._saferepr(obj_2) if 'obj_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_2) else 'obj_2',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert1 = obj_1 != obj_2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=61)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != %(py2)s', ), (obj_1, obj_2)) % {'py0':@pytest_ar._saferepr(obj_1) if 'obj_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_1) else 'obj_1',  'py2':@pytest_ar._saferepr(obj_2) if 'obj_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_2) else 'obj_2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_check__not_eq_for_diff_desc_same_func_and_version():
    obj_1 = versions.Check('Desc1 {}', operator.lt, 1, 2, 3)
    obj_2 = versions.Check('Desc2 {}', operator.lt, 1, 2, 3)
    @py_assert2 = hash(obj_1)
    @py_assert7 = hash(obj_2)
    @py_assert4 = @py_assert2 != @py_assert7
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=67)
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} != %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(obj_1) if 'obj_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_1) else 'obj_1',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py6':@pytest_ar._saferepr(obj_2) if 'obj_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_2) else 'obj_2',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert1 = obj_1 != obj_2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=68)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != %(py2)s', ), (obj_1, obj_2)) % {'py0':@pytest_ar._saferepr(obj_1) if 'obj_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_1) else 'obj_1',  'py2':@pytest_ar._saferepr(obj_2) if 'obj_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_2) else 'obj_2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_check__not_eq_for_same_func_desc_diff_version():
    obj_1 = versions.Check('Desc {}', operator.lt, 1, 2, 3)
    obj_2 = versions.Check('Desc {}', operator.lt, 1, 3, 3)
    @py_assert2 = hash(obj_1)
    @py_assert7 = hash(obj_2)
    @py_assert4 = @py_assert2 != @py_assert7
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=74)
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} != %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(obj_1) if 'obj_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_1) else 'obj_1',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py6':@pytest_ar._saferepr(obj_2) if 'obj_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_2) else 'obj_2',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert1 = obj_1 != obj_2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=75)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != %(py2)s', ), (obj_1, obj_2)) % {'py0':@pytest_ar._saferepr(obj_1) if 'obj_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_1) else 'obj_1',  'py2':@pytest_ar._saferepr(obj_2) if 'obj_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_2) else 'obj_2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_eq__str__one_value():
    obj = versions.EQ(1)
    @py_assert2 = str(obj)
    @py_assert5 = 'v1.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=85)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_eq__str__two_values():
    obj = versions.EQ(2, 1)
    @py_assert2 = str(obj)
    @py_assert5 = 'v2.1.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=90)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_eq__check_values__equal():
    obj = versions.EQ(2, 3)
    @py_assert1 = (2, 3)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=95)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_eq__check_values__not_equal():
    obj = versions.EQ(2, 3)
    @py_assert1 = (1, 3)
    @py_assert3 = obj(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=100)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = (2, 2)
    @py_assert3 = obj(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=101)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = (1, 4)
    @py_assert3 = obj(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=102)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_eq__check_values__equal_truncated():
    obj = versions.EQ(2, 3)
    @py_assert1 = (2, 3, 1)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=107)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_eq__check_values__equal_too_few_values():
    obj = versions.EQ(2, 3)
    with pytest.raises(ValueError):
        obj((2, ))


def test_eq__check_values__not_equal_too_few_values():
    obj = versions.EQ(2, 3)
    with pytest.raises(ValueError):
        obj((1, ))


def test_ge__str__one_value():
    obj = versions.GE(1)
    @py_assert2 = str(obj)
    @py_assert5 = 'at least v1.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=129)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_ge__str__two_values():
    obj = versions.GE(2, 1)
    @py_assert2 = str(obj)
    @py_assert5 = 'at least v2.1.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=134)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_ge__check_values__greater_than_or_equal():
    obj = versions.GE(2, 3)
    @py_assert1 = (2, 3)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=139)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (2, 4)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=140)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (3, 0)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=141)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_ge__check_values__not_greater_than_or_equal():
    obj = versions.GE(2, 3)
    @py_assert1 = (1, 3)
    @py_assert3 = obj(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=146)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = (2, 2)
    @py_assert3 = obj(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=147)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_ge__check_values__greater_than_or_equal_truncated():
    obj = versions.GE(2, 3)
    @py_assert1 = (2, 3, 1)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=152)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (2, 4, 2)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=153)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_ge__check_values__equal_too_few_values():
    obj = versions.GE(2, 3)
    with pytest.raises(ValueError):
        obj((2, ))


def test_ge__check_values__not_equal_too_few_values():
    obj = versions.GE(2, 3)
    with pytest.raises(ValueError):
        obj((1, ))


def test_lt__str__one_value():
    obj = versions.LT(1)
    @py_assert2 = str(obj)
    @py_assert5 = 'prior to v1.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=175)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_lt__str__two_values():
    obj = versions.LT(2, 1)
    @py_assert2 = str(obj)
    @py_assert5 = 'prior to v2.1.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=180)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_lt__check_values__less_than():
    obj = versions.LT(2, 3)
    @py_assert1 = (2, 2)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=185)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (1, 9)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=186)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_lt__check_values__not_less_than():
    obj = versions.LT(2, 3)
    @py_assert1 = (2, 3)
    @py_assert3 = obj(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=191)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = (2, 4)
    @py_assert3 = obj(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=192)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_lt__check_values__less_than_truncated():
    obj = versions.LT(2, 3)
    @py_assert1 = (2, 2, 1)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=197)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (2, 1, 2)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=198)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_lt__check_values__less_than_too_few_values():
    obj = versions.LT(2, 3)
    with pytest.raises(ValueError):
        obj((1, ))


def test_lt__check_values__not_less_than_too_few_values():
    obj = versions.LT(2, 3)
    with pytest.raises(ValueError):
        obj((3, ))


def test_any__str():
    obj = versions.Any()
    @py_assert2 = str(obj)
    @py_assert5 = 'any version'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=220)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_lt__check_values__always_true():
    obj = versions.Any()
    @py_assert1 = (1, )
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=225)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (2, 3)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=226)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (4, 5, 6)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=227)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (5, 6, 7, 8)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=228)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_and__init__non_check_value():
    with pytest.raises(ValueError):
        versions.And(versions.LT(2), None)


def test_and__str__single_item():
    obj = versions.And(versions.GE(1))
    @py_assert2 = str(obj)
    @py_assert5 = 'at least v1.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=248)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_and__str__two_items():
    obj_ge = versions.GE(1, 2)
    obj_lt = versions.LT(3, 4)
    obj = versions.And(obj_ge, obj_lt)
    @py_assert2 = str(obj)
    @py_assert5 = 'at least v1.2.x and prior to v3.4.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=256)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_and__str__two_items__first_is_operator():
    obj_1 = versions.And(versions.GE(1, 2), versions.LT(2, 0))
    obj_2 = versions.LT(3, 4)
    obj = versions.And(obj_1, obj_2)
    @py_assert2 = str(obj)
    @py_assert5 = '(at least v1.2.x and prior to v2.0.x) and prior to v3.4.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=264)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_and__str__two_items__second_is_operator():
    obj_1 = versions.GE(1, 2)
    obj_2 = versions.Or(versions.GE(2, 0), versions.LT(3, 4))
    obj = versions.And(obj_1, obj_2)
    @py_assert2 = str(obj)
    @py_assert5 = 'at least v1.2.x and (at least v2.0.x or prior to v3.4.x)'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=272)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_and__check_version__both_true():
    obj_1 = versions.GE(1, 2)
    obj_2 = versions.LT(2, 0)
    obj = versions.And(obj_1, obj_2)
    @py_assert1 = (1, 3)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=284)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_and__check_version__first_true():
    obj_1 = versions.And(versions.GE(1, 2), versions.LT(2, 0))
    obj_2 = versions.And(versions.GE(2, 3), versions.LT(3, 0))
    obj = versions.And(obj_1, obj_2)
    @py_assert1 = (1, 3)
    @py_assert3 = obj(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=291)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_and__check_version__second_true():
    obj_1 = versions.And(versions.GE(1, 2), versions.LT(2, 0))
    obj_2 = versions.And(versions.GE(2, 3), versions.LT(3, 0))
    obj = versions.And(obj_1, obj_2)
    @py_assert1 = (2, 3)
    @py_assert3 = obj(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=298)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_and__check_version__neither_true():
    obj_1 = versions.And(versions.GE(1, 2), versions.LT(2, 0))
    obj_2 = versions.And(versions.GE(2, 3), versions.LT(3, 0))
    obj = versions.And(obj_1, obj_2)
    @py_assert1 = (2, 2)
    @py_assert3 = obj(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=305)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


_TRUNCATED_VERSIONS = (
 (
  versions.GE(1, 2), versions.LT(2, 0)),
 (
  versions.GE(1, 2, 2), versions.LT(2, 0)),
 (
  versions.GE(1, 2), versions.LT(2, 0, 1)))

@pytest.mark.parametrize('obj_1, obj_2', _TRUNCATED_VERSIONS)
def test_and__check_version__truncated(obj_1, obj_2):
    obj = versions.And(obj_1, obj_2)
    @py_assert1 = (1, 3, 3)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=318)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


_INSUFFICIENT_VALUES = (
 (
  versions.GE(1, 2, 2), versions.LT(2, 0)),
 (
  versions.GE(1, 2), versions.LT(2, 0, 1)),
 (
  versions.GE(1, 2, 2), versions.LT(2, 0, 1)))

@pytest.mark.parametrize('obj_1, obj_2', _INSUFFICIENT_VALUES)
def test_and__check_version__insufficient_number_of_values(obj_1, obj_2):
    obj = versions.And(obj_1, obj_2)
    with pytest.raises(ValueError):
        obj((1, 3))


def test_or__init__non_check_value():
    with pytest.raises(ValueError):
        versions.Or(versions.LT(2), None)


def test_or__str__single_item():
    obj = versions.Or(versions.GE(1))
    @py_assert2 = str(obj)
    @py_assert5 = 'at least v1.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=352)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_or__str__two_items():
    obj_ge = versions.GE(1, 2)
    obj_lt = versions.LT(3, 4)
    obj = versions.Or(obj_ge, obj_lt)
    @py_assert2 = str(obj)
    @py_assert5 = 'at least v1.2.x or prior to v3.4.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=360)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_or__str__two_items__first_is_operator():
    obj_1 = versions.Or(versions.GE(1, 2), versions.LT(2, 0))
    obj_2 = versions.LT(3, 4)
    obj = versions.Or(obj_1, obj_2)
    @py_assert2 = str(obj)
    @py_assert5 = '(at least v1.2.x or prior to v2.0.x) or prior to v3.4.x'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=368)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_or__str__two_items__second_is_operator():
    obj_1 = versions.GE(1, 2)
    obj_2 = versions.And(versions.GE(2, 0), versions.LT(3, 4))
    obj = versions.Or(obj_1, obj_2)
    @py_assert2 = str(obj)
    @py_assert5 = 'at least v1.2.x or (at least v2.0.x and prior to v3.4.x)'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=376)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_or__check_version__both_true():
    obj_1 = versions.GE(1, 2)
    obj_2 = versions.LT(2, 0)
    obj = versions.Or(obj_1, obj_2)
    @py_assert1 = (1, 3)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=388)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_or__check_version__first_true():
    obj_1 = versions.And(versions.GE(1, 2), versions.LT(2, 0))
    obj_2 = versions.And(versions.GE(2, 3), versions.LT(3, 0))
    obj = versions.Or(obj_1, obj_2)
    @py_assert1 = (1, 3)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=395)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_or__check_version__second_true():
    obj_1 = versions.And(versions.GE(1, 2), versions.LT(2, 0))
    obj_2 = versions.And(versions.GE(2, 3), versions.LT(3, 0))
    obj = versions.Or(obj_1, obj_2)
    @py_assert1 = (2, 3)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=402)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_or__check_version__neither_true():
    obj_1 = versions.And(versions.GE(1, 2), versions.LT(2, 0))
    obj_2 = versions.And(versions.GE(2, 3), versions.LT(3, 0))
    obj = versions.Or(obj_1, obj_2)
    @py_assert1 = (2, 2)
    @py_assert3 = obj(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=409)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


@pytest.mark.parametrize('obj_1, obj_2', _TRUNCATED_VERSIONS)
def test_or__check_version__truncated(obj_1, obj_2):
    obj = versions.Or(obj_1, obj_2)
    @py_assert1 = (1, 3, 3)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=415)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


_INSUFFICIENT_VALUES_OR = (
 (
  versions.GE(1, 2, 2), versions.LT(2, 0)),
 (
  versions.GE(1, 2, 2), versions.LT(2, 0, 1)))

@pytest.mark.parametrize('obj_1, obj_2', _INSUFFICIENT_VALUES_OR)
def test_or__check_version__insufficient_number_of_values(obj_1, obj_2):
    obj = versions.Or(obj_1, obj_2)
    with pytest.raises(ValueError):
        obj((1, 3))


def test_or__check_version__insufficient_number_of_values__is_lazy():
    obj_1 = versions.GE(1, 2)
    obj_2 = versions.LT(2, 0, 1)
    obj = versions.Or(obj_1, obj_2)
    @py_assert1 = (1, 3)
    @py_assert3 = obj(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=435)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_requirementobj__init__defaults():
    obj = versions.RequirementObj(call=('echo', 'foo'),
      search='(\\d+)\\.(\\d+)',
      checks=(versions.Any()))
    @py_assert1 = obj.name
    @py_assert4 = 'echo'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=448)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = obj.priority
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=449)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.priority\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_requirementobj__init__non_defaults():
    obj = versions.RequirementObj(call=('bash', 'foo'),
      search='(\\d+)\\.(\\d+)',
      checks=(versions.Any()),
      name='A name',
      priority=17)
    @py_assert1 = obj.name
    @py_assert4 = 'A name'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=461)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = obj.priority
    @py_assert4 = 17
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=462)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.priority\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def _echo_version(version, dst='stdout', returncode=0):
    tmpl = 'import sys; sys.%s.write(%r); sys.exit(%s);'
    return ('/usr/bin/python', '-c', tmpl % (dst, version, returncode))


_PIPES = ('stderr', 'stdout')
_VERSION_CALL_RESULTS = (('v(\\d+)', (3,)), ('v(\\d+)\\.(\\d+)', (3, 5)), ('v(\\d+)\\.(\\d+)\\.(\\d+)', (3, 5, 2)))

@pytest.mark.parametrize('pipe', _PIPES)
@pytest.mark.parametrize('regexp, equals', _VERSION_CALL_RESULTS)
def test_requirementobj__version__call(pipe, regexp, equals):
    call = _echo_version('v3.5.2\n', dst=pipe)
    obj = versions.RequirementObj(call=call, search=regexp, checks=(versions.Any()))
    @py_assert1 = obj.version
    @py_assert3 = @py_assert1 == equals
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=489)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.version\n} == %(py4)s', ), (@py_assert1, equals)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(equals) if 'equals' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(equals) else 'equals'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_requirementobj__version__version_str_not_found():
    call = _echo_version('A typical error\n')
    obj = versions.RequirementObj(call=call,
      search='v(\\d+)\\.(\\d+)',
      checks=(versions.Any()))
    with pytest.raises(versions.VersionRequirementError):
        getattr(obj, 'version')


def test_requirementobj__version__command_not_found():
    obj = versions.RequirementObj(call=('xyzabcdefoo', ),
      search='v(\\d+)\\.(\\d+)',
      checks=(versions.Any()))
    try:
        obj.version
        @py_assert0 = False
        if @py_assert0 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=509)
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None
    except versions.VersionRequirementError as error:
        @py_assert0 = 'No such file or directory'
        @py_assert5 = str(error)
        @py_assert2 = @py_assert0 in @py_assert5
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=512)
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None


def test_requirementobj__version__command_not_executable():
    obj = versions.RequirementObj(call=('./README.rst', ),
      search='v(\\d+)\\.(\\d+)',
      checks=(versions.Any()))
    try:
        obj.version
        @py_assert0 = False
        if @py_assert0 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=522)
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None
    except versions.VersionRequirementError as error:
        @py_assert0 = '[Errno 13]'
        @py_assert5 = str(error)
        @py_assert2 = @py_assert0 in @py_assert5
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=525)
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None


def test_requirementobj__version__return_code_is_ignored():
    obj = versions.RequirementObj(_echo_version('v1.2.3', returncode=1),
      search='v(\\d+)\\.(\\d+)',
      checks=(versions.Any()))
    @py_assert1 = obj.version
    @py_assert4 = (1, 2)
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=534)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.version\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_requirementobj__version__func_call():

    def _return_version():
        return 'This is v5.3!'

    obj = versions.RequirementObj(call=_return_version,
      search='v(\\d+)\\.(\\d+)',
      checks=(versions.Any()))
    @py_assert1 = obj.version
    @py_assert4 = (5, 3)
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=544)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.version\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_requirementobj__version__func_call_with_arguments():

    def _return_version(arg1, arg2):
        @py_assert0 = (
         arg1, arg2)
        @py_assert3 = (2, 'foo')
        @py_assert2 = @py_assert0 == @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=549)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        return 'This is v5.3!'

    obj = versions.RequirementObj(call=(
     _return_version, 2, 'foo'),
      search='v(\\d+)\\.(\\d+)',
      checks=(versions.Any()))
    @py_assert1 = obj.version
    @py_assert4 = (5, 3)
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=555)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.version\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.parametrize('message', ('UnsupportedClassVersionError', 'UnsupportedClassVersionError v1.2.3'))
def test_requirementobj__version__outdated_jre__with_or_without_version_str(message):
    obj = versions.RequirementObj(call=(lambda : message),
      search='v(\\d+)\\.(\\d+)',
      checks=(versions.Any()))
    try:
        obj.version
        @py_assert0 = False
        if @py_assert0 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=568)
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None
    except versions.VersionRequirementError as error:
        @py_assert0 = 'upgrade your version of Java'
        @py_assert5 = str(error)
        @py_assert2 = @py_assert0 in @py_assert5
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=570)
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None


def test_requirementobj__executable__no_cli_args():
    obj = versions.RequirementObj(call=[
     'samtools'],
      search='v(\\d+)\\.(\\d+)',
      checks=(versions.Any()))
    @py_assert1 = obj.executable
    @py_assert4 = 'samtools'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=583)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.executable\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_requirementobj__executable__with_cli_arguments():
    obj = versions.RequirementObj(call=[
     'samtools', '--version'],
      search='v(\\d+)\\.(\\d+)',
      checks=(versions.Any()))
    @py_assert1 = obj.executable
    @py_assert4 = 'samtools'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=591)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.executable\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_requirementobj__executable__function():
    obj = versions.RequirementObj(call=(lambda : 'v1.1'),
      search='v(\\d+)\\.(\\d+)',
      checks=(versions.Any()))
    @py_assert1 = obj.executable
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=599)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.executable\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


class CheckCounted(versions.Check):

    def __init__(self, return_value=True, expected=(1, 1)):
        self.count = 0
        self.return_value = return_value
        (versions.Check.__init__)(self, 'counted {}', operator.eq, *expected)

    def _do_check_version(self, current, reference):
        @py_assert1 = current == reference
        if @py_assert1 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=614)
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (current, reference)) % {'py0':@pytest_ar._saferepr(current) if 'current' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(current) else 'current',  'py2':@pytest_ar._saferepr(reference) if 'reference' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reference) else 'reference'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        self.count += 1
        return self.return_value


def test_requirementobj__call__result_is_cached():
    counter = CheckCounted()
    obj = versions.RequirementObj(call=(lambda : 'v1.1.3'),
      search='(\\d)\\.(\\d)',
      checks=counter)
    obj()
    obj()
    @py_assert1 = counter.count
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=628)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.count\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(counter) if 'counter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(counter) else 'counter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_requirementobj__call__result_is_cached_unless_forced():
    counter = CheckCounted()
    obj = versions.RequirementObj(call=(lambda : 'v1.1.3'),
      search='(\\d)\\.(\\d)',
      checks=counter)
    obj()
    obj(force=True)
    @py_assert1 = counter.count
    @py_assert4 = 2
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=640)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.count\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(counter) if 'counter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(counter) else 'counter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_requirementobj__call__check_fails__function():
    expected = 'Version requirements not met for test#1; please refer\nto the PALEOMIX documentation for more information.\n\n    Version:       v1.0.x\n    Required:      at least v1.1.x'
    obj = versions.RequirementObj(call=(lambda : 'v1.0.3'),
      search='(\\d)\\.(\\d)',
      checks=(versions.GE(1, 1)),
      name='test#1')
    try:
        obj()
        @py_assert0 = False
        if @py_assert0 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=660)
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None
    except versions.VersionRequirementError as error:
        @py_assert2 = str(error)
        @py_assert4 = @py_assert2 == expected
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=662)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None


def test_requirementobj__call__check_fails():
    expected = "Version requirements not met for test#1; please refer\nto the PALEOMIX documentation for more information.\n\nAttempted to run command:\n    $ /usr/bin/python -c import sys; sys.stdout.write('v1.0.2'); sys.exit(0);\n    Version:       v1.0.x\n    Required:      at least v1.1.x"
    obj = versions.RequirementObj(call=(_echo_version('v1.0.2')),
      search='(\\d)\\.(\\d)',
      checks=(versions.GE(1, 1)),
      name='test#1')
    try:
        obj()
        @py_assert0 = False
        if @py_assert0 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=685)
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None
    except versions.VersionRequirementError as error:
        @py_assert2 = str(error)
        @py_assert4 = @py_assert2 == expected
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=687)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None


def test_requirementobj__call__check_fails__jre_outdated():
    expected = "Version could not be determined for test#1:\n\nAttempted to run command:\n    $ /usr/bin/python -c import sys; sys.stdout.write('UnsupportedClassVersionError'); sys.exit(0);\n\nThe version of the Java Runtime Environment on this\nsystem is too old; please check the the requirement\nfor the program and upgrade your version of Java.\n\nSee the documentation for more information."
    value = 'UnsupportedClassVersionError'
    obj = versions.RequirementObj(call=(_echo_version(value)),
      search='(\\d)\\.(\\d)',
      checks=(versions.GE(1, 1)),
      name='test#1')
    try:
        obj()
        @py_assert0 = False
        if @py_assert0 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=714)
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None
    except versions.VersionRequirementError as error:
        @py_assert2 = str(error)
        @py_assert4 = @py_assert2 == expected
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=716)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None


_CAN_PICKLE_VALUES = (
 versions.EQ(1, 2, 3),
 versions.GE(1, 2, 3),
 versions.LT(1, 2, 3),
 versions.Any(),
 versions.And(versions.EQ(1, 2, 3)),
 versions.Or(versions.GE(1, 2, 3)))

@pytest.mark.parametrize('obj', _CAN_PICKLE_VALUES)
def test_check__can_pickle(obj):
    pickle.dumps(obj)


def test_requirement__obj_is_cached_for_same_values():
    obj1 = versions.Requirement('echo', '', versions.LT(1))
    obj2 = versions.Requirement('echo', '', versions.LT(1))
    @py_assert1 = obj1 is obj2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=746)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (obj1, obj2)) % {'py0':@pytest_ar._saferepr(obj1) if 'obj1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj1) else 'obj1',  'py2':@pytest_ar._saferepr(obj2) if 'obj2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj2) else 'obj2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_requirement__new_obj_if_call_differ():
    obj1 = versions.Requirement('echo', '', versions.LT(1))
    obj2 = versions.Requirement('true', '', versions.LT(1))
    @py_assert1 = obj1 is not obj2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=752)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py2)s', ), (obj1, obj2)) % {'py0':@pytest_ar._saferepr(obj1) if 'obj1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj1) else 'obj1',  'py2':@pytest_ar._saferepr(obj2) if 'obj2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj2) else 'obj2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_requirement__new_obj_if_search_differ():
    obj1 = versions.Requirement('echo', '(\\d+)', versions.LT(1))
    obj2 = versions.Requirement('echo', '', versions.LT(1))
    @py_assert1 = obj1 is not obj2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=758)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py2)s', ), (obj1, obj2)) % {'py0':@pytest_ar._saferepr(obj1) if 'obj1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj1) else 'obj1',  'py2':@pytest_ar._saferepr(obj2) if 'obj2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj2) else 'obj2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_requirement__new_obj_if_checks_differ():
    obj1 = versions.Requirement('echo', '', versions.GE(1))
    obj2 = versions.Requirement('echo', '', versions.LT(1))
    @py_assert1 = obj1 is not obj2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=764)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py2)s', ), (obj1, obj2)) % {'py0':@pytest_ar._saferepr(obj1) if 'obj1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj1) else 'obj1',  'py2':@pytest_ar._saferepr(obj2) if 'obj2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj2) else 'obj2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_requirement__same_obj_if_name_differ():
    obj1 = versions.Requirement('echo', '', versions.GE(1))
    @py_assert1 = obj1.name
    @py_assert4 = 'echo'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=769)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj1) if 'obj1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj1) else 'obj1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    obj2 = versions.Requirement('echo', '', (versions.GE(1)), name='foo')
    @py_assert1 = obj2.name
    @py_assert4 = 'foo'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=771)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj2) if 'obj2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj2) else 'obj2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = obj1 is obj2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=772)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (obj1, obj2)) % {'py0':@pytest_ar._saferepr(obj1) if 'obj1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj1) else 'obj1',  'py2':@pytest_ar._saferepr(obj2) if 'obj2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj2) else 'obj2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    obj3 = versions.Requirement('echo', '', (versions.GE(1)), name='bar')
    @py_assert1 = obj3.name
    @py_assert4 = 'bar'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=775)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj3) if 'obj3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj3) else 'obj3',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = obj2 is obj3
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=776)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (obj2, obj3)) % {'py0':@pytest_ar._saferepr(obj2) if 'obj2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj2) else 'obj2',  'py2':@pytest_ar._saferepr(obj3) if 'obj3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj3) else 'obj3'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    obj4 = versions.Requirement('echo', '', versions.GE(1))
    @py_assert1 = obj3.name
    @py_assert4 = 'bar'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=779)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj3) if 'obj3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj3) else 'obj3',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = obj3 is obj4
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=780)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (obj3, obj4)) % {'py0':@pytest_ar._saferepr(obj3) if 'obj3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj3) else 'obj3',  'py2':@pytest_ar._saferepr(obj4) if 'obj4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj4) else 'obj4'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_requirement_highest_priority_overrides():
    obj1 = versions.Requirement('echo', '', (versions.LT(1)), priority=0)
    @py_assert1 = obj1.priority
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=785)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.priority\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj1) if 'obj1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj1) else 'obj1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    obj2 = versions.Requirement('echo', '', (versions.LT(1)), priority=5)
    @py_assert1 = obj1 is obj2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=787)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (obj1, obj2)) % {'py0':@pytest_ar._saferepr(obj1) if 'obj1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj1) else 'obj1',  'py2':@pytest_ar._saferepr(obj2) if 'obj2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj2) else 'obj2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = obj2.priority
    @py_assert4 = 5
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=788)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.priority\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj2) if 'obj2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj2) else 'obj2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_requirement_highest_priority_retained():
    obj1 = versions.Requirement('echo', '', (versions.LT(1)), priority=5)
    @py_assert1 = obj1.priority
    @py_assert4 = 5
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=793)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.priority\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj1) if 'obj1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj1) else 'obj1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    obj2 = versions.Requirement('echo', '', (versions.LT(1)), priority=0)
    @py_assert1 = obj1 is obj2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=795)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (obj1, obj2)) % {'py0':@pytest_ar._saferepr(obj1) if 'obj1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj1) else 'obj1',  'py2':@pytest_ar._saferepr(obj2) if 'obj2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj2) else 'obj2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = obj2.priority
    @py_assert4 = 5
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/versions_test.py', lineno=796)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.priority\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj2) if 'obj2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj2) else 'obj2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None