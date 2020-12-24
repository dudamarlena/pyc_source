# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/makefile_test.py
# Compiled at: 2019-10-20 09:12:08
# Size of source mod 2**32: 39108 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, pytest
from paleomix.common.makefile import DEFAULT_NOT_SET, REQUIRED_VALUE, MakefileError, MakefileSpec, read_makefile, process_makefile, WithoutDefaults, IsInt, IsUnsignedInt, IsFloat, IsBoolean, IsStr, IsNone, ValueIn, ValuesIntersect, ValuesSubsetOf, ValueMissing, And, Or, Not, StringIn, StringStartsWith, StringEndsWith, IsListOf, IsDictOf, PreProcessMakefile
_DUMMY_PATH = ('a', 'random', 'path')
_DUMMY_PATH_STR = ':'.join(_DUMMY_PATH)

class Unhashable:
    __hash__ = None


_COMMON_INVALID_VALUES = {None: None, 
 False: False, (): (), 
 'list_1': [], 
 'dict_1': {}, 
 'no_hash_1': [Unhashable()], 
 'no_hash_2': (Unhashable(),), 
 'dict_2': {None: Unhashable()}, 
 'obj_1': object, 
 'obj_2': object()}

def _common_invalid_values(exclude=(), extra=()):
    selection = list(extra)
    for key, value in _COMMON_INVALID_VALUES.items():
        if key not in exclude:
            selection.append(value)

    return selection


def test_dir():
    return os.path.dirname(os.path.dirname(__file__))


def test_file(*args):
    return (os.path.join)(test_dir(), 'data', *args)


def setup_module():
    timestamps = {test_file('simple.yaml'): 1120719000}
    for filename, timestamp in timestamps.items():
        os.utime(filename, (timestamp, timestamp))


def test_makefilespec__description_is_set():
    desc = 'a random description'
    spec = MakefileSpec(description=desc)
    @py_assert1 = spec.description
    @py_assert3 = @py_assert1 == desc
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=118)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py4)s', ), (@py_assert1, desc)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(desc) if 'desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(desc) else 'desc'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_makefilespec__meets_spec_must_be_implemented():
    spec = MakefileSpec(description='some description')
    with pytest.raises(NotImplementedError):
        spec(_DUMMY_PATH, 1)


def test_is_int__accepts_integers():
    spec = IsInt()
    spec(_DUMMY_PATH, 1234)
    spec(_DUMMY_PATH, 0)
    spec(_DUMMY_PATH, -1234)


@pytest.mark.parametrize('value', _common_invalid_values())
def test_is_int__rejects_not_int(value):
    spec = IsInt()
    with pytest.raises(MakefileError, match='Expected value: an integer'):
        spec(_DUMMY_PATH, value)


def test_is_int__default_description():
    spec = IsInt()
    @py_assert1 = spec.description
    @py_assert4 = 'an integer'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=148)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_int__custom_description():
    custom_desc = 'any old integer'
    spec = IsInt(description=custom_desc)
    @py_assert1 = spec.description
    @py_assert3 = @py_assert1 == custom_desc
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=154)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py4)s', ), (@py_assert1, custom_desc)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(custom_desc) if 'custom_desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(custom_desc) else 'custom_desc'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_int__default_not_set():
    spec = IsInt()
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=159)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_int__default_set__valid_value():
    spec = IsInt(default=7913)
    @py_assert1 = spec.default
    @py_assert4 = 7913
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=164)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_int__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        IsInt(default='abc')


def test_is_unsigned_int__accepts_non_negative_integers():
    spec = IsUnsignedInt()
    spec(_DUMMY_PATH, 1234)
    spec(_DUMMY_PATH, 0)


@pytest.mark.parametrize('value', _common_invalid_values(extra=(-1, )))
def test_is_unsigned_int__rejects_not_unsigned_int(value):
    spec = IsUnsignedInt()
    with pytest.raises(MakefileError, match='Expected value: an unsigned integer'):
        spec(_DUMMY_PATH, value)


def test_is_unsigned_int__default_description():
    spec = IsUnsignedInt()
    @py_assert1 = spec.description
    @py_assert4 = 'an unsigned integer'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=192)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_unsigned_int__custom_description():
    custom_desc = 'any old unsigned integer'
    spec = IsUnsignedInt(description=custom_desc)
    @py_assert1 = spec.description
    @py_assert3 = @py_assert1 == custom_desc
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=198)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py4)s', ), (@py_assert1, custom_desc)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(custom_desc) if 'custom_desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(custom_desc) else 'custom_desc'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_unsigned_int__default_not_set():
    spec = IsUnsignedInt()
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=203)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_unsigned_int__default_set__valid_value():
    spec = IsUnsignedInt(default=7913)
    @py_assert1 = spec.default
    @py_assert4 = 7913
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=208)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_unsigned_int__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        IsUnsignedInt(default=(-3))


def test_is_float__accepts_float():
    spec = IsFloat()
    spec(_DUMMY_PATH, 1.0)


