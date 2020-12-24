# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_uuid.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 9759 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from concrete.util import generate_UUID, bin_to_hex, hex_to_bin, AnalyticUUIDGeneratorFactory, generate_uuid_unif, generate_hex_unif, split_uuid, join_uuid
from concrete import AnnotationMetadata, Communication
from concrete.validate import validate_communication
import re, time
from pytest import raises
UUID_RE = re.compile('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')

def test_generate_UUID():
    comm = Communication()
    comm.uuid = generate_UUID()


def test_validate_minimal_communication_with_uuid():
    comm = Communication()
    comm.id = 'myID'
    comm.metadata = AnnotationMetadata(tool='TEST', timestamp=int(time.time()))
    comm.type = 'Test Communication'
    comm.uuid = generate_UUID()
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None


def test_hex_to_bin():
    @py_assert1 = '0'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = '1'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = '2'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 2
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = '3'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 3
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = '4'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 4
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = '5'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 5
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = '6'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 6
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = '7'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 7
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = '8'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 8
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = '9'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 9
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'a'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 10
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'A'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 10
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'b'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 11
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'B'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 11
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'c'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 12
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'C'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 12
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'd'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 13
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'D'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 13
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'e'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 14
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'E'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 14
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'f'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 15
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'F'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 15
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 'caf'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 15
    @py_assert8 = 10
    @py_assert10 = 16
    @py_assert12 = @py_assert8 * @py_assert10
    @py_assert13 = @py_assert6 + @py_assert12
    @py_assert14 = 12
    @py_assert16 = 256
    @py_assert18 = @py_assert14 * @py_assert16
    @py_assert19 = @py_assert13 + @py_assert18
    @py_assert5 = @py_assert3 == @py_assert19
    if not @py_assert5:
        @py_format20 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == ((%(py7)s + (%(py9)s * %(py11)s)) + (%(py15)s * %(py17)s))',), (@py_assert3, @py_assert19)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py17': @pytest_ar._saferepr(@py_assert16), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin', 'py7': @pytest_ar._saferepr(@py_assert6), 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format22 = ('' + 'assert %(py21)s') % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert19 = None
    @py_assert1 = 'cafe3'
    @py_assert3 = hex_to_bin(@py_assert1)
    @py_assert6 = 3
    @py_assert8 = 14
    @py_assert10 = 16
    @py_assert12 = @py_assert8 * @py_assert10
    @py_assert13 = @py_assert6 + @py_assert12
    @py_assert14 = 15
    @py_assert16 = 256
    @py_assert18 = @py_assert14 * @py_assert16
    @py_assert19 = @py_assert13 + @py_assert18
    @py_assert20 = 10
    @py_assert22 = 4096
    @py_assert24 = @py_assert20 * @py_assert22
    @py_assert25 = @py_assert19 + @py_assert24
    @py_assert26 = 12
    @py_assert28 = 65536
    @py_assert30 = @py_assert26 * @py_assert28
    @py_assert31 = @py_assert25 + @py_assert30
    @py_assert5 = @py_assert3 == @py_assert31
    if not @py_assert5:
        @py_format32 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == ((((%(py7)s + (%(py9)s * %(py11)s)) + (%(py15)s * %(py17)s)) + (%(py21)s * %(py23)s)) + (%(py27)s * %(py29)s))',), (@py_assert3, @py_assert31)) % {'py23': @pytest_ar._saferepr(@py_assert22), 'py2': @pytest_ar._saferepr(@py_assert1), 'py17': @pytest_ar._saferepr(@py_assert16), 'py27': @pytest_ar._saferepr(@py_assert26), 'py0': @pytest_ar._saferepr(hex_to_bin) if 'hex_to_bin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hex_to_bin) else 'hex_to_bin', 'py4': @pytest_ar._saferepr(@py_assert3), 'py15': @pytest_ar._saferepr(@py_assert14), 'py21': @pytest_ar._saferepr(@py_assert20), 'py29': @pytest_ar._saferepr(@py_assert28), 'py7': @pytest_ar._saferepr(@py_assert6), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format34 = ('' + 'assert %(py33)s') % {'py33': @py_format32}
        raise AssertionError(@pytest_ar._format_explanation(@py_format34))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert19 = @py_assert20 = @py_assert22 = @py_assert24 = @py_assert25 = @py_assert26 = @py_assert28 = @py_assert30 = @py_assert31 = None


