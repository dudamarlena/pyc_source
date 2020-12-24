# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/shawn/Desktop/projects/cadnano2.5/cadnano/tests/strandsettest.py
# Compiled at: 2018-01-23 23:43:02
# Size of source mod 2**32: 3304 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from cntestcase import cnapp
from nucleicacidparttest import create3Helix

def testStrandset(cnapp):
    doc = cnapp.document
    HELIX_LENGTH = 42
    part = create3Helix(doc, [0, 0, 1], HELIX_LENGTH)
    fwd_ss, rev_ss = part.getStrandSets(0)
    @py_assert1 = fwd_ss.isForward
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.isForward\n}()\n}') % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = rev_ss.isForward
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.isForward\n}()\n}') % {'py0':@pytest_ar._saferepr(rev_ss) if 'rev_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rev_ss) else 'rev_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = rev_ss.isReverse
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.isReverse\n}()\n}') % {'py0':@pytest_ar._saferepr(rev_ss) if 'rev_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rev_ss) else 'rev_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = fwd_ss.length
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == HELIX_LENGTH
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.length\n}()\n} == %(py6)s', ), (@py_assert3, HELIX_LENGTH)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(HELIX_LENGTH) if 'HELIX_LENGTH' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(HELIX_LENGTH) else 'HELIX_LENGTH'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = fwd_ss.idNum
    @py_assert3 = @py_assert1()
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.idNum\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = fwd_ss.createStrand
    @py_assert3 = 0
    @py_assert5 = 84
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 is @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.createStrand\n}(%(py4)s, %(py6)s)\n} is %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    strand1_fwd = fwd_ss.createStrand(0, 21)
    @py_assert2 = None
    @py_assert1 = strand1_fwd is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (strand1_fwd, @py_assert2)) % {'py0':@pytest_ar._saferepr(strand1_fwd) if 'strand1_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand1_fwd) else 'strand1_fwd',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    strand1_rev = rev_ss.createStrand(3, 24)
    @py_assert2 = None
    @py_assert1 = strand1_rev is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (strand1_rev, @py_assert2)) % {'py0':@pytest_ar._saferepr(strand1_rev) if 'strand1_rev' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand1_rev) else 'strand1_rev',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    strand1_get = fwd_ss.getStrand(1)
    @py_assert1 = strand1_fwd is strand1_get
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (strand1_fwd, strand1_get)) % {'py0':@pytest_ar._saferepr(strand1_fwd) if 'strand1_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand1_fwd) else 'strand1_fwd',  'py2':@pytest_ar._saferepr(strand1_get) if 'strand1_get' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand1_get) else 'strand1_get'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    overlapping = fwd_ss.getOverlappingStrands(0, 21)
    @py_assert2 = overlapping[0]
    @py_assert1 = strand1_fwd == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (strand1_fwd, @py_assert2)) % {'py0':@pytest_ar._saferepr(strand1_fwd) if 'strand1_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand1_fwd) else 'strand1_fwd',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    neighbors = fwd_ss.getNeighbors(strand1_fwd)
    @py_assert2 = (None, None)
    @py_assert1 = neighbors == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (neighbors, @py_assert2)) % {'py0':@pytest_ar._saferepr(neighbors) if 'neighbors' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(neighbors) else 'neighbors',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    strand2_fwd = fwd_ss.createStrand(19, 30)
    @py_assert2 = None
    @py_assert1 = strand2_fwd is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (strand2_fwd, @py_assert2)) % {'py0':@pytest_ar._saferepr(strand2_fwd) if 'strand2_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand2_fwd) else 'strand2_fwd',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    strand2_fwd = fwd_ss.createStrand(23, 30)
    @py_assert2 = None
    @py_assert1 = strand2_fwd is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (strand2_fwd, @py_assert2)) % {'py0':@pytest_ar._saferepr(strand2_fwd) if 'strand2_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand2_fwd) else 'strand2_fwd',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    idxs3 = (31, 40)
    strand3_fwd = (fwd_ss.createStrand)(*idxs3)
    @py_assert2 = None
    @py_assert1 = strand3_fwd is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (strand3_fwd, @py_assert2)) % {'py0':@pytest_ar._saferepr(strand3_fwd) if 'strand3_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_fwd) else 'strand3_fwd',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    strand3_rev = (rev_ss.createStrand)(*idxs3)
    @py_assert2 = None
    @py_assert1 = strand3_rev is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (strand3_rev, @py_assert2)) % {'py0':@pytest_ar._saferepr(strand3_rev) if 'strand3_rev' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_rev) else 'strand3_rev',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    neighbors = fwd_ss.getNeighbors(strand1_fwd)
    @py_assert2 = (None, strand2_fwd)
    @py_assert1 = neighbors == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (neighbors, @py_assert2)) % {'py0':@pytest_ar._saferepr(neighbors) if 'neighbors' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(neighbors) else 'neighbors',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    neighbors = fwd_ss.getNeighbors(strand2_fwd)
    @py_assert2 = (strand1_fwd, strand3_fwd)
    @py_assert1 = neighbors == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (neighbors, @py_assert2)) % {'py0':@pytest_ar._saferepr(neighbors) if 'neighbors' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(neighbors) else 'neighbors',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    fwd_ss.removeStrand(strand2_fwd)
    neighbors = fwd_ss.getNeighbors(strand3_fwd)
    @py_assert2 = (strand1_fwd, None)
    @py_assert1 = neighbors == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (neighbors, @py_assert2)) % {'py0':@pytest_ar._saferepr(neighbors) if 'neighbors' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(neighbors) else 'neighbors',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = fwd_ss.getStrandIndex
    @py_assert4 = @py_assert1(strand3_fwd)
    @py_assert7 = (
     True, idxs3[0])
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.getStrandIndex\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_fwd) if 'strand3_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_fwd) else 'strand3_fwd',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = fwd_ss.getStrandIndex
    @py_assert4 = @py_assert1(strand2_fwd)
    @py_assert7 = (False, 0)
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.getStrandIndex\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand2_fwd) if 'strand2_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand2_fwd) else 'strand2_fwd',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = fwd_ss.strandCanBeSplit
    @py_assert4 = idxs3[0]
    @py_assert6 = @py_assert1(strand3_fwd, @py_assert4)
    @py_assert9 = False
    @py_assert8 = @py_assert6 is @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.strandCanBeSplit\n}(%(py3)s, %(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_fwd) if 'strand3_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_fwd) else 'strand3_fwd',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = fwd_ss.strandCanBeSplit
    @py_assert4 = idxs3[0]
    @py_assert6 = 1
    @py_assert8 = @py_assert4 + @py_assert6
    @py_assert9 = @py_assert1(strand3_fwd, @py_assert8)
    @py_assert12 = True
    @py_assert11 = @py_assert9 is @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('is', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.strandCanBeSplit\n}(%(py3)s, (%(py5)s + %(py7)s))\n} is %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_fwd) if 'strand3_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_fwd) else 'strand3_fwd',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = fwd_ss.strandCanBeSplit
    @py_assert4 = idxs3[1]
    @py_assert6 = 2
    @py_assert8 = @py_assert4 - @py_assert6
    @py_assert9 = @py_assert1(strand3_fwd, @py_assert8)
    @py_assert12 = True
    @py_assert11 = @py_assert9 is @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('is', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.strandCanBeSplit\n}(%(py3)s, (%(py5)s - %(py7)s))\n} is %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_fwd) if 'strand3_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_fwd) else 'strand3_fwd',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = fwd_ss.strandCanBeSplit
    @py_assert4 = idxs3[1]
    @py_assert6 = 1
    @py_assert8 = @py_assert4 - @py_assert6
    @py_assert9 = @py_assert1(strand3_fwd, @py_assert8)
    @py_assert12 = False
    @py_assert11 = @py_assert9 is @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('is', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.strandCanBeSplit\n}(%(py3)s, (%(py5)s - %(py7)s))\n} is %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_fwd) if 'strand3_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_fwd) else 'strand3_fwd',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = fwd_ss.strandCanBeSplit
    @py_assert4 = idxs3[1]
    @py_assert6 = @py_assert1(strand3_fwd, @py_assert4)
    @py_assert9 = False
    @py_assert8 = @py_assert6 is @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.strandCanBeSplit\n}(%(py3)s, %(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_fwd) if 'strand3_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_fwd) else 'strand3_fwd',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = rev_ss.strandCanBeSplit
    @py_assert4 = idxs3[0]
    @py_assert6 = @py_assert1(strand3_rev, @py_assert4)
    @py_assert9 = False
    @py_assert8 = @py_assert6 is @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.strandCanBeSplit\n}(%(py3)s, %(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(rev_ss) if 'rev_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rev_ss) else 'rev_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_rev) if 'strand3_rev' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_rev) else 'strand3_rev',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = rev_ss.strandCanBeSplit
    @py_assert4 = idxs3[0]
    @py_assert6 = 1
    @py_assert8 = @py_assert4 + @py_assert6
    @py_assert9 = @py_assert1(strand3_rev, @py_assert8)
    @py_assert12 = False
    @py_assert11 = @py_assert9 is @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('is', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.strandCanBeSplit\n}(%(py3)s, (%(py5)s + %(py7)s))\n} is %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(rev_ss) if 'rev_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rev_ss) else 'rev_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_rev) if 'strand3_rev' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_rev) else 'strand3_rev',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = rev_ss.strandCanBeSplit
    @py_assert4 = idxs3[0]
    @py_assert6 = 2
    @py_assert8 = @py_assert4 + @py_assert6
    @py_assert9 = @py_assert1(strand3_rev, @py_assert8)
    @py_assert12 = True
    @py_assert11 = @py_assert9 is @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('is', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.strandCanBeSplit\n}(%(py3)s, (%(py5)s + %(py7)s))\n} is %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(rev_ss) if 'rev_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rev_ss) else 'rev_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_rev) if 'strand3_rev' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_rev) else 'strand3_rev',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = rev_ss.strandCanBeSplit
    @py_assert4 = idxs3[1]
    @py_assert6 = 2
    @py_assert8 = @py_assert4 - @py_assert6
    @py_assert9 = @py_assert1(strand3_rev, @py_assert8)
    @py_assert12 = True
    @py_assert11 = @py_assert9 is @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('is', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.strandCanBeSplit\n}(%(py3)s, (%(py5)s - %(py7)s))\n} is %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(rev_ss) if 'rev_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rev_ss) else 'rev_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_rev) if 'strand3_rev' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_rev) else 'strand3_rev',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = rev_ss.strandCanBeSplit
    @py_assert4 = idxs3[1]
    @py_assert6 = 1
    @py_assert8 = @py_assert4 - @py_assert6
    @py_assert9 = @py_assert1(strand3_rev, @py_assert8)
    @py_assert12 = True
    @py_assert11 = @py_assert9 is @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('is', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.strandCanBeSplit\n}(%(py3)s, (%(py5)s - %(py7)s))\n} is %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(rev_ss) if 'rev_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rev_ss) else 'rev_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_rev) if 'strand3_rev' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_rev) else 'strand3_rev',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = rev_ss.strandCanBeSplit
    @py_assert4 = idxs3[1]
    @py_assert6 = @py_assert1(strand3_rev, @py_assert4)
    @py_assert9 = False
    @py_assert8 = @py_assert6 is @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.strandCanBeSplit\n}(%(py3)s, %(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(rev_ss) if 'rev_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rev_ss) else 'rev_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_rev) if 'strand3_rev' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_rev) else 'strand3_rev',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = fwd_ss.splitStrand
    @py_assert4 = idxs3[0]
    @py_assert6 = @py_assert1(strand3_fwd, @py_assert4)
    @py_assert9 = False
    @py_assert8 = @py_assert6 is @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.splitStrand\n}(%(py3)s, %(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_fwd) if 'strand3_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_fwd) else 'strand3_fwd',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = fwd_ss.splitStrand
    @py_assert4 = idxs3[0]
    @py_assert6 = 1
    @py_assert8 = @py_assert4 + @py_assert6
    @py_assert9 = @py_assert1(strand3_fwd, @py_assert8)
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.splitStrand\n}(%(py3)s, (%(py5)s + %(py7)s))\n}') % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_fwd) if 'strand3_fwd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_fwd) else 'strand3_fwd',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = rev_ss.splitStrand
    @py_assert4 = idxs3[0]
    @py_assert6 = 1
    @py_assert8 = @py_assert4 + @py_assert6
    @py_assert9 = @py_assert1(strand3_rev, @py_assert8)
    @py_assert12 = False
    @py_assert11 = @py_assert9 is @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('is', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.splitStrand\n}(%(py3)s, (%(py5)s + %(py7)s))\n} is %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(rev_ss) if 'rev_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rev_ss) else 'rev_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_rev) if 'strand3_rev' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_rev) else 'strand3_rev',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert1 = rev_ss.splitStrand
    @py_assert4 = idxs3[0]
    @py_assert6 = 2
    @py_assert8 = @py_assert4 + @py_assert6
    @py_assert9 = @py_assert1(strand3_rev, @py_assert8)
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.splitStrand\n}(%(py3)s, (%(py5)s + %(py7)s))\n}') % {'py0':@pytest_ar._saferepr(rev_ss) if 'rev_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rev_ss) else 'rev_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(strand3_rev) if 'strand3_rev' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strand3_rev) else 'strand3_rev',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    overlapping = (fwd_ss.getOverlappingStrands)(*idxs3)
    @py_assert2 = len(overlapping)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(overlapping) if 'overlapping' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(overlapping) else 'overlapping',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = fwd_ss.mergeStrands
    @py_assert4 = @py_assert1(*overlapping)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.mergeStrands\n}(*%(py3)s)\n}') % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(overlapping) if 'overlapping' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(overlapping) else 'overlapping',  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    @py_assert1 = fwd_ss.strandCount
    @py_assert3 = @py_assert1()
    @py_assert6 = 2
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.strandCount\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    fwd_ss.removeAllStrands()
    @py_assert1 = fwd_ss.strandCount
    @py_assert3 = @py_assert1()
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.strandCount\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(fwd_ss) if 'fwd_ss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fwd_ss) else 'fwd_ss',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None