@pytest.mark.parametrize('value', _common_invalid_values(extra=(0, )))
def test_is_float__rejects_not_float(value):
    spec = IsFloat()
    with pytest.raises(MakefileError, match='Expected value: a float'):
        spec(_DUMMY_PATH, value)


def test_is_float__default_description():
    spec = IsFloat()
    @py_assert1 = spec.description
    @py_assert4 = 'a float'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=235)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_float__custom_description():
    custom_desc = 'a floaty, float'
    spec = IsFloat(description=custom_desc)
    @py_assert1 = spec.description
    @py_assert3 = @py_assert1 == custom_desc
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=241)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py4)s', ), (@py_assert1, custom_desc)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(custom_desc) if 'custom_desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(custom_desc) else 'custom_desc'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_float__default_not_set():
    spec = IsFloat()
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=246)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_float__default_set__valid_value():
    spec = IsFloat(default=3.14)
    @py_assert1 = spec.default
    @py_assert4 = 3.14
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=251)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_float__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        IsFloat(default='abc')


def test_is_boolean__accepts_boolean():
    spec = IsBoolean()
    spec(_DUMMY_PATH, False)


@pytest.mark.parametrize('value', _common_invalid_values(exclude=(False, ), extra=(0, )))
def test_is_boolean__rejects_not_boolean(value):
    spec = IsBoolean()
    with pytest.raises(MakefileError, match='Expected value: a boolean'):
        spec(_DUMMY_PATH, value)


def test_is_boolean__default_description():
    spec = IsBoolean()
    @py_assert1 = spec.description
    @py_assert4 = 'a boolean'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=278)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_boolean__custom_description():
    custom_desc = 'True or False'
    spec = IsBoolean(description=custom_desc)
    @py_assert1 = spec.description
    @py_assert3 = @py_assert1 == custom_desc
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=284)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py4)s', ), (@py_assert1, custom_desc)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(custom_desc) if 'custom_desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(custom_desc) else 'custom_desc'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_boolean__default_not_set():
    spec = IsBoolean()
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=289)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_boolean__default_set__valid_value():
    spec = IsBoolean(default=True)
    @py_assert1 = spec.default
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=294)
    if not @py_assert1:
        @py_format3 = 'assert %(py2)s\n{%(py2)s = %(py0)s.default\n}' % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None


def test_is_boolean__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        IsBoolean(default='abc')


def test_is_str__accepts_standard_str():
    spec = IsStr()
    spec(_DUMMY_PATH, 'abc')


def test_is_str__rejects_empty_str():
    with pytest.raises(MakefileError):
        IsStr()(_DUMMY_PATH, '')
    with pytest.raises(MakefileError):
        IsStr(min_len=1)(_DUMMY_PATH, '')
    with pytest.raises(MakefileError):
        IsStr(min_len=2)(_DUMMY_PATH, '')
    with pytest.raises(MakefileError):
        IsStr(min_len=3)(_DUMMY_PATH, '')


def test_is_str__accepts_empty_str():
    spec = IsStr(min_len=0)
    spec(_DUMMY_PATH, '')


def test_is_str__rejects_negative_min_len():
    with pytest.raises(ValueError):
        IsStr(min_len=(-1))


@pytest.mark.parametrize('value', _common_invalid_values(extra=(1, )))
def test_is_str__rejects_not_str(value):
    spec = IsStr()
    with pytest.raises(MakefileError, match='Expected value: a non-empty string'):
        spec(_DUMMY_PATH, value)


def test_is_str__default_description():
    spec = IsStr()
    @py_assert1 = spec.description
    @py_assert4 = 'a non-empty string'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=342)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_str__custom_description():
    custom_desc = 'a ball of string'
    spec = IsStr(description=custom_desc)
    @py_assert1 = spec.description
    @py_assert3 = @py_assert1 == custom_desc
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=348)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py4)s', ), (@py_assert1, custom_desc)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(custom_desc) if 'custom_desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(custom_desc) else 'custom_desc'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_str__default_not_set():
    spec = IsStr()
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=353)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_str__default_set__valid_value():
    spec = IsStr(default='abc')
    @py_assert1 = spec.default
    @py_assert4 = 'abc'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=358)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_str__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        IsStr(default=17)


def test_is_str__min_len_0():
    spec = IsStr(min_len=0)
    spec(_DUMMY_PATH, '')
    spec(_DUMMY_PATH, 'a')
    spec(_DUMMY_PATH, 'ab')


def test_is_str__min_len_1():
    spec = IsStr(min_len=1)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, '')
    spec(_DUMMY_PATH, 'a')
    spec(_DUMMY_PATH, 'ab')


def test_is_str__min_len_2():
    spec = IsStr(min_len=2)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, '')
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 'a')
    spec(_DUMMY_PATH, 'ab')
    spec(_DUMMY_PATH, 'abc')


def test_is_none__accepts_none():
    spec = IsNone()
    spec(_DUMMY_PATH, None)


