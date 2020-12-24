# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/extensions/test_check_docs_utils.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 2838 bytes
"""Unit tests for the pylint checkers in :mod:`pylint.extensions.check_docs`,
in particular the parameter documentation checker `DocstringChecker`
"""
from __future__ import absolute_import, division, print_function
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, astroid, pytest, pylint.extensions._check_docs_utils as utils

@pytest.mark.parametrize('string,count', [
 ('abc', 0),
 ('', 0),
 ('  abc', 2),
 ('\n  abc', 0),
 ('   \n  abc', 3)])
def test_space_indentation(string, count):
    """Test for pylint_plugin.ParamDocChecker"""
    @py_assert1 = utils.space_indentation
    @py_assert4 = @py_assert1(string)
    @py_assert6 = @py_assert4 == count
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_check_docs_utils.py', lineno=29)
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.space_indentation\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, count)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None


@pytest.mark.parametrize('raise_node,expected', [
 (
  astroid.extract_node('\n    def my_func():\n        raise NotImplementedError #@\n    '), {'NotImplementedError'}),
 (
  astroid.extract_node('\n    def my_func():\n        raise NotImplementedError("Not implemented!") #@\n    '), {'NotImplementedError'}),
 (
  astroid.extract_node('\n    def my_func():\n        try:\n            fake_func()\n        except RuntimeError:\n            raise #@\n    '), {'RuntimeError'}),
 (
  astroid.extract_node('\n    def my_func():\n        try:\n            fake_func()\n        except RuntimeError:\n            if another_func():\n                raise #@\n    '), {'RuntimeError'}),
 (
  astroid.extract_node('\n    def my_func():\n        try:\n            fake_func()\n        except RuntimeError:\n            try:\n                another_func()\n                raise #@\n            except NameError:\n                pass\n    '), {'RuntimeError'}),
 (
  astroid.extract_node('\n    def my_func():\n        try:\n            fake_func()\n        except RuntimeError:\n            try:\n                another_func()\n            except NameError:\n                raise #@\n    '), {'NameError'}),
 (
  astroid.extract_node('\n    def my_func():\n        try:\n            fake_func()\n        except:\n            raise #@\n    '), set()),
 (
  astroid.extract_node('\n    def my_func():\n        try:\n            fake_func()\n        except (RuntimeError, ValueError):\n            raise #@\n    '), {'RuntimeError', 'ValueError'}),
 (
  astroid.extract_node('\n    import not_a_module\n    def my_func():\n        try:\n            fake_func()\n        except not_a_module.Error:\n            raise #@\n    '), set())])
def test_exception(raise_node, expected):
    found = utils.possible_exc_types(raise_node)
    @py_assert1 = found == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_check_docs_utils.py', lineno=111)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (found, expected)) % {'py0':@pytest_ar._saferepr(found) if 'found' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(found) else 'found',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None