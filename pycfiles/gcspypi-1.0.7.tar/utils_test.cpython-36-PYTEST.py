# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Edd\Workspace\python\ethronsoft\gcspypi\test\utils_test.py
# Compiled at: 2018-07-15 07:17:56
# Size of source mod 2**32: 7556 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from .mocks.mock_repository import MockRepository as Repository
from ethronsoft.gcspypi.exceptions import InvalidParameter
from ethronsoft.gcspypi.package.package import Package
from ethronsoft.gcspypi.utilities import queries as utils
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.package.package_manager import PackageManager
import sys, os, pytest, functools

def test_version_complete():
    @py_assert1 = utils.complete_version
    @py_assert3 = '1'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = '1.0.0'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.complete_version\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = utils.complete_version
    @py_assert3 = '1.1'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = '1.1.0'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.complete_version\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = utils.complete_version
    @py_assert3 = '1.1.1'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = '1.1.1'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.complete_version\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = utils.complete_version
    @py_assert3 = ''
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = '0.0.0'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.complete_version\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    with pytest.raises(InvalidParameter):
        utils.complete_version('1.1.1.1')


def test_version_cmp(data):
    repo = Repository()
    pkg_mgr = PackageManager(repo=repo, installer=None, console=Console(exit_on_error=False))
    for syntax in ('toolkit>=1.0.3', ):
        pkg = pkg_mgr.search(syntax)

    @py_assert1 = utils.pkg_comp_version
    @py_assert3 = '1.05.0'
    @py_assert5 = '1.5.0'
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 0
    @py_assert9 = @py_assert7 < @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('<', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.pkg_comp_version\n}(%(py4)s, %(py6)s)\n} < %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.pkg_comp_version
    @py_assert3 = '1.0.15'
    @py_assert5 = '1.0.2'
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 0
    @py_assert9 = @py_assert7 > @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('>', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.pkg_comp_version\n}(%(py4)s, %(py6)s)\n} > %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.pkg_comp_version
    @py_assert3 = '10.0.0'
    @py_assert5 = '9.999.999'
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 0
    @py_assert9 = @py_assert7 > @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('>', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.pkg_comp_version\n}(%(py4)s, %(py6)s)\n} > %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_cmp_bisect(data):
    for i in range(len(data)):
        @py_assert3 = utils.cmp_bisect
        @py_assert6 = data[i]
        @py_assert9 = utils.pkg_comp_name_version
        @py_assert11 = @py_assert3(data, @py_assert6, @py_assert9)
        @py_assert1 = i == @py_assert11
        if not @py_assert1:
            @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py12)s\n{%(py12)s = %(py4)s\n{%(py4)s = %(py2)s.cmp_bisect\n}(%(py5)s, %(py7)s, %(py10)s\n{%(py10)s = %(py8)s.pkg_comp_name_version\n})\n}',), (i, @py_assert11)) % {'py0':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py2':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
            @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert9 = @py_assert11 = None

    @py_assert0 = 0
    @py_assert4 = utils.cmp_bisect
    @py_assert8 = 'hello1'
    @py_assert10 = '0.0.0'
    @py_assert12 = Package(@py_assert8, @py_assert10)
    @py_assert15 = utils.pkg_comp_name_version
    @py_assert17 = @py_assert4(data, @py_assert12, @py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py5)s\n{%(py5)s = %(py3)s.cmp_bisect\n}(%(py6)s, %(py13)s\n{%(py13)s = %(py7)s(%(py9)s, %(py11)s)\n}, %(py16)s\n{%(py16)s = %(py14)s.pkg_comp_name_version\n})\n}',), (@py_assert0, @py_assert17)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py7':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = None
    @py_assert0 = 2
    @py_assert4 = utils.cmp_bisect
    @py_assert8 = 'hello1'
    @py_assert10 = '0.0.3'
    @py_assert12 = Package(@py_assert8, @py_assert10)
    @py_assert15 = utils.pkg_comp_name_version
    @py_assert17 = @py_assert4(data, @py_assert12, @py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py5)s\n{%(py5)s = %(py3)s.cmp_bisect\n}(%(py6)s, %(py13)s\n{%(py13)s = %(py7)s(%(py9)s, %(py11)s)\n}, %(py16)s\n{%(py16)s = %(py14)s.pkg_comp_name_version\n})\n}',), (@py_assert0, @py_assert17)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py7':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = None
    @py_assert2 = len(data)
    @py_assert6 = utils.cmp_bisect
    @py_assert10 = 'hello3'
    @py_assert12 = '0.0.0'
    @py_assert14 = Package(@py_assert10, @py_assert12)
    @py_assert17 = utils.pkg_comp_name_version
    @py_assert19 = @py_assert6(data, @py_assert14, @py_assert17)
    @py_assert4 = @py_assert2 == @py_assert19
    if not @py_assert4:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py20)s\n{%(py20)s = %(py7)s\n{%(py7)s = %(py5)s.cmp_bisect\n}(%(py8)s, %(py15)s\n{%(py15)s = %(py9)s(%(py11)s, %(py13)s)\n}, %(py18)s\n{%(py18)s = %(py16)s.pkg_comp_name_version\n})\n}',), (@py_assert2, @py_assert19)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py9':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py16':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19)}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert17 = @py_assert19 = None