@pytest.mark.parametrize('value', _common_invalid_values(exclude=(None, ), extra=(0,
                                                                                  '')))
def test_is_none__rejects_not_none(value):
    spec = IsNone()
    with pytest.raises(MakefileError, match='Expected value: null or not set'):
        spec(_DUMMY_PATH, value)


def test_is_none__default_description():
    spec = IsNone()
    @py_assert1 = spec.description
    @py_assert4 = 'null or not set'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=412)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_none__custom_description():
    custom_desc = 'NOTHING!'
    spec = IsNone(description=custom_desc)
    @py_assert1 = spec.description
    @py_assert3 = @py_assert1 == custom_desc
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=418)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py4)s', ), (@py_assert1, custom_desc)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(custom_desc) if 'custom_desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(custom_desc) else 'custom_desc'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_none__default_not_set():
    spec = IsNone()
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=423)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_none__default_not_implemented_for_is_none():
    with pytest.raises(NotImplementedError):
        IsNone(default=None)


def test_value_in__single_value_in_set():
    spec = ValueIn(list(range(5)))
    spec(_DUMMY_PATH, 1)


def test_value_in__single_value_not_in_set():
    spec = ValueIn(list(range(5)))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 5)


def test_value_in__single_value_in_set__with_key():
    spec = ValueIn((list(range(5))), key=len)
    spec(_DUMMY_PATH, 'a')


def test_value_in__single_value_not_in_set__with_key():
    spec = ValueIn((list(range(5))), key=len)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 'abcde')


def test_value_in__case_sensitive__value_in_set():
    spec = ValueIn(('Abc', 'bCe', 'cdE'))
    spec(_DUMMY_PATH, 'bCe')


def test_value_in__case_sensitive__value_in_not_set():
    spec = ValueIn(('Abc', 'bCe', 'cdE'))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 'Bce')


def test_value_in__default_description():
    spec = ValueIn(('Abc', 'bCe', 'cdE'))
    @py_assert1 = spec.description
    @py_assert4 = "value in 'Abc', 'bCe', or 'cdE'"
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=471)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_value_in__custom_description():
    spec = ValueIn(('Abc', 'bCe', 'cdE'), description='One of {rvalue}')
    @py_assert1 = spec.description
    @py_assert4 = "One of 'Abc', 'bCe', or 'cdE'"
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=476)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_value_in__default_not_set():
    spec = ValueIn(list(range(5)))
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=481)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_value_in__default_set__valid_value():
    spec = ValueIn((list(range(5))), default=4)
    @py_assert1 = spec.default
    @py_assert4 = 4
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=486)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_value_in__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        ValueIn((list(range(5))), default=5)


@pytest.mark.parametrize('value', _common_invalid_values(extra=('foo', )))
def test_is_value_in__handles_types(value):
    spec = ValueIn((1, 2, 3, 4))
    with pytest.raises(MakefileError, match='Expected value: value in 1, 2, 3, or 4'):
        spec(_DUMMY_PATH, value)


def test_intersects__single_value_in_set():
    spec = ValuesIntersect(list(range(5)))
    spec(_DUMMY_PATH, [1])


def test_intersects__multiple_values_in_set():
    spec = ValuesIntersect(list(range(5)))
    spec(_DUMMY_PATH, [1, 4])


def test_intersects__single_value_not_in_set():
    spec = ValuesIntersect(list(range(5)))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, [5])


def test_intersects__some_values_in_set():
    spec = ValuesIntersect(list(range(5)))
    spec(_DUMMY_PATH, [4, 5])


def test_intersects__empty_set():
    spec = ValuesIntersect(list(range(5)))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, [])


def test_intersects__case_sensitive__value_in_set():
    spec = ValuesIntersect(('Abc', 'bCe', 'cdE'))
    spec(_DUMMY_PATH, ['bCe'])


def test_intersects__case_sensitive__value_in_not_set():
    spec = ValuesIntersect(('Abc', 'bCe', 'cdE'))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, ['Bce'])


def test_intersects__chars__case_sensitive():
    spec = ValuesIntersect('abcdefghijkl')
    spec(_DUMMY_PATH, 'a big deal')


def test_intersects__chars__case_sensitive__rejects_differences_in_case():
    spec = ValuesIntersect('abcdefghijkl')
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 'A BIG DEAL')


def test_intersects__rejects_dictionary():
    spec = ValuesIntersect('abc')
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, {'a':1,  'd':2})


def test_intersects__default_not_set():
    spec = ValuesIntersect(list(range(5)))
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=563)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_intersects__default_set__valid_value():
    spec = ValuesIntersect((list(range(5))), default=[3, 4])
    @py_assert1 = spec.default
    @py_assert4 = [
     3, 4]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=568)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_intersects__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        ValuesIntersect((list(range(5))), default=[5])


@pytest.mark.parametrize('value', _common_invalid_values(extra=('foo', )))
def test_intersects__handles_types(value):
    spec = ValuesIntersect(list(range(5)))
    with pytest.raises(MakefileError,
      match='Expected value: one or more of 0, 1, 2, 3, and 4'):
        spec(_DUMMY_PATH, value)


