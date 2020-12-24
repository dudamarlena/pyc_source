# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py
# Compiled at: 2019-10-20 09:12:00
# Size of source mod 2**32: 25394 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from unittest.mock import call, Mock, patch
import pytest
from paleomix.atomiccmd.builder import AtomicCmdBuilder, AtomicCmdBuilderError, AtomicJavaCmdBuilder, AtomicMPICmdBuilder, apply_options, use_customizable_cli_parameters, create_customizable_cli_parameters

def test_builder__simple__call():
    builder = AtomicCmdBuilder(['ls'])
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=46)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__simple__str():
    builder = AtomicCmdBuilder('ls')
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=51)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__simple__iterable():
    builder = AtomicCmdBuilder(iter(['ls']))
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=56)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__complex():
    builder = AtomicCmdBuilder(['java', 'jar', '/a/jar'])
    @py_assert1 = builder.call
    @py_assert4 = [
     'java', 'jar', '/a/jar']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=61)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__kwargs__empty():
    builder = AtomicCmdBuilder(['ls'])
    @py_assert1 = builder.kwargs
    @py_assert4 = {}
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=66)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__kwargs():
    expected = {'IN_FILE':'/abc/def.txt', 
     'OUT_FILE':'/etc/fstab'}
    builder = AtomicCmdBuilder(['ls'], **expected)
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=72)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_builder__kwargs__set_cwd():
    builder = AtomicCmdBuilder(['ls'], set_cwd=True)
    @py_assert1 = builder.kwargs
    @py_assert4 = {'set_cwd': True}
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=77)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__set_option():
    builder = AtomicCmdBuilder('find')
    builder.set_option('-name', '*.txt')
    @py_assert1 = builder.call
    @py_assert4 = [
     'find', '-name', '*.txt']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=88)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__set_option__overwrite():
    builder = AtomicCmdBuilder('find')
    builder.set_option('-name', '*.txt', fixed=False)
    builder.set_option('-name', '*.bat')
    @py_assert1 = builder.call
    @py_assert4 = [
     'find', '-name', '*.bat']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=95)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__set_option__overwrite_fixed():
    builder = AtomicCmdBuilder('find')
    builder.set_option('-name', '*.txt')
    with pytest.raises(AtomicCmdBuilderError):
        builder.set_option('-name', '*.bat')


def test_builder__add_option():
    builder = AtomicCmdBuilder('find')
    builder.add_option('-name', '*.txt')
    @py_assert1 = builder.call
    @py_assert4 = [
     'find', '-name', '*.txt']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=113)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_option__overwrite():
    builder = AtomicCmdBuilder('find')
    builder.add_option('-name', '*.txt')
    builder.add_option('-or')
    builder.add_option('-name', '*.bat')
    @py_assert1 = builder.call
    @py_assert4 = [
     'find', '-name', '*.txt', '-or', '-name', '*.bat']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=121)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


_ADD_SET_OPTION = [
 AtomicCmdBuilder.add_option, AtomicCmdBuilder.set_option]

@pytest.mark.parametrize('setter', _ADD_SET_OPTION)
def test_builder__add_or_set_option__without_value(setter):
    builder = AtomicCmdBuilder('find')
    setter(builder, '-delete')
    @py_assert1 = builder.call
    @py_assert4 = [
     'find', '-delete']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=135)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.parametrize('setter', _ADD_SET_OPTION)
def test_builder__add_or_set_option__with_sep(setter):
    builder = AtomicCmdBuilder('find')
    setter(builder, '-size', '0', sep='=')
    @py_assert1 = builder.call
    @py_assert4 = [
     'find', '-size=0']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=142)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.parametrize('setter', _ADD_SET_OPTION)
def test_builder__add_or_set_option__with_non_str_value(setter):
    builder = AtomicCmdBuilder('find')
    setter(builder, '-size', 0)
    @py_assert1 = builder.call
    @py_assert4 = [
     'find', '-size', 0]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=149)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_or_set_option__add_and_set():
    builder = AtomicCmdBuilder('find')
    builder.set_option('-name', '*.txt')
    with pytest.raises(AtomicCmdBuilderError):
        AtomicCmdBuilder.add_option(builder, '-name', '*.bat')


def test_builder__add_or_set_option__set_and_add():
    builder = AtomicCmdBuilder('find')
    builder.add_option('-name', '*.txt')
    with pytest.raises(AtomicCmdBuilderError):
        AtomicCmdBuilder.set_option(builder, '-name', '*.bat')