def test_bin_to_hex():
    @py_assert1 = 0
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert6 = '0'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 1
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert6 = '1'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 2
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert6 = '2'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 3
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert6 = '3'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 4
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert6 = '4'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 5
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert6 = '5'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 6
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert6 = '6'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 7
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert6 = '7'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 8
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert6 = '8'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 9
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert6 = '9'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = 10
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert5 = @py_assert3.lower
    @py_assert7 = @py_assert5()
    @py_assert10 = 'a'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.lower\n}()\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 11
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert5 = @py_assert3.lower
    @py_assert7 = @py_assert5()
    @py_assert10 = 'b'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.lower\n}()\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 12
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert5 = @py_assert3.lower
    @py_assert7 = @py_assert5()
    @py_assert10 = 'c'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.lower\n}()\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 13
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert5 = @py_assert3.lower
    @py_assert7 = @py_assert5()
    @py_assert10 = 'd'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.lower\n}()\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 14
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert5 = @py_assert3.lower
    @py_assert7 = @py_assert5()
    @py_assert10 = 'e'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.lower\n}()\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 15
    @py_assert3 = bin_to_hex(@py_assert1)
    @py_assert5 = @py_assert3.lower
    @py_assert7 = @py_assert5()
    @py_assert10 = 'f'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.lower\n}()\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 15
    @py_assert3 = 10
    @py_assert5 = 16
    @py_assert7 = @py_assert3 * @py_assert5
    @py_assert8 = @py_assert1 + @py_assert7
    @py_assert9 = 12
    @py_assert11 = 256
    @py_assert13 = @py_assert9 * @py_assert11
    @py_assert14 = @py_assert8 + @py_assert13
    @py_assert15 = bin_to_hex(@py_assert14)
    @py_assert17 = @py_assert15.lower
    @py_assert19 = @py_assert17()
    @py_assert22 = 'caf'
    @py_assert21 = @py_assert19 == @py_assert22
    if not @py_assert21:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert21,), ('%(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = %(py0)s(((%(py2)s + (%(py4)s * %(py6)s)) + (%(py10)s * %(py12)s)))\n}.lower\n}()\n} == %(py23)s',), (@py_assert19, @py_assert22)) % {'py12': @pytest_ar._saferepr(@py_assert11), 'py23': @pytest_ar._saferepr(@py_assert22), 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py18': @pytest_ar._saferepr(@py_assert17), 'py16': @pytest_ar._saferepr(@py_assert15), 'py4': @pytest_ar._saferepr(@py_assert3), 'py20': @pytest_ar._saferepr(@py_assert19), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert22 = None
    @py_assert1 = 3
    @py_assert3 = 14
    @py_assert5 = 16
    @py_assert7 = @py_assert3 * @py_assert5
    @py_assert8 = @py_assert1 + @py_assert7
    @py_assert9 = 15
    @py_assert11 = 256
    @py_assert13 = @py_assert9 * @py_assert11
    @py_assert14 = @py_assert8 + @py_assert13
    @py_assert15 = 10
    @py_assert17 = 4096
    @py_assert19 = @py_assert15 * @py_assert17
    @py_assert20 = @py_assert14 + @py_assert19
    @py_assert21 = 12
    @py_assert23 = 65536
    @py_assert25 = @py_assert21 * @py_assert23
    @py_assert26 = @py_assert20 + @py_assert25
    @py_assert27 = bin_to_hex(@py_assert26)
    @py_assert29 = @py_assert27.lower
    @py_assert31 = @py_assert29()
    @py_assert34 = 'cafe3'
    @py_assert33 = @py_assert31 == @py_assert34
    if not @py_assert33:
        @py_format36 = @pytest_ar._call_reprcompare(('==',), (@py_assert33,), ('%(py32)s\n{%(py32)s = %(py30)s\n{%(py30)s = %(py28)s\n{%(py28)s = %(py0)s(((((%(py2)s + (%(py4)s * %(py6)s)) + (%(py10)s * %(py12)s)) + (%(py16)s * %(py18)s)) + (%(py22)s * %(py24)s)))\n}.lower\n}()\n} == %(py35)s',), (@py_assert31, @py_assert34)) % {'py30': @pytest_ar._saferepr(@py_assert29), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py18': @pytest_ar._saferepr(@py_assert17), 'py16': @pytest_ar._saferepr(@py_assert15), 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py24': @pytest_ar._saferepr(@py_assert23), 'py35': @pytest_ar._saferepr(@py_assert34), 'py28': @pytest_ar._saferepr(@py_assert27), 
         'py22': @pytest_ar._saferepr(@py_assert21), 'py32': @pytest_ar._saferepr(@py_assert31)}
        @py_format38 = ('' + 'assert %(py37)s') % {'py37': @py_format36}
        raise AssertionError(@pytest_ar._format_explanation(@py_format38))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert20 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert26 = @py_assert27 = @py_assert29 = @py_assert31 = @py_assert33 = @py_assert34 = None


def test_bin_to_hex_with_len():
    @py_assert1 = 0
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert8 = '0000'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 1
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert8 = '0001'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 2
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert8 = '0002'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 3
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert8 = '0003'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 4
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert8 = '0004'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 5
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert8 = '0005'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 6
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert8 = '0006'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 7
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert8 = '0007'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 8
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert8 = '0008'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 9
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert8 = '0009'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py6': @pytest_ar._saferepr(@py_assert5), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = 10
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.lower
    @py_assert9 = @py_assert7()
    @py_assert12 = '000a'
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.lower\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = 11
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.lower
    @py_assert9 = @py_assert7()
    @py_assert12 = '000b'
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.lower\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = 12
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.lower
    @py_assert9 = @py_assert7()
    @py_assert12 = '000c'
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.lower\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = 13
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.lower
    @py_assert9 = @py_assert7()
    @py_assert12 = '000d'
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.lower\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = 14
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.lower
    @py_assert9 = @py_assert7()
    @py_assert12 = '000e'
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.lower\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = 15
    @py_assert3 = 4
    @py_assert5 = bin_to_hex(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.lower
    @py_assert9 = @py_assert7()
    @py_assert12 = '000f'
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.lower\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = 15
    @py_assert3 = 10
    @py_assert5 = 16
    @py_assert7 = @py_assert3 * @py_assert5
    @py_assert8 = @py_assert1 + @py_assert7
    @py_assert9 = 12
    @py_assert11 = 256
    @py_assert13 = @py_assert9 * @py_assert11
    @py_assert14 = @py_assert8 + @py_assert13
    @py_assert15 = 4
    @py_assert17 = bin_to_hex(@py_assert14, @py_assert15)
    @py_assert19 = @py_assert17.lower
    @py_assert21 = @py_assert19()
    @py_assert24 = '0caf'
    @py_assert23 = @py_assert21 == @py_assert24
    if not @py_assert23:
        @py_format26 = @pytest_ar._call_reprcompare(('==', ), (@py_assert23,), ('%(py22)s\n{%(py22)s = %(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py0)s(((%(py2)s + (%(py4)s * %(py6)s)) + (%(py10)s * %(py12)s)), %(py16)s)\n}.lower\n}()\n} == %(py25)s', ), (@py_assert21, @py_assert24)) % {'py12': @pytest_ar._saferepr(@py_assert11), 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(bin_to_hex) if 'bin_to_hex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bin_to_hex) else 'bin_to_hex', 'py18': @pytest_ar._saferepr(@py_assert17), 'py16': @pytest_ar._saferepr(@py_assert15), 'py22': @pytest_ar._saferepr(@py_assert21), 'py4': @pytest_ar._saferepr(@py_assert3), 'py20': @pytest_ar._saferepr(@py_assert19), 'py6': @pytest_ar._saferepr(@py_assert5), 'py25': @pytest_ar._saferepr(@py_assert24)}
        @py_format28 = 'assert %(py27)s' % {'py27': @py_format26}
        raise AssertionError(@pytest_ar._format_explanation(@py_format28))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert24 = None
    with raises(ValueError):
        bin_to_hex(831459, 4)


def test_split_uuid_valid():
    @py_assert1 = '7575a428-aaf7-4c2e-929e-1e2a0ab59e16'
    @py_assert3 = split_uuid(@py_assert1)
    @py_assert6 = ('7575a428aaf7', '4c2e929e', '1e2a0ab59e16')
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(split_uuid) if 'split_uuid' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(split_uuid) else 'split_uuid'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_split_uuid_too_many_pieces():
    with raises(ValueError):
        split_uuid('aaf7-7575a428-aaf7-4c2e-929e-1e2a0ab59e16')


def test_split_uuid_too_few_pieces():
    with raises(ValueError):
        split_uuid('7575a428-4c2e-929e-1e2a0ab59e16')


def test_split_uuid_first_piece_too_long():
    with raises(ValueError):
        split_uuid('7575a428a-aaf7-4c2e-929e-1e2a0ab59e16')


def test_split_uuid_second_piece_too_long():
    with raises(ValueError):
        split_uuid('7575a428-aaf7a-4c2e-929e-1e2a0ab59e16')


def test_split_uuid_third_piece_too_long():
    with raises(ValueError):
        split_uuid('7575a428-aaf7-4c2ea-929e-1e2a0ab59e16')


def test_split_uuid_fourth_piece_too_long():
    with raises(ValueError):
        split_uuid('7575a428-aaf7-4c2e-929ea-1e2a0ab59e16')


def test_split_uuid_fifth_piece_too_long():
    with raises(ValueError):
        split_uuid('7575a428-aaf7-4c2e-929e-1e2a0ab59e16a')


def test_split_uuid_first_piece_too_short():
    with raises(ValueError):
        split_uuid('7575a42-aaf7-4c2e-929e-1e2a0ab59e16')


def test_split_uuid_second_piece_too_short():
    with raises(ValueError):
        split_uuid('7575a428-aaf-4c2e-929e-1e2a0ab59e16')


def test_split_uuid_third_piece_too_short():
    with raises(ValueError):
        split_uuid('7575a428-aaf7-4c2-929e-1e2a0ab59e16')


def test_split_uuid_fourth_piece_too_short():
    with raises(ValueError):
        split_uuid('7575a428-aaf7-4c2e-929-1e2a0ab59e16')


def test_split_uuid_fifth_piece_too_short():
    with raises(ValueError):
        split_uuid('7575a428-aaf7-4c2e-929e-1e2a0ab59e1')


def test_join_uuid_valid():
    @py_assert1 = '7575a428aaf7'
    @py_assert3 = '4c2e929e'
    @py_assert5 = '1e2a0ab59e16'
    @py_assert7 = join_uuid(@py_assert1, @py_assert3, @py_assert5)
    @py_assert10 = '7575a428-aaf7-4c2e-929e-1e2a0ab59e16'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py2)s, %(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(join_uuid) if 'join_uuid' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(join_uuid) else 'join_uuid', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_join_uuid_first_piece_too_long():
    with raises(ValueError):
        join_uuid('7575a428aaf7a', '4c2e929e', '1e2a0ab59e16')


def test_join_uuid_second_piece_too_long():
    with raises(ValueError):
        join_uuid('7575a428aaf7', '4c2e929ea', '1e2a0ab59e16')


def test_join_uuid_third_piece_too_long():
    with raises(ValueError):
        join_uuid('7575a428aaf7', '4c2e929e', '1e2a0ab59e16a')


def test_join_uuid_first_piece_too_short():
    with raises(ValueError):
        join_uuid('7575a428aaf', '4c2e929e', '1e2a0ab59e16')


def test_join_uuid_second_piece_too_short():
    with raises(ValueError):
        join_uuid('7575a428aaf7', '4c2e929', '1e2a0ab59e16')


def test_join_uuid_third_piece_too_short():
    with raises(ValueError):
        join_uuid('7575a428aaf7', '4c2e929e', '1e2a0ab59e1')


def test_generate_hex_unif_range():
    n = 1000
    r = set()
    for i in range(n):
        r.add(generate_hex_unif(1))

    @py_assert2 = lambda x: str(x).lower()
    @py_assert5 = map(@py_assert2, r)
    @py_assert7 = sorted(@py_assert5)
    @py_assert10 = [c for c in '0123456789abcdef']
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py1)s(%(py3)s, %(py4)s)\n})\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_generate_hex_unif_len():
    h = generate_hex_unif(21)
    @py_assert2 = len(h)
    @py_assert5 = 21
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(h) if 'h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(h) else 'h', 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = (c for c in h)
    @py_assert4 = set(@py_assert2)
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 > @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('>', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} > %(py10)s', ), (@py_assert6, @py_assert9)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_generate_hex_unif_spread():
    n = 1000
    m = 32
    s = set([generate_hex_unif(m) for i in range(n)])
    @py_assert2 = len(s)
    @py_assert4 = @py_assert2 == n
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, n)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py5': @pytest_ar._saferepr(n) if 'n' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n) else 'n', 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_generate_uuid_unif_format():
    u = generate_uuid_unif()
    @py_assert1 = UUID_RE.match
    @py_assert4 = @py_assert1(u)
    @py_assert7 = None
    @py_assert6 = @py_assert4 is not @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.match\n}(%(py3)s)\n} is not %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(u) if 'u' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(u) else 'u', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(UUID_RE) if 'UUID_RE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(UUID_RE) else 'UUID_RE'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_generate_uuid_unif_spread():
    n = 1000
    s = set([generate_uuid_unif() for i in range(n)])
    @py_assert2 = len(s)
    @py_assert4 = @py_assert2 == n
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, n)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py5': @pytest_ar._saferepr(n) if 'n' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n) else 'n', 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