def test_subset_of__single_value_in_set():
    spec = ValuesSubsetOf(list(range(5)))
    spec(_DUMMY_PATH, [1])


def test_subset_of__multiple_values_in_set():
    spec = ValuesSubsetOf(list(range(5)))
    spec(_DUMMY_PATH, [1, 4])


def test_subset_of__empty_set_is_subset():
    spec = ValuesSubsetOf(list(range(5)))
    spec(_DUMMY_PATH, [])


def test_subset_of__single_value_not_in_set():
    spec = ValuesSubsetOf(list(range(5)))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, [5])


def test_subset_of__multiple_values_not_in_set():
    spec = ValuesSubsetOf(list(range(5)))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, [4, 5])


def test_subset_of__empty_set():
    spec = ValuesSubsetOf(list(range(5)))
    spec(_DUMMY_PATH, [])


def test_subset_of__case_sensitive__value_in_set():
    spec = ValuesSubsetOf(('Abc', 'bCe', 'cdE'))
    spec(_DUMMY_PATH, ['bCe'])


def test_subset_of__case_sensitive__value_in_not_set():
    spec = ValuesSubsetOf(('Abc', 'bCe', 'cdE'))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, ['Bce'])


def test_subset_of__chars__case_sensitive():
    spec = ValuesSubsetOf('abcdefghijkl ')
    spec(_DUMMY_PATH, 'a big deal')


def test_subset_of__chars__case_sensitive__rejects_differences_in_case():
    spec = ValuesSubsetOf('abcdefghijkl ')
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 'A big DEAL')


def test_subset_of__rejects_dictionary():
    spec = ValuesIntersect('abc')
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, {'a':1,  'b':2})


def test_subset_of__default_not_set():
    spec = ValuesSubsetOf(list(range(5)))
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=652)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_subset_of__default_set__valid_value():
    spec = ValuesSubsetOf((list(range(5))), default=[3, 4])
    @py_assert1 = spec.default
    @py_assert4 = [
     3, 4]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=657)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_subset_of__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        ValuesSubsetOf((list(range(5))), default=[4, 5])


@pytest.mark.parametrize('value', _common_invalid_values(extra=('foo', ), exclude=('list_1', ())))
def test_subset_of__handles_types(value):
    spec = ValuesSubsetOf(list(range(5)))
    with pytest.raises(MakefileError,
      match='Expected value: subset of 0, 1, 2, 3, and 4'):
        spec(_DUMMY_PATH, value)


def test_and__accepts_when_all_true():
    spec = And(IsFloat, ValueIn((0.0, 1, 2)))
    spec(_DUMMY_PATH, 0.0)


def test_and__rejects_when_first_is_false():
    spec = And(IsFloat, ValueIn((0.0, 1, 2)))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 1)


def test_and__rejects_when_second_is_false():
    spec = And(IsFloat, ValueIn((0.0, 1, 2)))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 3.0)


def test_and__rejects_when_both_is_false():
    spec = And(IsFloat, ValueIn((0.0, 1, 2)))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 3)


def test_and__rejects_no_tests():
    with pytest.raises(ValueError):
        And()


def test_and__rejects_non_spec_tests():
    with pytest.raises(TypeError):
        And(id)


def test_and__default_not_set():
    spec = And(IsInt, ValueIn(list(range(10))))
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=716)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_and__default_set__valid_value():
    spec = And(IsInt, (ValueIn(list(range(30)))), default=20)
    @py_assert1 = spec.default
    @py_assert4 = 20
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=721)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_and__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        And(IsInt, (ValueIn((1, ))), default=5)


def test_and__defaults_not_set_in_specs():
    with pytest.raises(ValueError):
        And(IsInt(default=10), ValueIn(list(range(100))))


def test_or__accepts_first_test():
    spec = Or(IsStr, IsBoolean)
    spec(_DUMMY_PATH, 'Foo')


def test_or__accepts_second_test():
    spec = Or(IsStr, IsBoolean)
    spec(_DUMMY_PATH, False)


def test_or__rejects_if_both_specs_fail():
    spec = Or(IsStr, IsBoolean)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 1)


def test_or__rejects_no_tests():
    with pytest.raises(ValueError):
        Or()


def test_or__rejects_non_spec_tests():
    with pytest.raises(TypeError):
        Or(id)


def test_or__default_not_set():
    spec = Or(IsInt, ValueIn((10, )))
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=767)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_or__default_set__valid_value():
    spec = Or(IsInt, (ValueIn((10, ))), default=17)
    @py_assert1 = spec.default
    @py_assert4 = 17
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=772)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_or__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        Or(IsInt, (ValueIn((10, ))), default=5.5)


def test_or__defaults_not_set_in_specs():
    with pytest.raises(ValueError):
        Or(IsInt(default=10), ValueIn((10, )))


