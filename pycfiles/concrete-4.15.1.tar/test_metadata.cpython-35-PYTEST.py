# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_metadata.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 21901 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from datetime import datetime
import random, string
from pytest import raises
from mock import Mock, sentinel, patch
from concrete.util import get_index_of_tool, datetime_to_timestamp, now_timestamp, timestamp_to_datetime, get_annotation_field, filter_annotations, ZeroAnnotationsError, MultipleAnnotationsError, filter_annotations_json, tool_to_filter
from concrete import AnnotationMetadata

class HasMetadata(object):

    def __init__(self, tool=None):
        self.metadata = AnnotationMetadata(tool=HasMetadata.gen_tool(tool), timestamp=0)

    @classmethod
    def gen_tool(cls, tool=None, size=6, chars=string.ascii_uppercase + string.digits):
        if tool is not None:
            return tool
        return ''.join(random.choice(chars) for _ in range(size))


def test_get_index_of_tool_none_list():
    @py_assert1 = None
    @py_assert3 = None
    @py_assert5 = get_index_of_tool(@py_assert1, @py_assert3)
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert7 = @py_assert5 == @py_assert10
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == -%(py9)s', ), (@py_assert5, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = None
    @py_assert1 = None
    @py_assert3 = ''
    @py_assert5 = get_index_of_tool(@py_assert1, @py_assert3)
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert7 = @py_assert5 == @py_assert10
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == -%(py9)s', ), (@py_assert5, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = None
    @py_assert1 = None
    @py_assert3 = 'My awesome tool'
    @py_assert5 = get_index_of_tool(@py_assert1, @py_assert3)
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert7 = @py_assert5 == @py_assert10
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == -%(py9)s', ), (@py_assert5, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = None


def test_get_index_of_tool_empty_list():
    @py_assert1 = []
    @py_assert3 = None
    @py_assert5 = get_index_of_tool(@py_assert1, @py_assert3)
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert7 = @py_assert5 == @py_assert10
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == -%(py9)s', ), (@py_assert5, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = None
    @py_assert1 = []
    @py_assert3 = ''
    @py_assert5 = get_index_of_tool(@py_assert1, @py_assert3)
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert7 = @py_assert5 == @py_assert10
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == -%(py9)s', ), (@py_assert5, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = None
    @py_assert1 = []
    @py_assert3 = 'My awesome tool'
    @py_assert5 = get_index_of_tool(@py_assert1, @py_assert3)
    @py_assert8 = 1
    @py_assert10 = -@py_assert8
    @py_assert7 = @py_assert5 == @py_assert10
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == -%(py9)s', ), (@py_assert5, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = None


def test_get_index_of_tool_nonempty_list_contains():
    lst = [
     HasMetadata('My awesome tool'),
     HasMetadata('My awesome tool--new'),
     HasMetadata()]
    @py_assert2 = None
    @py_assert4 = get_index_of_tool(lst, @py_assert2)
    @py_assert7 = 0
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(lst) if 'lst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lst) else 'lst', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = ''
    @py_assert4 = get_index_of_tool(lst, @py_assert2)
    @py_assert7 = 1
    @py_assert9 = -@py_assert7
    @py_assert6 = @py_assert4 == @py_assert9
    if not @py_assert6:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == -%(py8)s', ), (@py_assert4, @py_assert9)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(lst) if 'lst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lst) else 'lst', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = None
    @py_assert2 = 'My awesome tool'
    @py_assert4 = get_index_of_tool(lst, @py_assert2)
    @py_assert7 = 0
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(lst) if 'lst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lst) else 'lst', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    lst[2] = lst[0]
    lst[0] = HasMetadata()
    @py_assert2 = None
    @py_assert4 = get_index_of_tool(lst, @py_assert2)
    @py_assert7 = 0
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(lst) if 'lst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lst) else 'lst', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = ''
    @py_assert4 = get_index_of_tool(lst, @py_assert2)
    @py_assert7 = 1
    @py_assert9 = -@py_assert7
    @py_assert6 = @py_assert4 == @py_assert9
    if not @py_assert6:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == -%(py8)s', ), (@py_assert4, @py_assert9)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(lst) if 'lst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lst) else 'lst', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = None
    @py_assert2 = 'My awesome tool'
    @py_assert4 = get_index_of_tool(lst, @py_assert2)
    @py_assert7 = 2
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(lst) if 'lst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lst) else 'lst', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_get_index_of_tool_nonempty_list_no_contains():
    lst = [
     HasMetadata(),
     HasMetadata(),
     HasMetadata()]
    @py_assert2 = None
    @py_assert4 = get_index_of_tool(lst, @py_assert2)
    @py_assert7 = 0
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(lst) if 'lst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lst) else 'lst', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = ''
    @py_assert4 = get_index_of_tool(lst, @py_assert2)
    @py_assert7 = 1
    @py_assert9 = -@py_assert7
    @py_assert6 = @py_assert4 == @py_assert9
    if not @py_assert6:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == -%(py8)s', ), (@py_assert4, @py_assert9)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(lst) if 'lst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lst) else 'lst', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = None
    @py_assert2 = 'My awesome tool'
    @py_assert4 = get_index_of_tool(lst, @py_assert2)
    @py_assert7 = 1
    @py_assert9 = -@py_assert7
    @py_assert6 = @py_assert4 == @py_assert9
    if not @py_assert6:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == -%(py8)s', ), (@py_assert4, @py_assert9)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(lst) if 'lst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lst) else 'lst', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_index_of_tool) if 'get_index_of_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_index_of_tool) else 'get_index_of_tool', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = None


