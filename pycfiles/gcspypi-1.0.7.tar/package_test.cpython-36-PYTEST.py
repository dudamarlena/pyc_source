# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Edd\Workspace\python\ethronsoft\gcspypi\test\package_test.py
# Compiled at: 2018-07-15 07:17:56
# Size of source mod 2**32: 1528 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from ethronsoft.gcspypi.package.package import Package
from ethronsoft.gcspypi.exceptions import InvalidParameter, InvalidState
import pytest

def test_repo_name():
    p = Package('some', '1.0.0')
    @py_assert1 = p.full_name
    @py_assert4 = 'some:1.0.0'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.full_name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    wrong = Package('some', '')
    @py_assert1 = Package.repo_name
    @py_assert4 = '/some/filename.txt'
    @py_assert6 = @py_assert1(p, @py_assert4)
    @py_assert9 = 'some/1.0.0/filename.txt'
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.repo_name\n}(%(py3)s, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    with pytest.raises(InvalidState):
        Package.repo_name(wrong, '/some/filename.txt')


def test_equality():
    p1 = Package('some', '1.0.0', type='A')
    p2 = Package('some', '1.0.0', type='A')
    p3 = Package('some', '1.0.0', type='B')
    p4 = Package('some', '', type='A')
    p5 = Package('other', '1.0.0', type='A')
    p6 = Package('other', '1.0.0', type='B')
    @py_assert1 = p1.full_name
    @py_assert6 = str(p1)
    @py_assert3 = @py_assert1 == @py_assert6
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.full_name\n} == %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}', ), (@py_assert1, @py_assert6)) % {'py0':@pytest_ar._saferepr(p1) if 'p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p1) else 'p1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py5':@pytest_ar._saferepr(p1) if 'p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p1) else 'p1',  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = p1 == p2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (p1, p2)) % {'py0':@pytest_ar._saferepr(p1) if 'p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p1) else 'p1',  'py2':@pytest_ar._saferepr(p2) if 'p2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p2) else 'p2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert2 = hash(p1)
    @py_assert7 = hash(p2)
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(p1) if 'p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p1) else 'p1',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py6':@pytest_ar._saferepr(p2) if 'p2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p2) else 'p2',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert1 = p1 != p3
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != %(py2)s', ), (p1, p3)) % {'py0':@pytest_ar._saferepr(p1) if 'p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p1) else 'p1',  'py2':@pytest_ar._saferepr(p3) if 'p3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p3) else 'p3'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert2 = hash(p1)
    @py_assert7 = hash(p3)
    @py_assert4 = @py_assert2 != @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} != %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py1':@pytest_ar._saferepr(p1) if 'p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p1) else 'p1',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(hash) if 'hash' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hash) else 'hash',  'py6':@pytest_ar._saferepr(p3) if 'p3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p3) else 'p3',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert1 = p1 != p4
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != %(py2)s', ), (p1, p4)) % {'py0':@pytest_ar._saferepr(p1) if 'p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p1) else 'p1',  'py2':@pytest_ar._saferepr(p4) if 'p4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p4) else 'p4'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = p2 != p5
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != %(py2)s', ), (p2, p5)) % {'py0':@pytest_ar._saferepr(p2) if 'p2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p2) else 'p2',  'py2':@pytest_ar._saferepr(p5) if 'p5' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p5) else 'p5'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = p5 != p6
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != %(py2)s', ), (p5, p6)) % {'py0':@pytest_ar._saferepr(p5) if 'p5' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p5) else 'p5',  'py2':@pytest_ar._saferepr(p6) if 'p6' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p6) else 'p6'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_from_text():
    with pytest.raises(InvalidParameter):
        Package.from_text('some>1.0.0')
    with pytest.raises(InvalidParameter):
        Package.from_text('some<1.0.0')
    with pytest.raises(InvalidParameter):
        Package.from_text('some<=1.0.0')
    with pytest.raises(InvalidParameter):
        Package.from_text('some>=1.0.0')
    @py_assert1 = Package.from_text
    @py_assert3 = 'some==1.0.0'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = 'some'
    @py_assert11 = '1.0.0'
    @py_assert13 = Package(@py_assert9, @py_assert11)
    @py_assert7 = @py_assert5 == @py_assert13
    if not @py_assert7:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_text\n}(%(py4)s)\n} == %(py14)s\n{%(py14)s = %(py8)s(%(py10)s, %(py12)s)\n}', ), (@py_assert5, @py_assert13)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = Package.from_text
    @py_assert3 = 'some=='
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = 'some'
    @py_assert11 = ''
    @py_assert13 = Package(@py_assert9, @py_assert11)
    @py_assert7 = @py_assert5 == @py_assert13
    if not @py_assert7:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_text\n}(%(py4)s)\n} == %(py14)s\n{%(py14)s = %(py8)s(%(py10)s, %(py12)s)\n}', ), (@py_assert5, @py_assert13)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = Package.from_text
    @py_assert3 = 'some'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = 'some'
    @py_assert11 = ''
    @py_assert13 = Package(@py_assert9, @py_assert11)
    @py_assert7 = @py_assert5 == @py_assert13
    if not @py_assert7:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.from_text\n}(%(py4)s)\n} == %(py14)s\n{%(py14)s = %(py8)s(%(py10)s, %(py12)s)\n}', ), (@py_assert5, @py_assert13)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None