def test_not__accepts_when_test_is_false():
    spec = Not(IsInt)
    spec(_DUMMY_PATH, True)


def test_not__rejects_when_test_is_true():
    spec = Not(IsInt)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 1)


def test_not__defaults_not_set_in_specs():
    with pytest.raises(ValueError):
        Not(IsInt(default=10))


def test_string_in__case_sensitive__value_in_set():
    spec = StringIn(('Abc', 'bCe', 'cdE'))
    spec(_DUMMY_PATH, 'bCe')


def test_string_in__case_insensitive__value_in_set():
    spec = StringIn(('Abc', 'bCe', 'cdE'))
    spec(_DUMMY_PATH, 'Bce')


def test_string_in__case_insensitive__value_not_set():
    spec = StringIn(('Abc', 'bCe', 'cdE'))
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 'ABce')


def test_string_in__case_insensitive__mixed_string__non_string_found():
    spec = StringIn(('A', 'c', 'B', 1, 2, 3))
    spec(_DUMMY_PATH, 1)


def test_string_in__case_insensitive__mixed_string__string_found():
    spec = StringIn(('A', 'c', 'B', 1, 2, 3))
    spec(_DUMMY_PATH, 'a')


def test_string_in__default_not_set():
    spec = StringIn('ABCDEFGH')
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=839)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_string_in__default_set__valid_value():
    spec = StringIn('ABCDEFGH', default='e')
    @py_assert1 = spec.default
    @py_assert4 = 'e'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=844)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_string_in__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        StringIn('ABCDEFGH', default='i')


@pytest.mark.parametrize('value', _common_invalid_values(extra=('foo', )))
def test_string_in__handles_types(value):
    spec = StringIn('ABC')
    with pytest.raises(MakefileError, match="Expected value: one of 'A', 'B', or 'C'"):
        spec(_DUMMY_PATH, value)


def test_string_starts_with__accepts_standard_str():
    spec = StringStartsWith('A_')
    spec(_DUMMY_PATH, 'A_BC')


def test_string_starts_with__rejects_string_without_prefix():
    spec = StringStartsWith('A_')
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 'B_GHI')


@pytest.mark.parametrize('value', _common_invalid_values(extra=(1, )))
def test_string_starts_with__rejects_not_uppercase_str(value):
    spec = StringStartsWith('Foo')
    with pytest.raises(MakefileError,
      match="Expected value: a string with prefix 'Foo'"):
        spec(_DUMMY_PATH, value)


def test_string_starts_with__default_not_set():
    spec = StringStartsWith('Foo')
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=886)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_string_starts_with__default_set__valid_value():
    spec = StringStartsWith('Foo', default='FooBar')
    @py_assert1 = spec.default
    @py_assert4 = 'FooBar'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=891)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_string_starts_with__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        StringStartsWith('FooBar', default='BarFoo')


def test_string_ends_with__accepts_standard_str():
    spec = StringEndsWith('_A')
    spec(_DUMMY_PATH, 'BC_A')


def test_string_ends_with__rejects_string_without_prefix():
    spec = StringEndsWith('_A')
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, 'GHI_B')


@pytest.mark.parametrize('value', _common_invalid_values(extra=(1, )))
def test_string_ends_with__rejects_not_uppercase_str(value):
    spec = StringEndsWith('Foo')
    with pytest.raises(MakefileError,
      match="Expected value: a string with postfix 'Foo'"):
        spec(_DUMMY_PATH, value)


def test_string_ends_with__default_not_set():
    spec = StringEndsWith('Foo')
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=926)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_string_ends_with__default_set__valid_value():
    spec = StringEndsWith('Bar', default='FooBar')
    @py_assert1 = spec.default
    @py_assert4 = 'FooBar'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=931)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_string_ends_with__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        StringEndsWith('FooBar', default='BarFoo')


def test_is_list_of__empty_list_always_ok():
    spec = IsListOf(IsInt)
    spec(_DUMMY_PATH, [])


def test_is_list_of__list_of_ints_accepted():
    spec = IsListOf(IsInt)
    spec(_DUMMY_PATH, [1, 2, 3])


def test_is_list_of__list_of_non_ints_rejected():
    spec = IsListOf(IsInt)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, ['a', 'b', 'c'])


def test_is_list_of__mixed_list_rejected():
    spec = IsListOf(IsInt)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, [1, 'b', 3])


def test_is_list_of__default_description():
    spec = IsListOf(IsInt, IsFloat)
    @py_assert1 = spec.description
    @py_assert4 = '[(an integer) or (a float), ...]'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=968)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_list_of__non_list_rejected():
    spec = IsListOf(IsInt)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, {1: 2})


def test_is_list_of__default_not_set():
    spec = IsListOf(IsInt)
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=979)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_list_of__default_set__valid_value():
    spec = IsListOf(IsInt, default=(list(range(5))))
    @py_assert1 = spec.default
    @py_assert6 = 5
    @py_assert8 = range(@py_assert6)
    @py_assert10 = list(@py_assert8)
    @py_assert3 = @py_assert1 == @py_assert10
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=984)
    if not @py_assert3:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py11)s\n{%(py11)s = %(py4)s(%(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n})\n}', ), (@py_assert1, @py_assert10)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py5':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = None