@pytest.mark.parametrize('setter', _ADD_SET_OPTION)
def test_builder__add_or_set_option__with_non_str_key(setter):
    builder = AtomicCmdBuilder('find')
    with pytest.raises(TypeError):
        setter(builder, 7913, 'True')


@pytest.mark.parametrize('setter', _ADD_SET_OPTION)
def test_builder__add_or_set_option__after_finalize(setter):
    builder = AtomicCmdBuilder('find')
    builder.finalize()
    with pytest.raises(AtomicCmdBuilderError):
        setter(builder, '-size', '1')


@pytest.mark.parametrize('setter', _ADD_SET_OPTION)
def test_builder__add_or_set_option__empty_key(setter):
    builder = AtomicCmdBuilder('find')
    with pytest.raises(KeyError):
        setter(builder, '', '1')


@pytest.mark.parametrize('setter', _ADD_SET_OPTION)
def test_builder__pop_option(setter):
    builder = AtomicCmdBuilder('find')
    setter(builder, '-size', '0', fixed=False)
    builder.pop_option('-size')
    @py_assert1 = builder.call
    @py_assert4 = [
     'find']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=198)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__pop_option__last_option():
    builder = AtomicCmdBuilder('find')
    builder.add_option('-size', '0', fixed=False)
    builder.add_option('-size', '1', fixed=False)
    builder.pop_option('-size')
    @py_assert1 = builder.call
    @py_assert4 = [
     'find', '-size', '0']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=206)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.parametrize('setter', _ADD_SET_OPTION)
def test_builder__pop_option__different_options(setter):
    builder = AtomicCmdBuilder('find')
    setter(builder, '-empty', fixed=False)
    setter(builder, '-size', '1', fixed=False)
    setter(builder, '-name', '*.txt', fixed=False)
    builder.pop_option('-size')
    @py_assert1 = builder.call
    @py_assert4 = [
     'find', '-empty', '-name', '*.txt']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=216)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.parametrize('setter', _ADD_SET_OPTION)
def test_builder__pop_option__is_fixed(setter):
    builder = AtomicCmdBuilder('find')
    setter(builder, '-size', '0')
    with pytest.raises(AtomicCmdBuilderError):
        builder.pop_option('-size')


def test_builder__pop_option__empty():
    builder = AtomicCmdBuilder('find')
    with pytest.raises(KeyError):
        builder.pop_option('-size')


def test_builder__pop_option__missing_key():
    builder = AtomicCmdBuilder('find')
    builder.set_option('-size', 0)
    with pytest.raises(KeyError):
        builder.pop_option('-isize')


def test_builder__pop_option__with_non_str_key():
    builder = AtomicCmdBuilder('find')
    with pytest.raises(TypeError):
        builder.pop_option(7913)


def test_builder__pop_option__with_empty_key():
    builder = AtomicCmdBuilder('find')
    with pytest.raises(KeyError):
        builder.pop_option('')


