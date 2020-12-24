# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Edd\Workspace\python\ethronsoft\gcspypi\test\repository_test.py
# Compiled at: 2018-07-15 07:17:56
# Size of source mod 2**32: 1324 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from .mocks.mock_repository import MockRepository as Repository
import six, time
from io import BytesIO

def test_content():
    repo = Repository()
    repo.upload_content('object/x', 'hello world')
    @py_assert1 = repo.exists
    @py_assert3 = 'object/x'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}(%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(repo) if 'repo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo) else 'repo',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = repo.download_content
    @py_assert3 = 'object/x'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'hello world'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.download_content\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(repo) if 'repo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo) else 'repo',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_file():
    repo = Repository()
    io = BytesIO('hello world'.encode('utf-8'))
    repo.upload_file('object/x', io)
    @py_assert1 = repo.exists
    @py_assert3 = 'object/x'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}(%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(repo) if 'repo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo) else 'repo',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = repo.download_content
    @py_assert3 = 'object/x'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5.decode
    @py_assert9 = 'utf-8'
    @py_assert11 = @py_assert7(@py_assert9)
    @py_assert14 = 'hello world'
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.download_content\n}(%(py4)s)\n}.decode\n}(%(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(repo) if 'repo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo) else 'repo',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


def test_list():
    repo = Repository()
    repo.upload_content('object/x/y', 'hello world')
    repo.upload_content('object/x/z', 'hello world')
    @py_assert2 = repo.list
    @py_assert4 = 'object/x'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = len(@py_assert6)
    @py_assert11 = 2
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.list\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(repo) if 'repo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo) else 'repo',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert2 = repo.list
    @py_assert4 = 'object/x/y'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = len(@py_assert6)
    @py_assert11 = 1
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.list\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(repo) if 'repo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo) else 'repo',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert2 = repo.list
    @py_assert4 = 'object/x/z'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = len(@py_assert6)
    @py_assert11 = 1
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.list\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(repo) if 'repo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo) else 'repo',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert2 = repo.list
    @py_assert4 = 'object/x/w'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = len(@py_assert6)
    @py_assert11 = 0
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.list\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(repo) if 'repo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repo) else 'repo',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_metadata():
    repo = Repository()
    repo.upload_content('object/x', 'hello world')
    time.sleep(0.01)
    repo.upload_content('object/y', 'hello world')
    xm = repo.metadata('object/x')
    ym = repo.metadata('object/y')
    @py_assert1 = xm.md5
    @py_assert5 = ym.md5
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.md5\n} == %(py6)s\n{%(py6)s = %(py4)s.md5\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(xm) if 'xm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(xm) else 'xm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(ym) if 'ym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ym) else 'ym',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = xm.time_created
    @py_assert5 = ym.time_created
    @py_assert3 = @py_assert1 < @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('<', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.time_created\n} < %(py6)s\n{%(py6)s = %(py4)s.time_created\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(xm) if 'xm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(xm) else 'xm',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(ym) if 'ym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ym) else 'ym',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None