def test_is_list_of__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        IsListOf(IsInt, default=17)


def test_is_list_of__defaults_not_set_in_specs():
    with pytest.raises(ValueError):
        IsListOf(IsInt(default=10))


def test_is_dict_of__empty_dict_always_ok():
    spec = IsDictOf(IsInt, IsStr)
    spec(_DUMMY_PATH, {})


def test_is_dict_of__correct_key_and_value_accepted():
    spec = IsDictOf(IsInt, IsStr)
    spec(_DUMMY_PATH, {1: 'foo'})


def test_is_dict_of__wrong_key_and_correct_value_rejected():
    spec = IsDictOf(IsInt, IsStr)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, {1.5: 'foo'})


def test_is_dict_of__correct_key_and_wrong_value_rejected():
    spec = IsDictOf(IsInt, IsStr)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, {1: 1})


def test_is_dict_of__mixed_rejected():
    spec = IsDictOf(IsInt, IsStr)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, {1:1,  2:'foo'})


def test_is_dict_of__default_description():
    spec = IsDictOf(IsInt, IsStr)
    @py_assert1 = spec.description
    @py_assert4 = '{(an integer) : (a non-empty string)}'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1032)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_dict_of__rejects_non_dict():
    spec = IsDictOf(IsInt, IsStr)
    with pytest.raises(MakefileError):
        spec(_DUMMY_PATH, [])


def test_is_dict_of__default_not_set():
    spec = IsDictOf(IsInt, IsInt)
    @py_assert1 = spec.default
    @py_assert3 = @py_assert1 is DEFAULT_NOT_SET
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1043)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} is %(py4)s', ), (@py_assert1, DEFAULT_NOT_SET)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DEFAULT_NOT_SET) if 'DEFAULT_NOT_SET' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DEFAULT_NOT_SET) else 'DEFAULT_NOT_SET'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_is_dict_of__default_set__valid_value():
    spec = IsDictOf(IsInt, IsInt, default={1: 2})
    @py_assert1 = spec.default
    @py_assert4 = {1: 2}
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1048)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.default\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_is_dict_of__default_set__must_meet_spec():
    with pytest.raises(ValueError):
        IsDictOf(IsInt, IsInt, default={1: 'b'})


def test_is_dict_of__defaults_not_set_in_key_specs():
    with pytest.raises(ValueError):
        IsDictOf(IsInt(default=10), IsInt)


def test_is_dict_of__defaults_not_set_in_value_specs():
    with pytest.raises(ValueError):
        IsDictOf(IsInt, IsInt(default=10))


_PATH_IN_EXCEPTION_VALUES = (
 (
  IsInt(), 'foo'),
 (
  IsUnsignedInt(), -1),
 (
  IsFloat(), 'abc'),
 (
  IsBoolean(), 1),
 (
  IsStr(), 1),
 (
  IsNone(), 1),
 (
  ValueIn([1]), 2),
 (
  ValuesIntersect([1]), [2]),
 (
  ValuesSubsetOf([1]), [2]),
 (
  ValueMissing(), True),
 (
  And(IsStr), 1),
 (
  Or(IsStr), 1),
 (
  Not(IsInt), 1),
 (
  StringIn('abc'), 1),
 (
  StringStartsWith('FOO'), 1),
 (
  StringEndsWith('FOO'), 1),
 (
  IsListOf(IsInt), 'foo'),
 (
  IsDictOf(IsInt, IsInt), 1))

@pytest.mark.parametrize('spec, value', _PATH_IN_EXCEPTION_VALUES)
def test_specs__path_is_displayed_in_exception(spec, value):
    with pytest.raises(MakefileError, match=_DUMMY_PATH_STR):
        spec(_DUMMY_PATH, value)


_MAKEFILE_SPEC_MET = (
 (
  {'B': 7}, {'A':IsInt,  'B':IsInt}),
 (
  {1: 'Abc'}, {IsStr: IsInt, IsInt: IsStr}),
 (
  {1: 'Abc'}, {IsStr(): IsInt, IsInt: IsStr()}),
 (
  {3: 14}, {IsInt: IsInt, 'A': IsInt}),
 (
  {'A': 23}, {IsInt: IsInt, 'A': IsInt}))

@pytest.mark.parametrize('makefile, spec', _MAKEFILE_SPEC_MET)
def test_process_makefile__dict_keys_found(makefile, spec):
    process_makefile(makefile, spec)


_MAKEFILE_SPEC_NOT_MET = (
 (
  {'C': 7}, {'A':IsInt,  'B':IsInt}),
 (
  {1.3: 'Abc'}, {IsStr: IsInt, IsInt: IsStr}),
 (
  {1.3: 'Abc'}, {IsStr(): IsInt, IsInt: IsStr()}),
 (
  {'C': 14}, {IsInt: IsInt, 'A': IsInt}),
 (
  {'A': 23}, {}))