def test_lower(data):
    @py_assert1 = utils.lower
    @py_assert3 = [
     1, 2]
    @py_assert5 = 0
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.lower\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.lower
    @py_assert3 = [
     1, 2]
    @py_assert5 = 1
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.lower\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.lower
    @py_assert3 = [
     1, 2]
    @py_assert5 = 2
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 1
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.lower\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.lower
    @py_assert3 = [
     1, 2]
    @py_assert5 = 3
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 2
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.lower\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.lower
    @py_assert13 = 'hello1'
    @py_assert15 = '0.0.15'
    @py_assert17 = Package(@py_assert13, @py_assert15)
    @py_assert20 = utils.pkg_comp_name_version
    @py_assert22 = @py_assert9(data, @py_assert17, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.lower\n}(%(py11)s, %(py18)s\n{%(py18)s = %(py12)s(%(py14)s, %(py16)s)\n}, %(py21)s\n{%(py21)s = %(py19)s.pkg_comp_name_version\n})\n}',), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py12':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py19':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert20 = @py_assert22 = None
    @py_assert0 = None
    @py_assert4 = utils.lower
    @py_assert8 = 'hello1'
    @py_assert10 = '0.0.1'
    @py_assert12 = Package(@py_assert8, @py_assert10)
    @py_assert15 = utils.pkg_comp_name_version
    @py_assert17 = @py_assert4(data, @py_assert12, @py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py5)s\n{%(py5)s = %(py3)s.lower\n}(%(py6)s, %(py13)s\n{%(py13)s = %(py7)s(%(py9)s, %(py11)s)\n}, %(py16)s\n{%(py16)s = %(py14)s.pkg_comp_name_version\n})\n}',), (@py_assert0, @py_assert17)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py7':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'hello2'
    @py_assert3 = '0.1.1'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.lower
    @py_assert13 = 'hello3'
    @py_assert15 = '0.0.1'
    @py_assert17 = Package(@py_assert13, @py_assert15)
    @py_assert20 = utils.pkg_comp_name_version
    @py_assert22 = @py_assert9(data, @py_assert17, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.lower\n}(%(py11)s, %(py18)s\n{%(py18)s = %(py12)s(%(py14)s, %(py16)s)\n}, %(py21)s\n{%(py21)s = %(py19)s.pkg_comp_name_version\n})\n}',), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py12':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py19':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert20 = @py_assert22 = None