def test_builder__add_value():
    builder = AtomicCmdBuilder('ls')
    builder.add_value('%(IN_FILE)s')
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls', '%(IN_FILE)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=260)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_value__two_values():
    builder = AtomicCmdBuilder('ls')
    builder.add_value('%(IN_FILE)s')
    builder.add_value('%(OUT_FILE)s')
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls', '%(IN_FILE)s', '%(OUT_FILE)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=267)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__set_kwargs__called_once():
    expected = {'IN_PATH':'/a/b/', 
     'OUT_PATH':'/dst/file'}
    builder = AtomicCmdBuilder('echo')
    (builder.set_kwargs)(**expected)
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=279)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_builder__set_kwargs__called_twice():
    expected = {'IN_PATH':'/a/b/', 
     'OUT_PATH':'/dst/file'}
    builder = AtomicCmdBuilder('echo')
    builder.set_kwargs(OUT_PATH='/dst/file')
    builder.set_kwargs(IN_PATH='/a/b/')
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=287)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_builder__set_kwargs__atomiccmdbuilder():
    mock = Mock(AtomicCmdBuilder('true'))
    mock.finalize.return_value = 'finalized!'
    builder = AtomicCmdBuilder('ls', IN_BUILDER=mock)
    @py_assert1 = builder.kwargs
    @py_assert4 = {'IN_BUILDER': 'finalized!'}
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=294)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__set_kwargs__after_finalize():
    expected = {'IN_PATH': '/a/b/'}
    builder = AtomicCmdBuilder('echo')
    builder.set_kwargs(IN_PATH='/a/b/')
    builder.finalize()
    with pytest.raises(AtomicCmdBuilderError):
        builder.set_kwargs(OUT_PATH='/dst/file')
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=304)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_builder__set__kwargs__overwriting():
    expected = {'IN_PATH': '/a/b/'}
    builder = AtomicCmdBuilder('echo')
    builder.set_kwargs(IN_PATH='/a/b/')
    with pytest.raises(AtomicCmdBuilderError):
        builder.set_kwargs(IN_PATH='/dst/file')
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=313)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_builder__finalized_call__simple_command():
    builder = AtomicCmdBuilder('echo')
    @py_assert1 = builder.finalized_call
    @py_assert4 = [
     'echo']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=323)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.finalized_call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__finalized_call__kwargs_are_instantiated():
    builder = AtomicCmdBuilder(('echo', '%(ARG1)s', 'X=%(ARG2)s'),
      ARG1='/foo/bar', ARG2='zod')
    @py_assert1 = builder.finalized_call
    @py_assert4 = [
     'echo', '/foo/bar', 'X=zod']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=330)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.finalized_call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__finalized_call__kwargs_are_instantiated__with_temp_dir():
    builder = AtomicCmdBuilder(('echo', '%(ARG)s', '%(TEMP_DIR)s'), ARG='/foo/bar')
    @py_assert1 = builder.finalized_call
    @py_assert4 = [
     'echo', '/foo/bar', '%(TEMP_DIR)']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=335)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.finalized_call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__finalized_call__kwargs_are_instantiated__with_non_str_arg():
    builder = AtomicCmdBuilder(('echo', '%(ARG)s', 17), ARG='/foo/bar')
    @py_assert1 = builder.finalized_call
    @py_assert4 = [
     'echo', '/foo/bar', '17']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=340)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.finalized_call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__finalize__returns_singleton():
    builder = AtomicCmdBuilder('echo')
    @py_assert1 = builder.finalize
    @py_assert3 = @py_assert1()
    @py_assert7 = builder.finalize
    @py_assert9 = @py_assert7()
    @py_assert5 = @py_assert3 is @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=350)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.finalize\n}()\n} is %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.finalize\n}()\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_builder__finalize__calls_atomiccmd():
    builder = AtomicCmdBuilder('echo', set_cwd=True)
    builder.add_option('-out', '%(OUT_FILE)s')
    builder.add_value('%(IN_FILE)s')
    builder.set_kwargs(OUT_FILE='/out/file', IN_FILE='/in/file')
    with patch('paleomix.atomiccmd.builder.AtomicCmd') as (mock):
        builder.finalize()
    @py_assert1 = mock.mock_calls
    @py_assert4 = [
     call(['echo', '-out', '%(OUT_FILE)s', '%(IN_FILE)s'], IN_FILE='/in/file', OUT_FILE='/out/file', set_cwd=True)]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=361)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_multiple_options():
    values = ('file_a', 'file_b')
    expected = {'IN_FILE_01':'file_a',  'IN_FILE_02':'file_b'}
    builder = AtomicCmdBuilder('ls')
    kwargs = builder.add_multiple_options('-i', values)
    @py_assert1 = kwargs == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=383)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (kwargs, expected)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=384)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls', '-i', '%(IN_FILE_01)s', '-i', '%(IN_FILE_02)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=385)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_multiple_options_with_sep():
    values = ('file_a', 'file_b')
    expected = {'IN_FILE_01':'file_a',  'IN_FILE_02':'file_b'}
    builder = AtomicCmdBuilder('ls')
    kwargs = builder.add_multiple_options('-i', values, sep='=')
    @py_assert1 = kwargs == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=395)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (kwargs, expected)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=396)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls', '-i=%(IN_FILE_01)s', '-i=%(IN_FILE_02)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=397)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_multiple_options_with_template():
    values = ('file_a', 'file_b')
    expected = {'OUT_BAM_1':'file_a',  'OUT_BAM_2':'file_b'}
    builder = AtomicCmdBuilder('ls')
    kwargs = builder.add_multiple_options('-i', values, template='OUT_BAM_%i')
    @py_assert1 = kwargs == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=407)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (kwargs, expected)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=408)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls', '-i', '%(OUT_BAM_1)s', '-i', '%(OUT_BAM_2)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=409)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_multiple_options_multiple_times():
    expected = {'IN_FILE_01':'file_a', 
     'IN_FILE_02':'file_b'}
    builder = AtomicCmdBuilder('ls')
    kwargs = builder.add_multiple_options('-i', ('file_a', ))
    @py_assert2 = {'IN_FILE_01': 'file_a'}
    @py_assert1 = kwargs == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=417)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (kwargs, @py_assert2)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    kwargs = builder.add_multiple_options('-i', ('file_b', ))
    @py_assert2 = {'IN_FILE_02': 'file_b'}
    @py_assert1 = kwargs == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=419)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (kwargs, @py_assert2)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=421)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls', '-i', '%(IN_FILE_01)s', '-i', '%(IN_FILE_02)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=422)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_multiple_values():
    values = ('file_a', 'file_b')
    expected = {'IN_FILE_01':'file_a',  'IN_FILE_02':'file_b'}
    builder = AtomicCmdBuilder('ls')
    kwargs = builder.add_multiple_values(values)
    @py_assert1 = kwargs == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=437)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (kwargs, expected)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=438)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls', '%(IN_FILE_01)s', '%(IN_FILE_02)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=439)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_multiple_values_with_template():
    values = ('file_a', 'file_b')
    expected = {'OUT_BAM_1':'file_a',  'OUT_BAM_2':'file_b'}
    builder = AtomicCmdBuilder('ls')
    kwargs = builder.add_multiple_values(values, template='OUT_BAM_%i')
    @py_assert1 = kwargs == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=449)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (kwargs, expected)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=450)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls', '%(OUT_BAM_1)s', '%(OUT_BAM_2)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=451)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_multiple_values_multiple_times():
    expected = {'IN_FILE_01':'file_a', 
     'IN_FILE_02':'file_b'}
    builder = AtomicCmdBuilder('ls')
    kwargs = builder.add_multiple_values(('file_a', ))
    @py_assert2 = {'IN_FILE_01': 'file_a'}
    @py_assert1 = kwargs == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=459)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (kwargs, @py_assert2)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    kwargs = builder.add_multiple_values(('file_b', ))
    @py_assert2 = {'IN_FILE_02': 'file_b'}
    @py_assert1 = kwargs == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=461)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (kwargs, @py_assert2)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=463)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls', '%(IN_FILE_01)s', '%(IN_FILE_02)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=464)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_multiple_kwargs():
    values = ('file_a', 'file_b')
    expected = {'IN_FILE_01':'file_a',  'IN_FILE_02':'file_b'}
    builder = AtomicCmdBuilder('ls')
    kwargs = builder.add_multiple_kwargs(values)
    @py_assert1 = kwargs == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=479)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (kwargs, expected)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=480)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=481)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_multiple_kwargs_with_template():
    values = ('file_a', 'file_b')
    expected = {'OUT_BAM_1':'file_a',  'OUT_BAM_2':'file_b'}
    builder = AtomicCmdBuilder('ls')
    kwargs = builder.add_multiple_kwargs(values, template='OUT_BAM_%i')
    @py_assert1 = kwargs == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=491)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (kwargs, expected)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=492)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=493)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_builder__add_multiple_kwargs_multiple_times():
    expected = {'IN_FILE_01':'file_a', 
     'IN_FILE_02':'file_b'}
    builder = AtomicCmdBuilder('ls')
    kwargs = builder.add_multiple_kwargs(('file_a', ))
    @py_assert2 = {'IN_FILE_01': 'file_a'}
    @py_assert1 = kwargs == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=501)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (kwargs, @py_assert2)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    kwargs = builder.add_multiple_kwargs(('file_b', ))
    @py_assert2 = {'IN_FILE_02': 'file_b'}
    @py_assert1 = kwargs == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=503)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (kwargs, @py_assert2)) % {'py0':@pytest_ar._saferepr(kwargs) if 'kwargs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kwargs) else 'kwargs',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = builder.kwargs
    @py_assert3 = @py_assert1 == expected
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=505)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=506)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_java_builder__default__no_config():
    builder = AtomicJavaCmdBuilder('/path/Foo.jar')
    @py_assert1 = builder.call
    @py_assert4 = [
     'java', '-server', '-Djava.io.tmpdir=%(TEMP_DIR)s', '-Djava.awt.headless=true', '-XX:+UseSerialGC', '-Xmx4g', '-jar', '%(AUX_JAR)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=516)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_java_builder__defaults__call():
    builder = AtomicJavaCmdBuilder('/path/Foo.jar', temp_root='/disk/tmp')
    @py_assert1 = builder.call
    @py_assert4 = [
     'java', '-server', '-Djava.io.tmpdir=/disk/tmp', '-Djava.awt.headless=true', '-XX:+UseSerialGC', '-Xmx4g', '-jar', '%(AUX_JAR)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=530)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_java_builder__defaults__kwargs():
    builder = AtomicJavaCmdBuilder('/path/Foo.jar')
    @py_assert1 = builder.kwargs
    @py_assert4 = {'AUX_JAR': '/path/Foo.jar'}
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=544)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_java_builder__multithreaded_gc():
    builder = AtomicJavaCmdBuilder('/path/Foo.jar', temp_root='/disk/tmp', gc_threads=3)
    @py_assert1 = builder.call
    @py_assert4 = [
     'java', '-server', '-Djava.io.tmpdir=/disk/tmp', '-Djava.awt.headless=true', '-XX:ParallelGCThreads=3', '-Xmx4g', '-jar', '%(AUX_JAR)s']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=549)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_java_builder__multithreaded_gc__zero_or_negative_threads():
    with pytest.raises(ValueError):
        AtomicJavaCmdBuilder('/path/Foo.jar', gc_threads=0)
    with pytest.raises(ValueError):
        AtomicJavaCmdBuilder('/path/Foo.jar', gc_threads=(-1))


