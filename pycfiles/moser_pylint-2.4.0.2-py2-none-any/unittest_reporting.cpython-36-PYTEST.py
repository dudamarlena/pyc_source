# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_reporting.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 2509 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, warnings
from io import StringIO
import pytest
from pylint import checkers
from pylint.lint import PyLinter
from pylint.reporters.text import ParseableTextReporter, TextReporter

@pytest.fixture(scope='module')
def reporter(reporter):
    return TextReporter


@pytest.fixture(scope='module')
def disable(disable):
    return ['I']


def test_template_option(linter):
    output = StringIO()
    linter.reporter.set_output(output)
    linter.set_option('msg-template', '{msg_id}:{line:03d}')
    linter.open()
    linter.set_current_module('0123')
    linter.add_message('C0301', line=1, args=(1, 2))
    linter.add_message('line-too-long', line=2, args=(3, 4))
    @py_assert1 = output.getvalue
    @py_assert3 = @py_assert1()
    @py_assert6 = '************* Module 0123\nC0301:001\nC0301:002\n'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_reporting.py', lineno=41)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_parseable_output_deprecated():
    with warnings.catch_warnings(record=True) as (cm):
        warnings.simplefilter('always')
        ParseableTextReporter()
    @py_assert2 = len(cm)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_reporting.py', lineno=51)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(cm) if 'cm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cm) else 'cm',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = cm[0]
    @py_assert3 = @py_assert1.message
    @py_assert6 = isinstance(@py_assert3, DeprecationWarning)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_reporting.py', lineno=52)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py4)s\n{%(py4)s = %(py2)s.message\n}, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(DeprecationWarning) if 'DeprecationWarning' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DeprecationWarning) else 'DeprecationWarning',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_parseable_output_regression():
    output = StringIO()
    with warnings.catch_warnings(record=True):
        linter = PyLinter(reporter=(ParseableTextReporter()))
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.reporter.set_output(output)
    linter.set_option('output-format', 'parseable')
    linter.open()
    linter.set_current_module('0123')
    linter.add_message('line-too-long', line=1, args=(1, 2))
    @py_assert1 = output.getvalue
    @py_assert3 = @py_assert1()
    @py_assert6 = '************* Module 0123\n0123:1: [C0301(line-too-long), ] Line too long (1/2)\n'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_reporting.py', lineno=67)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_display_results_is_renamed():

    class CustomReporter(TextReporter):

        def _display(self, layout):
            pass

    reporter = CustomReporter()
    with pytest.raises(AttributeError):
        reporter.display_results