def test_floor(data):
    @py_assert1 = utils.floor
    @py_assert3 = [
     1, 2, 3]
    @py_assert5 = 1
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 1
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.floor\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.floor
    @py_assert3 = [
     1, 2, 3]
    @py_assert5 = 2
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 2
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.floor\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.floor
    @py_assert3 = [
     1, 2, 3]
    @py_assert5 = 0
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.floor\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.floor
    @py_assert3 = [
     1, 2, 3]
    @py_assert5 = 4
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 3
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.floor\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.floor
    @py_assert3 = [
     1, 2, 3, 5]
    @py_assert5 = 4
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 3
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.floor\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.1'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.floor
    @py_assert13 = 'hello1'
    @py_assert15 = '0.0.1'
    @py_assert17 = Package(@py_assert13, @py_assert15)
    @py_assert20 = utils.pkg_comp_name_version
    @py_assert22 = @py_assert9(data, @py_assert17, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.floor\n}(%(py11)s, %(py18)s\n{%(py18)s = %(py12)s(%(py14)s, %(py16)s)\n}, %(py21)s\n{%(py21)s = %(py19)s.pkg_comp_name_version\n})\n}',), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py12':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py19':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert20 = @py_assert22 = None
    @py_assert0 = None
    @py_assert4 = utils.floor
    @py_assert8 = 'hello1'
    @py_assert10 = '0.0.05'
    @py_assert12 = Package(@py_assert8, @py_assert10)
    @py_assert15 = utils.pkg_comp_name_version
    @py_assert17 = @py_assert4(data, @py_assert12, @py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py5)s\n{%(py5)s = %(py3)s.floor\n}(%(py6)s, %(py13)s\n{%(py13)s = %(py7)s(%(py9)s, %(py11)s)\n}, %(py16)s\n{%(py16)s = %(py14)s.pkg_comp_name_version\n})\n}',), (@py_assert0, @py_assert17)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py7':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.lower
    @py_assert13 = 'hello1'
    @py_assert15 = '0.0.3'
    @py_assert17 = Package(@py_assert13, @py_assert15)
    @py_assert20 = utils.pkg_comp_name_version
    @py_assert22 = @py_assert9(data, @py_assert17, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.lower\n}(%(py11)s, %(py18)s\n{%(py18)s = %(py12)s(%(py14)s, %(py16)s)\n}, %(py21)s\n{%(py21)s = %(py19)s.pkg_comp_name_version\n})\n}',), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py12':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py19':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert20 = @py_assert22 = None


def test_higher(data):
    @py_assert1 = utils.higher
    @py_assert3 = [
     1, 2]
    @py_assert5 = 0
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 1
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.higher\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.higher
    @py_assert3 = [
     1, 2]
    @py_assert5 = 1
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 2
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.higher\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.higher
    @py_assert3 = [
     1, 2]
    @py_assert5 = 2
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.higher\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.higher
    @py_assert3 = [
     1, 2]
    @py_assert5 = 3
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.higher\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.1'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.higher
    @py_assert13 = 'hello1'
    @py_assert15 = '0.0.0'
    @py_assert17 = Package(@py_assert13, @py_assert15)
    @py_assert20 = utils.pkg_comp_name_version
    @py_assert22 = @py_assert9(data, @py_assert17, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.higher\n}(%(py11)s, %(py18)s\n{%(py18)s = %(py12)s(%(py14)s, %(py16)s)\n}, %(py21)s\n{%(py21)s = %(py19)s.pkg_comp_name_version\n})\n}',), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py12':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py19':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert20 = @py_assert22 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.1.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.higher
    @py_assert13 = 'hello1'
    @py_assert15 = '0.0.3'
    @py_assert17 = Package(@py_assert13, @py_assert15)
    @py_assert20 = utils.pkg_comp_name_version
    @py_assert22 = @py_assert9(data, @py_assert17, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.higher\n}(%(py11)s, %(py18)s\n{%(py18)s = %(py12)s(%(py14)s, %(py16)s)\n}, %(py21)s\n{%(py21)s = %(py19)s.pkg_comp_name_version\n})\n}',), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py12':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py19':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert20 = @py_assert22 = None
    @py_assert0 = None
    @py_assert4 = utils.higher
    @py_assert8 = 'hello2'
    @py_assert10 = '0.1.1'
    @py_assert12 = Package(@py_assert8, @py_assert10)
    @py_assert15 = utils.pkg_comp_name_version
    @py_assert17 = @py_assert4(data, @py_assert12, @py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py5)s\n{%(py5)s = %(py3)s.higher\n}(%(py6)s, %(py13)s\n{%(py13)s = %(py7)s(%(py9)s, %(py11)s)\n}, %(py16)s\n{%(py16)s = %(py14)s.pkg_comp_name_version\n})\n}',), (@py_assert0, @py_assert17)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py7':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = None


