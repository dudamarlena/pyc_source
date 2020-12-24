# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/eevee/dev/camel.git/build/lib/camel/tests/test_general.py
# Compiled at: 2015-10-19 22:52:12
# Size of source mod 2**32: 3427 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, collections, datetime, pytest
from camel import Camel, CamelRegistry, PYTHON_TYPES

@pytest.mark.parametrize(('value', 'expected_serialization'), [
 (None, 'null\n...\n'),
 ('ⓤⓝⓘⓒⓞⓓⓔ', 'ⓤⓝⓘⓒⓞⓓⓔ\n...\n'),
 ('bytes', '!!binary |\n  Ynl0ZXM=\n'),
 (True, 'true\n...\n'),
 (133, '133\n...\n'),
 (10889035741470030830827987437816582766592, '10889035741470030830827987437816582766592\n...\n'),
 (3.52, '3.52\n...\n'),
 (
  [
   1, 2, 'three'], '- 1\n- 2\n- three\n'),
 (
  {'x': 7, 'y': 8, 'z': 9}, 'x: 7\ny: 8\nz: 9\n'),
 (
  set('qvx'), '!!set\nq: null\nv: null\nx: null\n'),
 (
  datetime.date(2015, 10, 21), '2015-10-21\n...\n'),
 (
  datetime.datetime(2015, 10, 21, 4, 29), '2015-10-21 04:29:00\n...\n'),
 (
  collections.OrderedDict([('a', 1), ('b', 2), ('c', 3)]), '!!omap\n- a: 1\n- b: 2\n- c: 3\n')])
def test_basic_roundtrip(value, expected_serialization):
    camel = Camel()
    dumped = camel.dump(value)
    @py_assert1 = dumped == expected_serialization
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (dumped, expected_serialization)) % {'py2': @pytest_ar._saferepr(expected_serialization) if 'expected_serialization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_serialization) else 'expected_serialization', 'py0': @pytest_ar._saferepr(dumped) if 'dumped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dumped) else 'dumped'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = camel.load
    @py_assert4 = @py_assert1(dumped)
    @py_assert6 = @py_assert4 == value
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.load\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, value)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(camel) if 'camel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(camel) else 'camel', 'py3': @pytest_ar._saferepr(dumped) if 'dumped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dumped) else 'dumped'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None


def test_tuple_roundtrip():
    value = (
     4, 3, 2)
    camel = Camel()
    dumped = camel.dump(value)
    @py_assert2 = '- 4\n- 3\n- 2\n'
    @py_assert1 = dumped == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (dumped, @py_assert2)) % {'py0': @pytest_ar._saferepr(dumped) if 'dumped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dumped) else 'dumped', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = ('' + 'assert %(py5)s') % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = camel.load
    @py_assert4 = @py_assert1(dumped)
    @py_assert9 = list(value)
    @py_assert6 = @py_assert4 == @py_assert9
    if not @py_assert6:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.load\n}(%(py3)s)\n} == %(py10)s\n{%(py10)s = %(py7)s(%(py8)s)\n}',), (@py_assert4, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(camel) if 'camel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(camel) else 'camel', 'py3': @pytest_ar._saferepr(dumped) if 'dumped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dumped) else 'dumped', 'py8': @pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value', 'py10': @pytest_ar._saferepr(@py_assert9), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list'}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = None


def test_frozenset_roundtrip():
    value = frozenset((4, 3, 2))
    camel = Camel()
    dumped = camel.dump(value)
    @py_assert2 = '!!set\n2: null\n3: null\n4: null\n'
    @py_assert1 = dumped == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (dumped, @py_assert2)) % {'py0': @pytest_ar._saferepr(dumped) if 'dumped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dumped) else 'dumped', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = ('' + 'assert %(py5)s') % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = camel.load
    @py_assert4 = @py_assert1(dumped)
    @py_assert9 = set(value)
    @py_assert6 = @py_assert4 == @py_assert9
    if not @py_assert6:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.load\n}(%(py3)s)\n} == %(py10)s\n{%(py10)s = %(py7)s(%(py8)s)\n}',), (@py_assert4, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(camel) if 'camel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(camel) else 'camel', 'py3': @pytest_ar._saferepr(dumped) if 'dumped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dumped) else 'dumped', 'py8': @pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value', 'py10': @pytest_ar._saferepr(@py_assert9), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = None


@pytest.mark.parametrize(('value', 'expected_serialization'), [
 ((4, 3, 2), '!!python/tuple\n- 4\n- 3\n- 2\n'),
 (complex(5.0, 12.0), '!!python/complex 5+12j\n...\n'),
 (complex(0.0, 2.0), '!!python/complex 2j\n...\n'),
 (
  frozenset((4, 3, 2)), '!!python/frozenset\n- 2\n- 3\n- 4\n')])
def test_python_roundtrip(value, expected_serialization):
    camel = Camel([PYTHON_TYPES])
    dumped = camel.dump(value)
    @py_assert1 = dumped == expected_serialization
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (dumped, expected_serialization)) % {'py2': @pytest_ar._saferepr(expected_serialization) if 'expected_serialization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_serialization) else 'expected_serialization', 'py0': @pytest_ar._saferepr(dumped) if 'dumped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dumped) else 'dumped'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    vanilla_camel = Camel()
    @py_assert1 = vanilla_camel.load
    @py_assert4 = @py_assert1(dumped)
    @py_assert6 = @py_assert4 == value
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.load\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, value)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(vanilla_camel) if 'vanilla_camel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vanilla_camel) else 'vanilla_camel', 'py3': @pytest_ar._saferepr(dumped) if 'dumped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dumped) else 'dumped'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None


class DieRoll(tuple):

    def __new__(cls, a, b):
        return tuple.__new__(cls, [a, b])

    def __repr__(self):
        return 'DieRoll(%s,%s)' % self


reg = CamelRegistry()

@reg.dumper(DieRoll, 'roll', version=None)
def dump_dice(data):
    return '{}d{}'.format(*data)


@reg.loader('roll', version=None)
def load_dice(data, version):
    a, _, b = data.partition('d')
    return DieRoll(int(a), int(b))


def test_dieroll():
    value = DieRoll(3, 6)
    camel = Camel([reg])
    dumped = camel.dump(value)
    @py_assert2 = '!roll 3d6\n...\n'
    @py_assert1 = dumped == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (dumped, @py_assert2)) % {'py0': @pytest_ar._saferepr(dumped) if 'dumped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dumped) else 'dumped', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = camel.load
    @py_assert4 = @py_assert1(dumped)
    @py_assert6 = @py_assert4 == value
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.load\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, value)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(camel) if 'camel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(camel) else 'camel', 'py3': @pytest_ar._saferepr(dumped) if 'dumped' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dumped) else 'dumped'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None