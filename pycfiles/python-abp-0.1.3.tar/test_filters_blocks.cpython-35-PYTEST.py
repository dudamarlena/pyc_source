# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vkuznetsov/prog/devops/python-abp/tests/test_filters_blocks.py
# Compiled at: 2019-06-13 06:59:11
# Size of source mod 2**32: 1986 bytes
"""Tests for abp.filters.blocks."""
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, json, os, pytest
from abp.filters import parse_filterlist, SelectorType, FilterAction
from abp.filters.blocks import to_blocks
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')

@pytest.fixture()
def fl_lines():
    with open(os.path.join(DATA_PATH, 'filterlist.txt')) as (f):
        return list(parse_filterlist(f))


@pytest.fixture()
def expected_blocks():
    with open(os.path.join(DATA_PATH, 'expected_blocks.json')) as (f):
        return json.load(f)


def test_to_blocks(fl_lines):
    blocks = list(to_blocks(fl_lines))
    @py_assert2 = len(blocks)
    @py_assert5 = 3
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_filters_blocks.py', lineno=45)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(blocks) if 'blocks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blocks) else 'blocks'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    block = blocks[0]
    @py_assert0 = block.variables['foo']
    @py_assert3 = 'bar'
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_filters_blocks.py', lineno=47)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = block.variables['baz']
    @py_assert3 = 'some_tricky?variable=with&funny=chars#and-stuff'
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_filters_blocks.py', lineno=48)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = block.description
    @py_assert4 = 'Example block 1\nAnother comment'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_filters_blocks.py', lineno=50)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.description\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(block) if 'block' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(block) else 'block'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = block.filters
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 2
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_filters_blocks.py', lineno=52)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.filters\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(block) if 'block' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(block) else 'block'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = block.filters[0].selector['type']
    @py_assert4 = SelectorType.URL_PATTERN
    @py_assert2 = @py_assert0 == @py_assert4
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_filters_blocks.py', lineno=53)
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.URL_PATTERN\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(SelectorType) if 'SelectorType' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SelectorType) else 'SelectorType', 'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = block.filters[1]
    @py_assert2 = @py_assert0.action
    @py_assert6 = FilterAction.SHOW
    @py_assert4 = @py_assert2 == @py_assert6
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_filters_blocks.py', lineno=54)
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.action\n} == %(py7)s\n{%(py7)s = %(py5)s.SHOW\n}', ), (@py_assert2, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(FilterAction) if 'FilterAction' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FilterAction) else 'FilterAction', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_to_dict(fl_lines, expected_blocks):
    blocks = [b.to_dict() for b in to_blocks(fl_lines)]
    @py_assert1 = blocks == expected_blocks
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_filters_blocks.py', lineno=59)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (blocks, expected_blocks)) % {'py2': @pytest_ar._saferepr(expected_blocks) if 'expected_blocks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_blocks) else 'expected_blocks', 'py0': @pytest_ar._saferepr(blocks) if 'blocks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blocks) else 'blocks'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None