def test_ceiling(data):
    @py_assert1 = utils.ceiling
    @py_assert3 = [
     1, 2]
    @py_assert5 = 0
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 1
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.ceiling\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.ceiling
    @py_assert3 = [
     1, 2]
    @py_assert5 = 1
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 1
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.ceiling\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.ceiling
    @py_assert3 = [
     1, 2]
    @py_assert5 = 2
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 2
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.ceiling\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.ceiling
    @py_assert3 = [
     1, 2]
    @py_assert5 = 3
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = None
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.ceiling\n}(%(py4)s, %(py6)s)\n} == %(py11)s',), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = utils.ceiling
    @py_assert3 = []
    @py_assert5 = 1
    @py_assert7 = -@py_assert5
    @py_assert8 = @py_assert1(@py_assert3, @py_assert7)
    @py_assert11 = None
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.ceiling\n}(%(py4)s, -%(py6)s)\n} == %(py12)s',), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.1'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.ceiling
    @py_assert13 = 'hello1'
    @py_assert15 = '0.0.0'
    @py_assert17 = Package(@py_assert13, @py_assert15)
    @py_assert20 = utils.pkg_comp_name_version
    @py_assert22 = @py_assert9(data, @py_assert17, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.ceiling\n}(%(py11)s, %(py18)s\n{%(py18)s = %(py12)s(%(py14)s, %(py16)s)\n}, %(py21)s\n{%(py21)s = %(py19)s.pkg_comp_name_version\n})\n}',), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py12':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py19':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert20 = @py_assert22 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.1'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.ceiling
    @py_assert13 = 'hello1'
    @py_assert15 = '0.0.1'
    @py_assert17 = Package(@py_assert13, @py_assert15)
    @py_assert20 = utils.pkg_comp_name_version
    @py_assert22 = @py_assert9(data, @py_assert17, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.ceiling\n}(%(py11)s, %(py18)s\n{%(py18)s = %(py12)s(%(py14)s, %(py16)s)\n}, %(py21)s\n{%(py21)s = %(py19)s.pkg_comp_name_version\n})\n}',), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py12':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py19':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert20 = @py_assert22 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.1.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.ceiling
    @py_assert13 = 'hello1'
    @py_assert15 = '0.0.3'
    @py_assert17 = Package(@py_assert13, @py_assert15)
    @py_assert20 = utils.pkg_comp_name_version
    @py_assert22 = @py_assert9(data, @py_assert17, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.ceiling\n}(%(py11)s, %(py18)s\n{%(py18)s = %(py12)s(%(py14)s, %(py16)s)\n}, %(py21)s\n{%(py21)s = %(py19)s.pkg_comp_name_version\n})\n}',), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py12':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py19':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = ('' + 'assert %(py25)s') % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert20 = @py_assert22 = None
    @py_assert0 = None
    @py_assert4 = utils.ceiling
    @py_assert8 = 'hello3'
    @py_assert10 = '0.0.3'
    @py_assert12 = Package(@py_assert8, @py_assert10)
    @py_assert15 = utils.pkg_comp_name_version
    @py_assert17 = @py_assert4(data, @py_assert12, @py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py5)s\n{%(py5)s = %(py3)s.ceiling\n}(%(py6)s, %(py13)s\n{%(py13)s = %(py7)s(%(py9)s, %(py11)s)\n}, %(py16)s\n{%(py16)s = %(py14)s.pkg_comp_name_version\n})\n}',), (@py_assert0, @py_assert17)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py7':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py14':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert15 = @py_assert17 = None


