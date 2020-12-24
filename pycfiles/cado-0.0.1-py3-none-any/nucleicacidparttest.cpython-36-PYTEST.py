# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/shawn/Desktop/projects/cadnano2.5/cadnano/tests/nucleicacidparttest.py
# Compiled at: 2018-01-15 17:51:29
# Size of source mod 2**32: 1661 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, math
from cntestcase import cnapp
from cadnano.part.nucleicacidpart import NucleicAcidPart

def create3Helix(doc, direction, length):
    part = doc.createNucleicAcidPart()
    @py_assert2 = part.getidNums
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 0
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.getidNums\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(part) if 'part' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(part) else 'part',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    radius = part.radius()
    origin_pt00 = (0, 0, 0)
    origin_pt90 = (0, 2 * radius, 0)
    theta = math.radians(30)
    origin_pt60 = (2 * radius * math.cos(-theta), 2 * radius * math.sin(-theta), 0)
    (part.createVirtualHelix)(*origin_pt00, id_num=0, length=length)
    (part.createVirtualHelix)(*origin_pt60, id_num=1, length=length)
    (part.createVirtualHelix)(*origin_pt90, id_num=2, length=length)
    return part


@pytest.mark.parametrize('direction', [(0, 0, 1), (0, 1, 0)])
def testVirtualHelixCreate(cnapp, direction):
    doc = cnapp.document
    part = create3Helix(doc, direction, 42)
    id_nums = part.getidNums()
    @py_assert2 = len(id_nums)
    @py_assert5 = 3
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(id_nums) if 'id_nums' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id_nums) else 'id_nums',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def testVirtualHelixResize(cnapp):
    doc = cnapp.document
    start_length = 42
    end_length = 84
    part = create3Helix(doc, (0, 0, 1), start_length)
    @py_assert1 = part.getVirtualHelixProperties
    @py_assert3 = 1
    @py_assert5 = 'length'
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert9 = @py_assert7 == start_length
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.getVirtualHelixProperties\n}(%(py4)s, %(py6)s)\n} == %(py10)s', ), (@py_assert7, start_length)) % {'py0':@pytest_ar._saferepr(part) if 'part' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(part) else 'part',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(start_length) if 'start_length' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(start_length) else 'start_length'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    part.setVirtualHelixSize(1, end_length)
    @py_assert1 = part.getVirtualHelixProperties
    @py_assert3 = 1
    @py_assert5 = 'length'
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert9 = @py_assert7 == end_length
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.getVirtualHelixProperties\n}(%(py4)s, %(py6)s)\n} == %(py10)s', ), (@py_assert7, end_length)) % {'py0':@pytest_ar._saferepr(part) if 'part' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(part) else 'part',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(end_length) if 'end_length' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(end_length) else 'end_length'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    part.setVirtualHelixSize(1, start_length)
    @py_assert1 = part.getVirtualHelixProperties
    @py_assert3 = 1
    @py_assert5 = 'length'
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert9 = @py_assert7 == start_length
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.getVirtualHelixProperties\n}(%(py4)s, %(py6)s)\n} == %(py10)s', ), (@py_assert7, start_length)) % {'py0':@pytest_ar._saferepr(part) if 'part' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(part) else 'part',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(start_length) if 'start_length' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(start_length) else 'start_length'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def testRemove(cnapp):
    doc = cnapp.document
    start_length = 42
    part = create3Helix(doc, (0, 0, 1), start_length)
    @py_assert2 = doc.children
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.children\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    us = part.undoStack()
    part.remove()
    @py_assert2 = doc.children
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 0
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.children\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    us.undo()
    @py_assert2 = doc.children
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.children\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None