def test_datetime_to_timestamp():
    @py_assert2 = 1970
    @py_assert4 = 1
    @py_assert6 = 1
    @py_assert8 = datetime(@py_assert2, @py_assert4, @py_assert6)
    @py_assert10 = datetime_to_timestamp(@py_assert8)
    @py_assert13 = 0
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(%(py3)s, %(py5)s, %(py7)s)\n})\n} == %(py14)s',), (@py_assert10, @py_assert13)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py14': @pytest_ar._saferepr(@py_assert13), 'py0': @pytest_ar._saferepr(datetime_to_timestamp) if 'datetime_to_timestamp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime_to_timestamp) else 'datetime_to_timestamp', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format17 = ('' + 'assert %(py16)s') % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = 1970
    @py_assert4 = 1
    @py_assert6 = 1
    @py_assert8 = 0
    @py_assert10 = 0
    @py_assert12 = 47
    @py_assert14 = datetime(@py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert16 = datetime_to_timestamp(@py_assert14)
    @py_assert19 = 47
    @py_assert18 = @py_assert16 == @py_assert19
    if not @py_assert18:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert18,), ('%(py17)s\n{%(py17)s = %(py0)s(%(py15)s\n{%(py15)s = %(py1)s(%(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n})\n} == %(py20)s',), (@py_assert16, @py_assert19)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py17': @pytest_ar._saferepr(@py_assert16), 'py13': @pytest_ar._saferepr(@py_assert12), 'py0': @pytest_ar._saferepr(datetime_to_timestamp) if 'datetime_to_timestamp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime_to_timestamp) else 'datetime_to_timestamp', 'py15': @pytest_ar._saferepr(@py_assert14), 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py20': @pytest_ar._saferepr(@py_assert19), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert19 = None