def test_java_builder__multithreaded_gc__non_int_threads():
    with pytest.raises(TypeError):
        AtomicJavaCmdBuilder('/path/Foo.jar', gc_threads='3')


def test_java_builder__kwargs():
    builder = AtomicJavaCmdBuilder('/path/Foo.jar', set_cwd=True)
    @py_assert1 = builder.kwargs
    @py_assert4 = {'AUX_JAR':'/path/Foo.jar', 
     'set_cwd':True}
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=575)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_mpi_builder__defaults__str():
    builder = AtomicMPICmdBuilder('ls')
    @py_assert1 = builder.call
    @py_assert4 = [
     'ls']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=585)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = builder.kwargs
    @py_assert4 = {'EXEC_MPI': 'mpirun'}
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=586)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_mpi_builder__multithreaded__str():
    builder = AtomicMPICmdBuilder('ls', threads=3)
    @py_assert1 = builder.call
    @py_assert4 = [
     'mpirun', '-n', 3, 'ls']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=591)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = builder.kwargs
    @py_assert4 = {'EXEC_MAIN': 'ls'}
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=592)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_mpi_builder__defaults__complex_cmd():
    builder = AtomicMPICmdBuilder(['python', '/foo/run.py'])
    @py_assert1 = builder.call
    @py_assert4 = [
     'python', '/foo/run.py']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=597)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = builder.kwargs
    @py_assert4 = {'EXEC_MPI': 'mpirun'}
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=598)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_mpi_builder__multithreaded__complex_cmd():
    builder = AtomicMPICmdBuilder(['python', '/foo/run.py'], threads=3)
    @py_assert1 = builder.call
    @py_assert4 = [
     'mpirun', '-n', 3, 'python', '/foo/run.py']
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=603)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = builder.kwargs
    @py_assert4 = {'EXEC_MAIN': 'python'}
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=604)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_mpi_builder__kwargs():
    builder = AtomicMPICmdBuilder('ls', set_cwd=True)
    @py_assert1 = builder.kwargs
    @py_assert4 = {'set_cwd':True, 
     'EXEC_MPI':'mpirun'}
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=609)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.kwargs\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(builder) if 'builder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(builder) else 'builder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_mpi_builder__threads__zero_or_negative():
    with pytest.raises(ValueError):
        AtomicMPICmdBuilder('ls', threads=0)
    with pytest.raises(ValueError):
        AtomicMPICmdBuilder('ls', threads=(-1))


