# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_mem_io.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 3540 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from concrete.util import read_communication_from_buffer, write_communication_to_buffer, communication_deep_copy
from concrete.util import create_comm
from concrete import Token

def assert_simple_comms_equal(comm1, comm2):
    @py_assert1 = comm1.id
    @py_assert5 = comm2.id
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py6)s\n{%(py6)s = %(py4)s.id\n}',), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(comm2) if 'comm2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm2) else 'comm2', 'py0': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = comm1.uuid
    @py_assert3 = @py_assert1.uuidString
    @py_assert7 = comm2.uuid
    @py_assert9 = @py_assert7.uuidString
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.uuid\n}.uuidString\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.uuid\n}.uuidString\n}',), (@py_assert3, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(comm2) if 'comm2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm2) else 'comm2'}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = comm1.metadata
    @py_assert3 = @py_assert1.tool
    @py_assert7 = comm2.metadata
    @py_assert9 = @py_assert7.tool
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.metadata\n}.tool\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.metadata\n}.tool\n}',), (@py_assert3, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(comm2) if 'comm2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm2) else 'comm2'}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = comm1.metadata
    @py_assert3 = @py_assert1.timestamp
    @py_assert7 = comm2.metadata
    @py_assert9 = @py_assert7.timestamp
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.metadata\n}.timestamp\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.metadata\n}.timestamp\n}',), (@py_assert3, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(comm1) if 'comm1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm1) else 'comm1', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(comm2) if 'comm2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm2) else 'comm2'}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert0 = comm1.sectionList[0]
    @py_assert2 = @py_assert0.uuid
    @py_assert4 = @py_assert2.uuidString
    @py_assert7 = comm2.sectionList[0]
    @py_assert9 = @py_assert7.uuid
    @py_assert11 = @py_assert9.uuidString
    @py_assert6 = @py_assert4 == @py_assert11
    if not @py_assert6:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.uuid\n}.uuidString\n} == %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s.uuid\n}.uuidString\n}',), (@py_assert4, @py_assert11)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert0 = comm1.sectionList[0]
    @py_assert2 = @py_assert0.kind
    @py_assert5 = comm2.sectionList[0]
    @py_assert7 = @py_assert5.kind
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.kind\n} == %(py8)s\n{%(py8)s = %(py6)s.kind\n}',), (@py_assert2, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(@py_assert0), 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = None
    @py_assert0 = comm1.sectionList[0].sentenceList[0]
    @py_assert2 = @py_assert0.uuid
    @py_assert4 = @py_assert2.uuidString
    @py_assert7 = comm2.sectionList[0].sentenceList[0]
    @py_assert9 = @py_assert7.uuid
    @py_assert11 = @py_assert9.uuidString
    @py_assert6 = @py_assert4 == @py_assert11
    if not @py_assert6:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.uuid\n}.uuidString\n} == %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s.uuid\n}.uuidString\n}',), (@py_assert4, @py_assert11)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert0 = comm1.sectionList[0].sentenceList[0]
    @py_assert2 = @py_assert0.tokenization
    @py_assert4 = @py_assert2.uuid
    @py_assert7 = comm2.sectionList[0].sentenceList[0]
    @py_assert9 = @py_assert7.tokenization
    @py_assert11 = @py_assert9.uuid
    @py_assert6 = @py_assert4 == @py_assert11
    if not @py_assert6:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.tokenization\n}.uuid\n} == %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s.tokenization\n}.uuid\n}',), (@py_assert4, @py_assert11)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert0 = comm1.sectionList[0].sentenceList[0]
    @py_assert2 = @py_assert0.tokenization
    @py_assert4 = @py_assert2.kind
    @py_assert7 = comm2.sectionList[0].sentenceList[0]
    @py_assert9 = @py_assert7.tokenization
    @py_assert11 = @py_assert9.kind
    @py_assert6 = @py_assert4 == @py_assert11
    if not @py_assert6:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.tokenization\n}.kind\n} == %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s.tokenization\n}.kind\n}',), (@py_assert4, @py_assert11)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert0 = comm1.sectionList[0].sentenceList[0]
    @py_assert2 = @py_assert0.tokenization
    @py_assert4 = @py_assert2.metadata
    @py_assert6 = @py_assert4.tool
    @py_assert9 = comm2.sectionList[0].sentenceList[0]
    @py_assert11 = @py_assert9.tokenization
    @py_assert13 = @py_assert11.metadata
    @py_assert15 = @py_assert13.tool
    @py_assert8 = @py_assert6 == @py_assert15
    if not @py_assert8:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.tokenization\n}.metadata\n}.tool\n} == %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py12)s\n{%(py12)s = %(py10)s.tokenization\n}.metadata\n}.tool\n}',), (@py_assert6, @py_assert15)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py16': @pytest_ar._saferepr(@py_assert15), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert0 = comm1.sectionList[0].sentenceList[0]
    @py_assert2 = @py_assert0.tokenization
    @py_assert4 = @py_assert2.metadata
    @py_assert6 = @py_assert4.timestamp
    @py_assert9 = comm2.sectionList[0].sentenceList[0]
    @py_assert11 = @py_assert9.tokenization
    @py_assert13 = @py_assert11.metadata
    @py_assert15 = @py_assert13.timestamp
    @py_assert8 = @py_assert6 == @py_assert15
    if not @py_assert8:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.tokenization\n}.metadata\n}.timestamp\n} == %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py12)s\n{%(py12)s = %(py10)s.tokenization\n}.metadata\n}.timestamp\n}',), (@py_assert6, @py_assert15)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py16': @pytest_ar._saferepr(@py_assert15), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert2 = lambda t: (
     t.text, t.tokenIndex)
    @py_assert4 = comm1.sectionList[0].sentenceList[0]
    @py_assert6 = @py_assert4.tokenization
    @py_assert8 = @py_assert6.tokenList
    @py_assert10 = @py_assert8.tokenList
    @py_assert12 = map(@py_assert2, @py_assert10)
    @py_assert14 = list(@py_assert12)
    @py_assert19 = lambda t: (
     t.text, t.tokenIndex)
    @py_assert21 = comm2.sectionList[0].sentenceList[0]
    @py_assert23 = @py_assert21.tokenization
    @py_assert25 = @py_assert23.tokenList
    @py_assert27 = @py_assert25.tokenList
    @py_assert29 = map(@py_assert19, @py_assert27)
    @py_assert31 = list(@py_assert29)
    @py_assert16 = @py_assert14 == @py_assert31
    if not @py_assert16:
        @py_format33 = @pytest_ar._call_reprcompare(('==',), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py13)s\n{%(py13)s = %(py1)s(%(py3)s, %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.tokenization\n}.tokenList\n}.tokenList\n})\n})\n} == %(py32)s\n{%(py32)s = %(py17)s(%(py30)s\n{%(py30)s = %(py18)s(%(py20)s, %(py28)s\n{%(py28)s = %(py26)s\n{%(py26)s = %(py24)s\n{%(py24)s = %(py22)s.tokenization\n}.tokenList\n}.tokenList\n})\n})\n}',), (@py_assert14, @py_assert31)) % {'py30': @pytest_ar._saferepr(@py_assert29), 'py17': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py22': @pytest_ar._saferepr(@py_assert21), 'py28': @pytest_ar._saferepr(@py_assert27), 'py5': @pytest_ar._saferepr(@py_assert4), 'py15': @pytest_ar._saferepr(@py_assert14), 'py24': @pytest_ar._saferepr(@py_assert23), 'py3': @pytest_ar._saferepr(@py_assert2), 'py20': @pytest_ar._saferepr(@py_assert19), 'py13': @pytest_ar._saferepr(@py_assert12), 'py18': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py32': @pytest_ar._saferepr(@py_assert31), 'py11': @pytest_ar._saferepr(@py_assert10), 'py26': @pytest_ar._saferepr(@py_assert25), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format35 = ('' + 'assert %(py34)s') % {'py34': @py_format33}
        raise AssertionError(@pytest_ar._format_explanation(@py_format35))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert27 = @py_assert29 = @py_assert31 = None