class Duck(object):
    pass


def test_AnalyticUUIDGeneratorFactory_x_prefix_no_comm():
    n = 1000
    augf = AnalyticUUIDGeneratorFactory()
    u = augf.comm_uuid
    for i in range(n):
        aug = augf.create()
        @py_assert2 = next(aug)
        @py_assert4 = @py_assert2.uuidString
        @py_assert6 = @py_assert4.startswith
        @py_assert8 = u[:13]
        @py_assert10 = @py_assert6(@py_assert8)
        if not @py_assert10:
            @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}.uuidString\n}.startswith\n}(%(py9)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(aug) if 'aug' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(aug) else 'aug', 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(@py_assert8)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None


def test_AnalyticUUIDGeneratorFactory_x_prefix_with_comm():
    n = 1000
    u = '7575a428-aaf7-4c2e-929e-1e2a0ab59e16'
    comm = Duck()
    comm.uuid = Duck()
    comm.uuid.uuidString = u
    augf = AnalyticUUIDGeneratorFactory(comm)
    @py_assert1 = augf.comm_uuid
    @py_assert3 = @py_assert1 == u
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.comm_uuid\n} == %(py4)s', ), (@py_assert1, u)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(u) if 'u' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(u) else 'u', 'py0': @pytest_ar._saferepr(augf) if 'augf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augf) else 'augf'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    for i in range(n):
        aug = augf.create()
        @py_assert2 = next(aug)
        @py_assert4 = @py_assert2.uuidString
        @py_assert6 = @py_assert4.startswith
        @py_assert8 = u[:13]
        @py_assert10 = @py_assert6(@py_assert8)
        if not @py_assert10:
            @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}.uuidString\n}.startswith\n}(%(py9)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(aug) if 'aug' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(aug) else 'aug', 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(@py_assert8)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None


def test_AnalyticUUIDGeneratorFactory_x_prefix_bad_comm_uuid():
    u = '7575a428a-aaf7-4c2e-929e-1e2a0ab59e16'
    comm = Duck()
    comm.uuid = Duck()
    comm.uuid.uuidString = u
    augf = AnalyticUUIDGeneratorFactory(comm)
    with raises(ValueError):
        augf.create()


def test_AnalyticUUIDGeneratorFactory_y_prefix():
    m = 100
    n = 100
    augf = AnalyticUUIDGeneratorFactory()
    for i in range(m):
        aug = augf.create()
        uu = next(aug).uuidString
        for j in range(n - 1):
            @py_assert2 = next(aug)
            @py_assert4 = @py_assert2.uuidString
            @py_assert6 = @py_assert4.startswith
            @py_assert8 = uu[:23]
            @py_assert10 = @py_assert6(@py_assert8)
            if not @py_assert10:
                @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}.uuidString\n}.startswith\n}(%(py9)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(aug) if 'aug' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(aug) else 'aug', 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(@py_assert8)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format12))
            @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None


