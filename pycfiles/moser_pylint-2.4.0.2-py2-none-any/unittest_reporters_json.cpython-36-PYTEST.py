# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_reporters_json.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 1692 bytes
"""Test for the JSON reporter."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, json
from io import StringIO
from pylint import checkers
from pylint.lint import PyLinter
from pylint.reporters import JSONReporter

def test_simple_json_output():
    output = StringIO()
    reporter = JSONReporter()
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.reporter.set_output(output)
    linter.open()
    linter.set_current_module('0123')
    linter.add_message('line-too-long', line=1, args=(1, 2))
    reporter.display_messages(None)
    expected_result = [
     [
      ('column', 0),
      ('line', 1),
      ('message', 'Line too long (1/2)'),
      ('message-id', 'C0301'),
      ('module', '0123'),
      ('obj', ''),
      ('path', '0123'),
      ('symbol', 'line-too-long'),
      ('type', 'convention')]]
    report_result = json.loads(output.getvalue())
    report_result = [sorted((report_result[0].items()), key=(lambda item: item[0]))]
    @py_assert1 = report_result == expected_result
    if @py_assert1 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_reporters_json.py', lineno=52)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (report_result, expected_result)) % {'py0':@pytest_ar._saferepr(report_result) if 'report_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(report_result) else 'report_result',  'py2':@pytest_ar._saferepr(expected_result) if 'expected_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_result) else 'expected_result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None