def test_communication_deep_copy():
    comm1 = create_comm('a-b-c', text='foo bar baz .')
    comm2 = communication_deep_copy(comm1)
    comm3 = communication_deep_copy(comm1)
    assert_simple_comms_equal(comm1, comm2)
    assert_simple_comms_equal(comm2, comm3)
    tkzn1 = comm1.sectionList[0].sentenceList[0].tokenization
    tkzn1.tokenList.tokenList[0] = Token(text='bbq', tokenIndex=0)
    tkzn2 = comm2.sectionList[0].sentenceList[0].tokenization
    @py_assert2 = lambda t: t.text
    @py_assert5 = tkzn1.tokenList
    @py_assert7 = @py_assert5.tokenList
    @py_assert9 = map(@py_assert2, @py_assert7)
    @py_assert11 = list(@py_assert9)
    @py_assert16 = lambda t: t.text
    @py_assert19 = tkzn2.tokenList
    @py_assert21 = @py_assert19.tokenList
    @py_assert23 = map(@py_assert16, @py_assert21)
    @py_assert25 = list(@py_assert23)
    @py_assert13 = @py_assert11 != @py_assert25
    if not @py_assert13:
        @py_format27 = @pytest_ar._call_reprcompare(('!=',), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py10)s\n{%(py10)s = %(py1)s(%(py3)s, %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.tokenList\n}.tokenList\n})\n})\n} != %(py26)s\n{%(py26)s = %(py14)s(%(py24)s\n{%(py24)s = %(py15)s(%(py17)s, %(py22)s\n{%(py22)s = %(py20)s\n{%(py20)s = %(py18)s.tokenList\n}.tokenList\n})\n})\n}',), (@py_assert11, @py_assert25)) % {'py12': @pytest_ar._saferepr(@py_assert11), 'py17': @pytest_ar._saferepr(@py_assert16), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py22': @pytest_ar._saferepr(@py_assert21), 'py4': @pytest_ar._saferepr(tkzn1) if 'tkzn1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tkzn1) else 'tkzn1', 'py15': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py20': @pytest_ar._saferepr(@py_assert19), 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py14': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py18': @pytest_ar._saferepr(tkzn2) if 'tkzn2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tkzn2) else 'tkzn2', 'py1': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py26': @pytest_ar._saferepr(@py_assert25), 'py24': @pytest_ar._saferepr(@py_assert23)}
        @py_format29 = ('' + 'assert %(py28)s') % {'py28': @py_format27}
        raise AssertionError(@pytest_ar._format_explanation(@py_format29))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert16 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = None
    assert_simple_comms_equal(comm2, comm3)