def test_AnalyticUUIDGeneratorFactory_z_increment():
    m = 100
    n = 100
    augf = AnalyticUUIDGeneratorFactory()
    for i in range(m):
        aug = augf.create()
        u = next(aug).uuidString
        z = int(u[24:], 16)
        for j in range(n - 1):
            u = next(aug).uuidString
            @py_assert1 = u[24:]
            @py_assert3 = 16
            @py_assert5 = int(@py_assert1, @py_assert3)
            @py_assert9 = 1
            @py_assert11 = z + @py_assert9
            @py_assert12 = 2
            @py_assert14 = 48
            @py_assert16 = @py_assert12 ** @py_assert14
            @py_assert17 = @py_assert11 % @py_assert16
            @py_assert7 = @py_assert5 == @py_assert17
            if not @py_assert7:
                @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == ((%(py8)s + %(py10)s) %% (%(py13)s ** %(py15)s))', ), (@py_assert5, @py_assert17)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(z) if 'z' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(z) else 'z', 'py0': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py15': @pytest_ar._saferepr(@py_assert14), 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
                @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
                raise AssertionError(@pytest_ar._format_explanation(@py_format20))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None
            z = (z + 1) % 281474976710656


def test_AnalyticUUIDGeneratorFactory_x_prefix_spread():
    m = 100
    s = set()
    for i in range(m):
        augf = AnalyticUUIDGeneratorFactory()
        aug = augf.create()
        u = next(aug).uuidString
        s.add(u[:13])

    @py_assert2 = len(s)
    @py_assert4 = @py_assert2 == m
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, m)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py5': @pytest_ar._saferepr(m) if 'm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(m) else 'm', 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_AnalyticUUIDGeneratorFactory_y_prefix_spread():
    m = 10
    augf = AnalyticUUIDGeneratorFactory()
    s = set()
    for i in range(m):
        aug = augf.create()
        u = next(aug).uuidString
        s.add(u[:23])

    @py_assert2 = len(s)
    @py_assert4 = @py_assert2 == m
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, m)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py5': @pytest_ar._saferepr(m) if 'm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(m) else 'm', 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_AnalyticUUIDGeneratorFactory_spread():
    m = 100
    n = 100
    augf = AnalyticUUIDGeneratorFactory()
    s = set()
    for i in range(m):
        aug = augf.create()
        u = next(aug).uuidString
        s.add(u)
        for j in range(n - 1):
            u = next(aug).uuidString
            s.add(u)

    @py_assert2 = len(s)
    @py_assert7 = m * n
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py5)s * %(py6)s)',), (@py_assert2, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py5': @pytest_ar._saferepr(m) if 'm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(m) else 'm', 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(n) if 'n' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n) else 'n'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert7 = None