def test_timestamp_to_datetime():
    @py_assert1 = 0
    @py_assert3 = timestamp_to_datetime(@py_assert1)
    @py_assert7 = 1970
    @py_assert9 = 1
    @py_assert11 = 1
    @py_assert13 = datetime(@py_assert7, @py_assert9, @py_assert11)
    @py_assert5 = @py_assert3 == @py_assert13
    if not @py_assert5:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py14)s\n{%(py14)s = %(py6)s(%(py8)s, %(py10)s, %(py12)s)\n}',), (@py_assert3, @py_assert13)) % {'py12': @pytest_ar._saferepr(@py_assert11), 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(timestamp_to_datetime) if 'timestamp_to_datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timestamp_to_datetime) else 'timestamp_to_datetime', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format17 = ('' + 'assert %(py16)s') % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = 47
    @py_assert3 = timestamp_to_datetime(@py_assert1)
    @py_assert7 = 1970
    @py_assert9 = 1
    @py_assert11 = 1
    @py_assert13 = 0
    @py_assert15 = 0
    @py_assert17 = 47
    @py_assert19 = datetime(@py_assert7, @py_assert9, @py_assert11, @py_assert13, @py_assert15, @py_assert17)
    @py_assert5 = @py_assert3 == @py_assert19
    if not @py_assert5:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py20)s\n{%(py20)s = %(py6)s(%(py8)s, %(py10)s, %(py12)s, %(py14)s, %(py16)s, %(py18)s)\n}',), (@py_assert3, @py_assert19)) % {'py12': @pytest_ar._saferepr(@py_assert11), 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(timestamp_to_datetime) if 'timestamp_to_datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timestamp_to_datetime) else 'timestamp_to_datetime', 'py18': @pytest_ar._saferepr(@py_assert17), 'py16': @pytest_ar._saferepr(@py_assert15), 'py4': @pytest_ar._saferepr(@py_assert3), 'py20': @pytest_ar._saferepr(@py_assert19), 'py6': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = None


def test_now_timestamp():
    @py_assert1 = now_timestamp()
    @py_assert6 = 2000
    @py_assert8 = 1
    @py_assert10 = 1
    @py_assert12 = 0
    @py_assert14 = 0
    @py_assert16 = 0
    @py_assert18 = datetime(@py_assert6, @py_assert8, @py_assert10, @py_assert12, @py_assert14, @py_assert16)
    @py_assert20 = datetime_to_timestamp(@py_assert18)
    @py_assert3 = @py_assert1 > @py_assert20
    if not @py_assert3:
        @py_format22 = @pytest_ar._call_reprcompare(('>',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} > %(py21)s\n{%(py21)s = %(py4)s(%(py19)s\n{%(py19)s = %(py5)s(%(py7)s, %(py9)s, %(py11)s, %(py13)s, %(py15)s, %(py17)s)\n})\n}',), (@py_assert1, @py_assert20)) % {'py21': @pytest_ar._saferepr(@py_assert20), 'py2': @pytest_ar._saferepr(@py_assert1), 'py17': @pytest_ar._saferepr(@py_assert16), 'py0': @pytest_ar._saferepr(now_timestamp) if 'now_timestamp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(now_timestamp) else 'now_timestamp', 'py9': @pytest_ar._saferepr(@py_assert8), 'py4': @pytest_ar._saferepr(datetime_to_timestamp) if 'datetime_to_timestamp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime_to_timestamp) else 'datetime_to_timestamp', 'py19': @pytest_ar._saferepr(@py_assert18), 'py15': @pytest_ar._saferepr(@py_assert14), 'py13': @pytest_ar._saferepr(@py_assert12), 'py7': @pytest_ar._saferepr(@py_assert6), 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime'}
        @py_format24 = ('' + 'assert %(py23)s') % {'py23': @py_format22}
        raise AssertionError(@pytest_ar._format_explanation(@py_format24))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = None


def test_get_annotation_field_kBest():
    annotation = Mock(metadata=Mock(kBest=4))
    @py_assert2 = 'kBest'
    @py_assert4 = get_annotation_field(annotation, @py_assert2)
    @py_assert7 = 4
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(annotation) if 'annotation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(annotation) else 'annotation', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_annotation_field) if 'get_annotation_field' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_annotation_field) else 'get_annotation_field', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_get_annotation_field_tool():
    annotation = Mock(metadata=Mock(tool='goldenhorse'))
    @py_assert2 = 'tool'
    @py_assert4 = get_annotation_field(annotation, @py_assert2)
    @py_assert7 = 'goldenhorse'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(annotation) if 'annotation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(annotation) else 'annotation', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_annotation_field) if 'get_annotation_field' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_annotation_field) else 'get_annotation_field', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_get_annotation_field_timestamp():
    annotation = Mock(metadata=Mock(timestamp=4))
    @py_assert2 = 'timestamp'
    @py_assert4 = get_annotation_field(annotation, @py_assert2)
    @py_assert7 = 4
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(annotation) if 'annotation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(annotation) else 'annotation', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(get_annotation_field) if 'get_annotation_field' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_annotation_field) else 'get_annotation_field', 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_get_annotation_field_invalid():
    annotation = Mock(metadata=Mock())
    with raises(ValueError):
        get_annotation_field(annotation, 'foobar')