def test_read_against_file_contents():
    filename = 'tests/testdata/simple_1.concrete'
    with open(filename, 'rb') as (f):
        buf = f.read()
        comm = read_communication_from_buffer(buf)
        @py_assert2 = 'sentenceForUUID'
        @py_assert4 = hasattr(comm, @py_assert2)
        if not @py_assert4:
            @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert2 = @py_assert4 = None
        @py_assert0 = 'one'
        @py_assert4 = comm.id
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None


def test_read_against_file_contents_no_add_references():
    filename = 'tests/testdata/simple_1.concrete'
    with open(filename, 'rb') as (f):
        buf = f.read()
        comm = read_communication_from_buffer(buf, add_references=False)
        @py_assert2 = 'sentenceForUUID'
        @py_assert4 = hasattr(comm, @py_assert2)
        @py_assert6 = not @py_assert4
        if not @py_assert6:
            @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 'one'
        @py_assert4 = comm.id
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.id\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None


def test_write_against_file_contents():
    filename = 'tests/testdata/simple_1.concrete'
    with open(filename, 'rb') as (f):
        f_buf = f.read()
        comm = read_communication_from_buffer(f_buf)
    buf = write_communication_to_buffer(comm)
    @py_assert1 = f_buf == buf
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (f_buf, buf)) % {'py2': @pytest_ar._saferepr(buf) if 'buf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(buf) else 'buf', 'py0': @pytest_ar._saferepr(f_buf) if 'f_buf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f_buf) else 'f_buf'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_read_write_fixed_point():
    comm = create_comm('comm-1')
    buf_1 = write_communication_to_buffer(comm)
    buf_2 = write_communication_to_buffer(read_communication_from_buffer(buf_1))
    @py_assert1 = buf_1 == buf_2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (buf_1, buf_2)) % {'py2': @pytest_ar._saferepr(buf_2) if 'buf_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(buf_2) else 'buf_2', 'py0': @pytest_ar._saferepr(buf_1) if 'buf_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(buf_1) else 'buf_1'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None