def test_mpi_builder__threads__non_int():
    with pytest.raises(TypeError):
        AtomicMPICmdBuilder('ls', threads='3')


def test_custom_cli__single_named_arg():

    class SingleNamedArg:

        @create_customizable_cli_parameters
        def customize(cls, argument):
            return {}

    value = 'A value'
    obj = SingleNamedArg.customize(value)
    @py_assert1 = obj.argument
    @py_assert3 = @py_assert1 == value
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=637)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.argument\n} == %(py4)s', ), (@py_assert1, value)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_custom_cli__adding_new_values():

    class SingleNamedArg:

        @create_customizable_cli_parameters
        def customize(cls):
            return {'dynamic': 12345}

    obj = SingleNamedArg.customize()
    @py_assert1 = obj.dynamic
    @py_assert4 = 12345
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=647)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dynamic\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_custom_cli__multiple_named_args():

    class SingleNamedArg:

        @create_customizable_cli_parameters
        def customize(cls, first, second):
            return {}

    obj = SingleNamedArg.customize(123, 456)
    @py_assert1 = obj.first
    @py_assert4 = 123
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=657)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.first\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = obj.second
    @py_assert4 = 456
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=658)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.second\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_custom_cli__only_customize_is_valid_function_name():
    try:

        class ClassWithMisnamedFunction:

            @create_customizable_cli_parameters
            def not_called_customize(cls, first, second):
                return {}

        @py_assert0 = False
        if @py_assert0 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=669)
        if not @py_assert0:
            @py_format2 = (@pytest_ar._format_assertmsg('ValueError not raised') + '\n>assert %(py1)s') % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None
    except ValueError:
        pass