@pytest.mark.parametrize('makefile, spec', _MAKEFILE_SPEC_NOT_MET)
def test_process_makefile__dict_keys_not_found(makefile, spec):
    with pytest.raises(MakefileError):
        process_makefile(makefile, spec)


def test_validate_makefile__unexpected_type_in_reference():
    current = {1: 2}
    specs = {IsInt: 2}
    with pytest.raises(TypeError):
        process_makefile(current, specs)


def test_validate_makefile__unexpected_type_in_current():
    current = {1: []}
    specs = {IsInt: {IsInt: IsInt}}
    with pytest.raises(MakefileError):
        process_makefile(current, specs)


def test_process_makefile__sets_missing_keys():
    current = {'A': 1}
    specs = {'A':IsInt(default=0),  'B':IsInt(default=-1),  'C':IsInt(default=-2)}
    expected = {'A':1,  'B':-1,  'C':-2}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1150)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__mixed_keys():
    current = {'A': 1}
    specs = {IsStr: IsInt, 'B': IsInt(default=(-1)), 'C': IsInt(default=(-2))}
    expected = {'A':1,  'B':-1,  'C':-2}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1158)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__sets_missing_recursive():
    current = {'A':1, 
     'B':{'C': 2}}
    specs = {'A':IsInt(default=0), 
     'B':{'C':IsInt(default=-1), 
      'D':IsInt(default=-2)}}
    expected = {'A':1, 
     'B':{'C':2,  'D':-2}}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1169)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__sets_missing_recursive__with_missing_substructure():
    current = {'A': 1}
    specs = {'A':IsInt(default=0), 
     'B':{'C':IsInt(default=-1), 
      'D':IsInt(default=-2)}}
    expected = {'A':1, 
     'B':{'C':-1,  'D':-2}}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1180)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__shared_subtrees_with_defaults():
    subtree = {'A':IsInt(default=1234), 
     'B':IsInt(default=5678)}
    specs = {'A':subtree,  'B':subtree}
    current = {'A':{'B': 17},  'B':{'A': 71}}
    expected = {'A':{'A':1234,  'B':17},  'B':{'A':71,  'B':5678}}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1189)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__shared_subtrees_with_defaults__defaults_disabled():
    subtree = {'A':IsInt(default=1234), 
     'B':IsInt(default=5678)}
    specs = {'A':subtree,  'B':WithoutDefaults(subtree)}
    current = {'A':{'B': 17},  'B':{'A': 71}}
    expected = {'A':{'A':1234,  'B':17},  'B':{'A': 71}}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1198)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__accept_when_required_value_is_set():
    current = {'A':1, 
     'B':{'C': 3}}
    expected = {'A':1,  'B':{'C': 3}}
    specs = {'A':IsInt,  'B':{'C': IsInt(default=REQUIRED_VALUE)}}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1206)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__fails_when_required_value_not_set():
    current = {'A': 1}
    specs = {'A':IsInt,  'B':{'C': IsInt(default=REQUIRED_VALUE)}}
    with pytest.raises(MakefileError):
        process_makefile(current, specs)


def test_process_makefile__fails_required_value_not_set_in_dynamic_subtree():
    current = {'A':1, 
     'B':{}}
    specs = {'A': IsInt, IsStr: {'C': IsInt(default=REQUIRED_VALUE)}}
    with pytest.raises(MakefileError):
        process_makefile(current, specs)


def test_process_makefile__accept_missing_value_if_in_implicit_subtree():
    current = {'A': 1}
    expected = {'A': 1}
    specs = {'A': IsInt, IsStr: {'C': IsInt(default=REQUIRED_VALUE)}}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1228)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__path_shown_in_exception_for_list():
    with pytest.raises(MakefileError, match=_DUMMY_PATH_STR):
        process_makefile({}, [], _DUMMY_PATH)


def test_process_makefile__path_shown_in_exception_for_dict():
    with pytest.raises(MakefileError, match=_DUMMY_PATH_STR):
        process_makefile([], {}, _DUMMY_PATH)


def test_process_makefile__implicit_subdict_is_allowed():
    current = {'A':1, 
     'B':None}
    expected = {'A':1,  'B':{'C': 3}}
    specs = {'A':IsInt,  'B':{'C': IsInt(default=3)}}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1246)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__list_types_accepted():
    current = {'A':1, 
     'B':[17, 'Foo']}
    expected = {'A':1,  'B':[17, 'Foo']}
    specs = {'A':IsInt,  'B':[IsInt, IsStr]}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1259)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__wrong_list_types():
    current = {'A':1, 
     'B':[17, 'foo']}
    specs = {'A':IsInt,  'B':[IsInt]}
    with pytest.raises(MakefileError):
        process_makefile(current, specs)