def test_range_query(data):
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '>'
    @py_assert16 = '0.0.1'
    @py_assert18 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16)
    @py_assert7 = @py_assert5 == @py_assert18
    if not @py_assert7:
        @py_format20 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py19)s\n{%(py19)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s)\n}', ), (@py_assert5, @py_assert18)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert0 = None
    @py_assert4 = utils.pkg_range_query
    @py_assert7 = 'hello1'
    @py_assert9 = '>'
    @py_assert11 = ''
    @py_assert13 = @py_assert4(data, @py_assert7, @py_assert9, @py_assert11)
    @py_assert2 = @py_assert0 == @py_assert13
    if not @py_assert2:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py14)s\n{%(py14)s = %(py5)s\n{%(py5)s = %(py3)s.pkg_range_query\n}(%(py6)s, %(py8)s, %(py10)s, %(py12)s)\n}', ), (@py_assert0, @py_assert13)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '<='
    @py_assert16 = '0.0.2'
    @py_assert18 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16)
    @py_assert7 = @py_assert5 == @py_assert18
    if not @py_assert7:
        @py_format20 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py19)s\n{%(py19)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s)\n}', ), (@py_assert5, @py_assert18)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.1.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '<='
    @py_assert16 = ''
    @py_assert18 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16)
    @py_assert7 = @py_assert5 == @py_assert18
    if not @py_assert7:
        @py_format20 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py19)s\n{%(py19)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s)\n}', ), (@py_assert5, @py_assert18)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.1.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '>='
    @py_assert16 = ''
    @py_assert18 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16)
    @py_assert7 = @py_assert5 == @py_assert18
    if not @py_assert7:
        @py_format20 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py19)s\n{%(py19)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s)\n}', ), (@py_assert5, @py_assert18)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '=='
    @py_assert16 = '0.0.2'
    @py_assert18 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16)
    @py_assert7 = @py_assert5 == @py_assert18
    if not @py_assert7:
        @py_format20 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py19)s\n{%(py19)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s)\n}', ), (@py_assert5, @py_assert18)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.1'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '<'
    @py_assert16 = '0.0.2'
    @py_assert18 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16)
    @py_assert7 = @py_assert5 == @py_assert18
    if not @py_assert7:
        @py_format20 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py19)s\n{%(py19)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s)\n}', ), (@py_assert5, @py_assert18)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '<'
    @py_assert16 = ''
    @py_assert18 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16)
    @py_assert7 = @py_assert5 == @py_assert18
    if not @py_assert7:
        @py_format20 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py19)s\n{%(py19)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s)\n}', ), (@py_assert5, @py_assert18)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18)}
        @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert0 = None
    @py_assert4 = utils.pkg_range_query
    @py_assert7 = 'hello1'
    @py_assert9 = '>'
    @py_assert11 = '1.1.2'
    @py_assert13 = @py_assert4(data, @py_assert7, @py_assert9, @py_assert11)
    @py_assert2 = @py_assert0 == @py_assert13
    if not @py_assert2:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py14)s\n{%(py14)s = %(py5)s\n{%(py5)s = %(py3)s.pkg_range_query\n}(%(py6)s, %(py8)s, %(py10)s, %(py12)s)\n}', ), (@py_assert0, @py_assert13)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.1.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = @py_assert9(data, @py_assert12)
    @py_assert7 = @py_assert5 == @py_assert14
    if not @py_assert7:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py15)s\n{%(py15)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s)\n}', ), (@py_assert5, @py_assert14)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '<'
    @py_assert16 = @py_assert9(data, @py_assert12, @py_assert14)
    @py_assert7 = @py_assert5 == @py_assert16
    if not @py_assert7:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py17)s\n{%(py17)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s)\n}', ), (@py_assert5, @py_assert16)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '>'
    @py_assert16 = '0.0.1'
    @py_assert18 = '<='
    @py_assert20 = '0.0.2'
    @py_assert22 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16, @py_assert18, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s, %(py19)s, %(py21)s)\n}', ), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18),  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert22 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '>'
    @py_assert16 = '0.0.1'
    @py_assert18 = '=='
    @py_assert20 = '0.0.2'
    @py_assert22 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16, @py_assert18, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s, %(py19)s, %(py21)s)\n}', ), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18),  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert22 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '<'
    @py_assert16 = '0.1.2'
    @py_assert18 = '>'
    @py_assert20 = '0.0.1'
    @py_assert22 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16, @py_assert18, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s, %(py19)s, %(py21)s)\n}', ), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18),  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert22 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.2'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '<'
    @py_assert16 = '0.1.2'
    @py_assert18 = '>='
    @py_assert20 = '0.0.2'
    @py_assert22 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16, @py_assert18, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s, %(py19)s, %(py21)s)\n}', ), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18),  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert22 = None
    @py_assert0 = None
    @py_assert4 = utils.pkg_range_query
    @py_assert7 = 'hello1'
    @py_assert9 = '>'
    @py_assert11 = '0.0.1'
    @py_assert13 = '<'
    @py_assert15 = '0.0.2'
    @py_assert17 = @py_assert4(data, @py_assert7, @py_assert9, @py_assert11, @py_assert13, @py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py5)s\n{%(py5)s = %(py3)s.pkg_range_query\n}(%(py6)s, %(py8)s, %(py10)s, %(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert0, @py_assert17)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert1 = 'hello1'
    @py_assert3 = '0.0.1'
    @py_assert5 = Package(@py_assert1, @py_assert3)
    @py_assert9 = utils.pkg_range_query
    @py_assert12 = 'hello1'
    @py_assert14 = '>='
    @py_assert16 = '0.0.1'
    @py_assert18 = '<'
    @py_assert20 = '0.0.2'
    @py_assert22 = @py_assert9(data, @py_assert12, @py_assert14, @py_assert16, @py_assert18, @py_assert20)
    @py_assert7 = @py_assert5 == @py_assert22
    if not @py_assert7:
        @py_format24 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py23)s\n{%(py23)s = %(py10)s\n{%(py10)s = %(py8)s.pkg_range_query\n}(%(py11)s, %(py13)s, %(py15)s, %(py17)s, %(py19)s, %(py21)s)\n}', ), (@py_assert5, @py_assert22)) % {'py0':@pytest_ar._saferepr(Package) if 'Package' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Package) else 'Package',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18),  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert22 = None
    @py_assert0 = None
    @py_assert4 = utils.pkg_range_query
    @py_assert7 = 'hello1'
    @py_assert9 = '>'
    @py_assert11 = '0.0.1'
    @py_assert13 = '<'
    @py_assert15 = '0.0.1'
    @py_assert17 = @py_assert4(data, @py_assert7, @py_assert9, @py_assert11, @py_assert13, @py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py5)s\n{%(py5)s = %(py3)s.pkg_range_query\n}(%(py6)s, %(py8)s, %(py10)s, %(py12)s, %(py14)s, %(py16)s)\n}', ), (@py_assert0, @py_assert17)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    with pytest.raises(InvalidParameter):
        utils.pkg_range_query(data, 'hello1', 'wrong-op')
    with pytest.raises(InvalidParameter):
        utils.pkg_range_query(data, 'hello1', '>', '0.0.1', 'wrong-op', '0.0.2')