def test_filter_annotations_noop():
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2]
    @py_assert3 = filter_annotations(@py_assert1)
    @py_assert6 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 4, 
         (
 sentinel.annotation0, 'bar'): 3, 
         (
 sentinel.annotation1, 'bar'): 4, 
         (
 sentinel.annotation2, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = filter_annotations(@py_assert1, filter_fields=@py_assert3)
    @py_assert8 = [
     sentinel.annotation1]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, filter_fields=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_zero(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 4, 
         (
 sentinel.annotation0, 'bar'): 3, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = filter_annotations(@py_assert1, filter_fields=@py_assert3)
    @py_assert8 = []
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, filter_fields=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = filter_annotations(@py_assert1, filter_fields=@py_assert3)
    @py_assert8 = [
     sentinel.annotation0, sentinel.annotation2]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, filter_fields=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_reverse(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation3, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4, 
         (
 sentinel.annotation3, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2, sentinel.annotation3]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = True
    @py_assert7 = filter_annotations(@py_assert1, filter_fields=@py_assert3, sort_reverse=@py_assert5)
    @py_assert10 = [
     sentinel.annotation3, sentinel.annotation2, sentinel.annotation0]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, filter_fields=%(py4)s, sort_reverse=%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_sort(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation3, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4, 
         (
 sentinel.annotation3, 'bar'): 4, 
         (
 sentinel.annotation0, 'baz'): 2, 
         (
 sentinel.annotation1, 'baz'): 0, 
         (
 sentinel.annotation2, 'baz'): 1, 
         (
 sentinel.annotation3, 'baz'): 3}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2, sentinel.annotation3]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = 'baz'
    @py_assert7 = filter_annotations(@py_assert1, filter_fields=@py_assert3, sort_field=@py_assert5)
    @py_assert10 = [
     sentinel.annotation2, sentinel.annotation0, sentinel.annotation3]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, filter_fields=%(py4)s, sort_field=%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_sort_reverse(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation3, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4, 
         (
 sentinel.annotation3, 'bar'): 4, 
         (
 sentinel.annotation0, 'baz'): 2, 
         (
 sentinel.annotation1, 'baz'): 0, 
         (
 sentinel.annotation2, 'baz'): 1, 
         (
 sentinel.annotation3, 'baz'): 3}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2, sentinel.annotation3]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = 'baz'
    @py_assert7 = True
    @py_assert9 = filter_annotations(@py_assert1, filter_fields=@py_assert3, sort_field=@py_assert5, sort_reverse=@py_assert7)
    @py_assert12 = [
     sentinel.annotation3, sentinel.annotation0, sentinel.annotation2]
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py2)s, filter_fields=%(py4)s, sort_field=%(py6)s, sort_reverse=%(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_raise(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    with raises(MultipleAnnotationsError):
        filter_annotations([
         sentinel.annotation0,
         sentinel.annotation1,
         sentinel.annotation2], filter_fields={'foo': 3, 'bar': 4}, action_if_multiple='raise')


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_zero_raise(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 4, 
         (
 sentinel.annotation0, 'bar'): 3, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    with raises(ZeroAnnotationsError):
        filter_annotations([
         sentinel.annotation0,
         sentinel.annotation1,
         sentinel.annotation2], filter_fields={'foo': 3, 'bar': 4}, action_if_zero='raise')


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_zero_raise_with_multiple(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = 'raise'
    @py_assert7 = filter_annotations(@py_assert1, filter_fields=@py_assert3, action_if_zero=@py_assert5)
    @py_assert10 = [
     sentinel.annotation0, sentinel.annotation2]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, filter_fields=%(py4)s, action_if_zero=%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_raise_with_zero(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 4, 
         (
 sentinel.annotation0, 'bar'): 3, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = 'raise'
    @py_assert7 = filter_annotations(@py_assert1, filter_fields=@py_assert3, action_if_multiple=@py_assert5)
    @py_assert10 = []
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, filter_fields=%(py4)s, action_if_multiple=%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_zero_raise_with_one(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 4, 
         (
 sentinel.annotation0, 'bar'): 3, 
         (
 sentinel.annotation1, 'bar'): 4, 
         (
 sentinel.annotation2, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = filter_annotations(@py_assert1, filter_fields=@py_assert3)
    @py_assert8 = [
     sentinel.annotation1]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, filter_fields=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_raise_with_one(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 4, 
         (
 sentinel.annotation0, 'bar'): 3, 
         (
 sentinel.annotation1, 'bar'): 4, 
         (
 sentinel.annotation2, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = filter_annotations(@py_assert1, filter_fields=@py_assert3)
    @py_assert8 = [
     sentinel.annotation1]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, filter_fields=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_first(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = 'first'
    @py_assert7 = filter_annotations(@py_assert1, filter_fields=@py_assert3, action_if_multiple=@py_assert5)
    @py_assert10 = [
     sentinel.annotation0]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, filter_fields=%(py4)s, action_if_multiple=%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_last(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = 'last'
    @py_assert7 = filter_annotations(@py_assert1, filter_fields=@py_assert3, action_if_multiple=@py_assert5)
    @py_assert10 = [
     sentinel.annotation2]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, filter_fields=%(py4)s, action_if_multiple=%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_sort_first(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation3, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4, 
         (
 sentinel.annotation3, 'bar'): 4, 
         (
 sentinel.annotation0, 'baz'): 2, 
         (
 sentinel.annotation1, 'baz'): 0, 
         (
 sentinel.annotation2, 'baz'): 1, 
         (
 sentinel.annotation3, 'baz'): 3}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2, sentinel.annotation3]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = 'baz'
    @py_assert7 = 'first'
    @py_assert9 = filter_annotations(@py_assert1, filter_fields=@py_assert3, sort_field=@py_assert5, action_if_multiple=@py_assert7)
    @py_assert12 = [
     sentinel.annotation2]
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py2)s, filter_fields=%(py4)s, sort_field=%(py6)s, action_if_multiple=%(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_sort_last(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation3, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4, 
         (
 sentinel.annotation3, 'bar'): 4, 
         (
 sentinel.annotation0, 'baz'): 2, 
         (
 sentinel.annotation1, 'baz'): 0, 
         (
 sentinel.annotation2, 'baz'): 1, 
         (
 sentinel.annotation3, 'baz'): 3}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2, sentinel.annotation3]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = 'baz'
    @py_assert7 = 'last'
    @py_assert9 = filter_annotations(@py_assert1, filter_fields=@py_assert3, sort_field=@py_assert5, action_if_multiple=@py_assert7)
    @py_assert12 = [
     sentinel.annotation3]
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py2)s, filter_fields=%(py4)s, sort_field=%(py6)s, action_if_multiple=%(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_sort_reverse_first(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation3, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4, 
         (
 sentinel.annotation3, 'bar'): 4, 
         (
 sentinel.annotation0, 'baz'): 2, 
         (
 sentinel.annotation1, 'baz'): 0, 
         (
 sentinel.annotation2, 'baz'): 1, 
         (
 sentinel.annotation3, 'baz'): 3}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2, sentinel.annotation3]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = 'baz'
    @py_assert7 = True
    @py_assert9 = 'first'
    @py_assert11 = filter_annotations(@py_assert1, filter_fields=@py_assert3, sort_field=@py_assert5, sort_reverse=@py_assert7, action_if_multiple=@py_assert9)
    @py_assert14 = [
     sentinel.annotation3]
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py2)s, filter_fields=%(py4)s, sort_field=%(py6)s, sort_reverse=%(py8)s, action_if_multiple=%(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py12': @pytest_ar._saferepr(@py_assert11), 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py15': @pytest_ar._saferepr(@py_assert14), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


@patch('concrete.util.metadata.get_annotation_field')
def test_filter_annotations_multiple_sort_reverse_last(mock_get_annotation_field):

    def _mock_get_annotation_field(annotation, field):
        return {(
 sentinel.annotation0, 'foo'): 3, 
         (
 sentinel.annotation1, 'foo'): 3, 
         (
 sentinel.annotation2, 'foo'): 3, 
         (
 sentinel.annotation3, 'foo'): 3, 
         (
 sentinel.annotation0, 'bar'): 4, 
         (
 sentinel.annotation1, 'bar'): 3, 
         (
 sentinel.annotation2, 'bar'): 4, 
         (
 sentinel.annotation3, 'bar'): 4, 
         (
 sentinel.annotation0, 'baz'): 2, 
         (
 sentinel.annotation1, 'baz'): 0, 
         (
 sentinel.annotation2, 'baz'): 1, 
         (
 sentinel.annotation3, 'baz'): 3}[(
         annotation, field)]

    mock_get_annotation_field.side_effect = _mock_get_annotation_field
    @py_assert1 = [
     sentinel.annotation0, sentinel.annotation1, sentinel.annotation2, sentinel.annotation3]
    @py_assert3 = {'foo': 3, 'bar': 4}
    @py_assert5 = 'baz'
    @py_assert7 = True
    @py_assert9 = 'last'
    @py_assert11 = filter_annotations(@py_assert1, filter_fields=@py_assert3, sort_field=@py_assert5, sort_reverse=@py_assert7, action_if_multiple=@py_assert9)
    @py_assert14 = [
     sentinel.annotation2]
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py2)s, filter_fields=%(py4)s, sort_field=%(py6)s, sort_reverse=%(py8)s, action_if_multiple=%(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py12': @pytest_ar._saferepr(@py_assert11), 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filter_annotations) if 'filter_annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations) else 'filter_annotations', 'py15': @pytest_ar._saferepr(@py_assert14), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


@patch('concrete.util.metadata.filter_annotations')
def test_filter_annotations_json(mock_filter_annotations):
    mock_filter_annotations.side_effect = [sentinel.return_value]
    @py_assert2 = sentinel.annotations
    @py_assert4 = '{"foo": 47, "baz": ["hello", "world"]}'
    @py_assert6 = filter_annotations_json(@py_assert2, @py_assert4)
    @py_assert10 = sentinel.return_value
    @py_assert8 = @py_assert6 == @py_assert10
    if not @py_assert8:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.annotations\n}, %(py5)s)\n} == %(py11)s\n{%(py11)s = %(py9)s.return_value\n}',), (@py_assert6, @py_assert10)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(filter_annotations_json) if 'filter_annotations_json' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_annotations_json) else 'filter_annotations_json', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel'}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    mock_filter_annotations.assert_called_once_with(sentinel.annotations, foo=47, baz=[
     'hello', 'world'])


def test_tool_to_filter():
    @py_assert1 = None
    @py_assert3 = None
    @py_assert5 = tool_to_filter(@py_assert1, @py_assert3)
    @py_assert8 = None
    @py_assert7 = @py_assert5 is @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} is %(py9)s',), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(tool_to_filter) if 'tool_to_filter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tool_to_filter) else 'tool_to_filter', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = None
    @py_assert4 = sentinel.explicit_filter
    @py_assert6 = tool_to_filter(@py_assert1, @py_assert4)
    @py_assert10 = sentinel.explicit_filter
    @py_assert8 = @py_assert6 == @py_assert10
    if not @py_assert8:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py2)s, %(py5)s\n{%(py5)s = %(py3)s.explicit_filter\n})\n} == %(py11)s\n{%(py11)s = %(py9)s.explicit_filter\n}',), (@py_assert6, @py_assert10)) % {'py3': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(tool_to_filter) if 'tool_to_filter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tool_to_filter) else 'tool_to_filter', 'py7': @pytest_ar._saferepr(@py_assert6), 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel'}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    annotation_filter = tool_to_filter(sentinel.tool, None)
    annotations = [
     Mock(metadata=Mock(tool=sentinel.tool)),
     Mock(metadata=Mock(tool=sentinel.other_tool)),
     Mock(metadata=Mock(tool=sentinel.tool))]
    @py_assert2 = annotation_filter(annotations)
    @py_assert5 = [
     annotations[0], annotations[2]]
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(annotations) if 'annotations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(annotations) else 'annotations', 'py0': @pytest_ar._saferepr(annotation_filter) if 'annotation_filter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(annotation_filter) else 'annotation_filter', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    with raises(ValueError):
        tool_to_filter(sentinel.tool, sentinel.explicit_filter)