def test_apply_options__single_option__default_pred__set_when_pred_is_true():
    mock = Mock(AtomicCmdBuilder('ls'))
    apply_options(mock, {'--foo': 17})
    mock.set_option.assert_called_once_with('--foo', 17)


def test_apply_options__single_option__default_pred__ignore_false_pred():
    mock = Mock(AtomicCmdBuilder('ls'))
    apply_options(mock, {'Other': None})


def _user_pred(key):
    return key.startswith('FOO')


def test_apply_options__single_option__user_pred__set_when_pred_is_true():
    mock = Mock(AtomicCmdBuilder('ls'))
    apply_options(mock, {'FOO_BAR': 17}, _user_pred)
    mock.set_option.assert_called_once_with('FOO_BAR', 17)


def test_apply_options__single_option__user_pred__ignore_when_pred_is_false():
    mock = Mock(AtomicCmdBuilder('ls'))
    apply_options(mock, {'BAR_FOO': 17}, _user_pred)


def test_apply_options__single_option__boolean__set_when_value_is_true():
    mock = Mock(AtomicCmdBuilder('ls'))
    apply_options(mock, {'-v': True})
    mock.set_option.assert_called_once_with('-v')


def test_apply_options__single_option__boolean__set_when_value_is_none():
    mock = Mock(AtomicCmdBuilder('ls'))
    apply_options(mock, {'-v': None})
    mock.set_option.assert_called_once_with('-v')


def test_apply_options__single_option__boolean__pop_when_value_is_false():
    mock = Mock(AtomicCmdBuilder('ls'))
    apply_options(mock, {'-v': False})
    mock.pop_option.assert_called_once_with('-v')


def test_apply_options__single_option__boolean__pop_missing_throws():
    mock = Mock(AtomicCmdBuilder('ls'))
    mock.pop_option.side_effect = KeyError('-v')
    with pytest.raises(KeyError):
        apply_options(mock, {'-v': False})
    mock.pop_option.assert_called_once_with('-v')


def test_apply_options__multiple_option():
    mock = Mock(AtomicCmdBuilder('ls'))
    apply_options(mock, {'--foo': [3, 17]})
    @py_assert1 = mock.mock_calls
    @py_assert4 = [
     call.add_option('--foo', 3), call.add_option('--foo', 17)]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/builder_test.py', lineno=739)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_apply_options__boolean_and_none_is_single_value_only():
    mock = Mock(AtomicCmdBuilder('ls'))
    with pytest.raises(TypeError):
        apply_options(mock, {'--foo': [True]})
    with pytest.raises(TypeError):
        apply_options(mock, {'--foo': [False]})
    with pytest.raises(TypeError):
        apply_options(mock, {'--foo': [None]})


def test_apply_options__unexpected_types_in_values():
    mock = Mock(AtomicCmdBuilder('ls'))
    with pytest.raises(TypeError):
        apply_options(mock, {'--foo': object()})
    with pytest.raises(TypeError):
        apply_options(mock, {'--foo': iter([])})
    with pytest.raises(TypeError):
        apply_options(mock, {'--foo': {}})
    with pytest.raises(TypeError):
        apply_options(mock, {'--foo': set()})


def test_apply_options__non_string_types_in_keys():
    mock = Mock(AtomicCmdBuilder('ls'))
    with pytest.raises(TypeError):
        apply_options(mock, {1: 17})
    with pytest.raises(TypeError):
        apply_options(mock, {('foo', ): 17})


def test_apply_options__not_dict_like():
    mock = Mock(AtomicCmdBuilder('ls'))
    with pytest.raises(TypeError):
        apply_options(mock, None)
    with pytest.raises(TypeError):
        apply_options(mock, [1, 2, 3])