def test_get_type():
    @py_assert1 = utils.get_package_type
    @py_assert3 = 'something.zip'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'SOURCE'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_package_type\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = utils.get_package_type
    @py_assert3 = 'something.tar'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'SOURCE'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_package_type\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = utils.get_package_type
    @py_assert3 = 'something.tar.gz'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'SOURCE'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_package_type\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = utils.get_package_type
    @py_assert3 = 'something.whl'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'WHEEL'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_package_type\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    with pytest.raises(InvalidParameter):
        utils.get_package_type('wrong')


def test_version_sorting():
    versions = [
     '1.0.0',
     '1.0.05',
     '0.1.0',
     '1.1.1',
     '0.0.1',
     '1.01.1']
    versions.sort(key=(functools.cmp_to_key(utils.pkg_comp_version)))
    @py_assert2 = ['0.0.1', '0.1.0', '1.0.0', '1.0.05', '1.01.1', '1.1.1']
    @py_assert1 = versions == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (versions, @py_assert2)) % {'py0':@pytest_ar._saferepr(versions) if 'versions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(versions) else 'versions',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_items_to_package():
    items = [
     'some/1.1.0/filename.zip',
     'some/1.1.0/filename.zip',
     'some/1.0.0/filename.zip',
     'some/2.0.0/filename.zip',
     'other/3.0.0/filename.zip',
     'other/1.0.0/filename.zip']
    @py_assert0 = [p.full_name for p in utils.items_to_package(items, unique=False)]
    @py_assert3 = [
     'other:1.0.0', 'other:3.0.0', 'some:1.0.0', 'some:1.1.0', 'some:1.1.0', 'some:2.0.0']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = [p.full_name for p in utils.items_to_package(items, unique=True)]
    @py_assert3 = [
     'other:1.0.0', 'other:3.0.0', 'some:1.0.0', 'some:1.1.0', 'some:2.0.0']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


@pytest.fixture
def data():
    return [
     Package('hello1', '0.0.1'),
     Package('hello1', '0.0.2'),
     Package('hello1', '0.1.2'),
     Package('hello2', '0.1.0'),
     Package('hello2', '0.1.1')]