def test_process_makefile__missing_list_defaults_to_empty():
    current = {'A': 1}
    expected = {'A':1,  'B':{'C': []}}
    specs = {'A':IsInt,  'B':{'C': [IsInt]}}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1274)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__missing_list_default_value():
    current = {'A': 1}
    expected = {'A':1,  'B':[1, 2, 3]}
    specs = {'A':IsInt,  'B':IsListOf(IsInt, default=[1, 2, 3])}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1282)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__key_specified_but_no_entries():
    current = {'A':1, 
     'B':None}
    expected = {'A':1,  'B':[]}
    specs = {'A':IsInt,  'B':[IsInt]}
    result = process_makefile(current, specs)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1290)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_process_makefile__list_spec_must_contain_specs():
    specs = {'A':IsInt, 
     'B':[1, 2, 3]}
    with pytest.raises(TypeError):
        process_makefile({}, specs)


def test_process_makefile__list_spec_must_contain_only_specs():
    specs = {'A':IsInt, 
     'B':[1, 2, IsStr]}
    with pytest.raises(TypeError):
        process_makefile({}, specs)


def test_read_makefile__missing_file():
    with pytest.raises(IOError):
        read_makefile('does_not_exist.yaml', {})


def test_read_makefile__not_a_yaml_file():
    fpath = test_file('fasta_file.fasta')
    with pytest.raises(MakefileError):
        read_makefile(fpath, {})


def test_read_makefile__simple_file():
    specs = {'Defaults': {'First':IsFloat,  'Second':IsStr}}
    expected = {'Defaults': {'First':0.0001,  'Second':'a string'}}
    result = read_makefile(test_file('simple.yaml'), specs)
    @py_assert1 = expected == result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1326)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, result)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


class _PreProcess(PreProcessMakefile):

    def __call__(self, path, value):
        if isinstance(value, str):
            return (int(value), IsInt)
        else:
            return (
             value, IsInt)


def test__preprocess_makefile__missing_value():
    spec = {'Key': _PreProcess()}
    @py_assert0 = {}
    @py_assert4 = {}
    @py_assert7 = process_makefile(@py_assert4, spec)
    @py_assert2 = @py_assert0 == @py_assert7
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1344)
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py8)s\n{%(py8)s = %(py3)s(%(py5)s, %(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(process_makefile) if 'process_makefile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(process_makefile) else 'process_makefile',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None


def test__preprocess_makefile__expected_value():
    spec = {'Key': _PreProcess()}
    @py_assert0 = {'Key': 13}
    @py_assert4 = {'Key': 13}
    @py_assert7 = process_makefile(@py_assert4, spec)
    @py_assert2 = @py_assert0 == @py_assert7
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1349)
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py8)s\n{%(py8)s = %(py3)s(%(py5)s, %(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(process_makefile) if 'process_makefile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(process_makefile) else 'process_makefile',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None


def test__preprocess_makefile__processed_value():
    spec = {'Key': _PreProcess()}
    @py_assert0 = {'Key': 14}
    @py_assert4 = {'Key': '14'}
    @py_assert7 = process_makefile(@py_assert4, spec)
    @py_assert2 = @py_assert0 == @py_assert7
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1354)
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py8)s\n{%(py8)s = %(py3)s(%(py5)s, %(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(process_makefile) if 'process_makefile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(process_makefile) else 'process_makefile',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None


def test__preprocess_makefile__invalid_value():
    spec = {'Key': _PreProcess()}
    with pytest.raises(MakefileError):
        process_makefile({'Key': False}, spec)


def test__preprocess_makefile__invalid_string():
    spec = {'Key': _PreProcess()}
    with pytest.raises(ValueError):
        process_makefile({'Key': 'x14'}, spec)


class _PreProcessWithDefault(PreProcessMakefile):

    def __init__(self, default):
        self._default = default

    def __call__(self, path, value):
        if isinstance(value, str):
            return (int(value), IsInt)
        else:
            return (
             value, IsInt(default=(self._default)))


def test__preprocess_makefile__with_default__missing_value():
    spec = {'Key': _PreProcessWithDefault(314)}
    @py_assert0 = {'Key': 314}
    @py_assert4 = {}
    @py_assert7 = process_makefile(@py_assert4, spec)
    @py_assert2 = @py_assert0 == @py_assert7
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1383)
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py8)s\n{%(py8)s = %(py3)s(%(py5)s, %(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(process_makefile) if 'process_makefile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(process_makefile) else 'process_makefile',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None


def test__preprocess_makefile__with_default__expected_value():
    spec = {'Key': _PreProcessWithDefault(314)}
    @py_assert0 = {'Key': 14}
    @py_assert4 = {'Key': 14}
    @py_assert7 = process_makefile(@py_assert4, spec)
    @py_assert2 = @py_assert0 == @py_assert7
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/makefile_test.py', lineno=1388)
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py8)s\n{%(py8)s = %(py3)s(%(py5)s, %(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(process_makefile) if 'process_makefile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(process_makefile) else 'process_makefile',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(spec) if 'spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spec) else 'spec',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None