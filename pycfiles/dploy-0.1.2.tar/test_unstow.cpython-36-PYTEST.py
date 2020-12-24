# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/arecarn/Dropbox/projects/dploy/master/tests/test_unstow.py
# Compiled at: 2017-10-27 00:13:46
# Size of source mod 2**32: 8017 bytes
"""
Tests for the stow stub command
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, pytest, dploy
from dploy import error
import utils
SUBCMD = 'unstow'

def test_unstow_with_basic_senario(source_a, dest):
    dploy.stow([source_a], dest)
    dploy.unstow([source_a], dest)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'aaa'
    @py_assert13 = @py_assert8(dest, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    @py_assert17 = not @py_assert15
    if not @py_assert17:
        @py_format18 = ('' + 'assert not %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None


def test_unstow_dwith_basic_senario_doesnt_delete_dest_directory(source_a, dest):
    dploy.stow([source_a], dest)
    dploy.unstow([source_a], dest)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = @py_assert3(dest)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_unstow_with_a_broken_link_dest(source_a, dest):
    conflicting_link = os.path.join(dest, 'aaa')
    source_file = os.path.join(source_a, 'aaa')
    os.symlink('non_existant_source', os.path.join(dest, 'aaa'))
    with pytest.raises(ValueError) as (e):
        dploy.unstow([source_a], dest)
    @py_assert1 = error.ConflictsWithExistingLink
    @py_assert6 = @py_assert1(subcmd=SUBCMD, source=source_file, dest=conflicting_link)
    @py_assert8 = @py_assert6.msg
    @py_assert13 = e.value
    @py_assert15 = str(@py_assert13)
    @py_assert10 = @py_assert8 in @py_assert15
    if not @py_assert10:
        @py_format17 = @pytest_ar._call_reprcompare(('in',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.ConflictsWithExistingLink\n}(subcmd=%(py3)s, source=%(py4)s, dest=%(py5)s)\n}.msg\n} in %(py16)s\n{%(py16)s = %(py11)s(%(py14)s\n{%(py14)s = %(py12)s.value\n})\n}',), (@py_assert8, @py_assert15)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(source_file) if 'source_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source_file) else 'source_file',  'py5':@pytest_ar._saferepr(conflicting_link) if 'conflicting_link' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conflicting_link) else 'conflicting_link',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py12':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert13 = @py_assert15 = None


def test_unstow_with_broken_link_in_dest(source_a, dest):
    os.mkdir(os.path.join(dest, 'aaa'))
    dploy.stow([source_a], dest)
    os.symlink(os.path.join(source_a, 'non_existant_source'), os.path.join(dest, 'aaa', 'non_existant_source'))
    dploy.unstow([source_a], dest)


def test_unstow_with_non_existant_source(dest):
    source = 'source'
    with pytest.raises(NotADirectoryError) as (e):
        dploy.unstow([source], dest)
    @py_assert1 = error.NoSuchDirectory
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=source)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.NoSuchDirectory\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(source) if 'source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source) else 'source',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_unstow_with_duplicate_source(source_a, dest):
    dploy.stow([source_a], dest)
    with pytest.raises(ValueError) as (e):
        dploy.unstow([source_a, source_a], dest)
    @py_assert1 = error.DuplicateSource
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=source_a)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.DuplicateSource\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(source_a) if 'source_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source_a) else 'source_a',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_unstow_with_non_existant_dest(source_a):
    dest = 'dest'
    with pytest.raises(NotADirectoryError) as (e):
        dploy.unstow([source_a], dest)
    @py_assert1 = error.NoSuchDirectoryToSubcmdInto
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=dest)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.NoSuchDirectoryToSubcmdInto\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_unstow_with_file_as_source(file_a, dest):
    with pytest.raises(NotADirectoryError) as (e):
        dploy.unstow([file_a], dest)
    @py_assert1 = error.NoSuchDirectory
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=file_a)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.NoSuchDirectory\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(file_a) if 'file_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_a) else 'file_a',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_unstow_with_file_as_dest(source_a, file_a):
    with pytest.raises(NotADirectoryError) as (e):
        dploy.unstow([source_a], file_a)
    @py_assert1 = error.NoSuchDirectoryToSubcmdInto
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=file_a)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.NoSuchDirectoryToSubcmdInto\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(file_a) if 'file_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_a) else 'file_a',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_unstow_with_file_as_source_and_dest(file_a, file_b):
    with pytest.raises(NotADirectoryError) as (e):
        dploy.unstow([file_a], file_b)
    @py_assert1 = error.NoSuchDirectoryToSubcmdInto
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=file_b)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.NoSuchDirectoryToSubcmdInto\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(file_b) if 'file_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_b) else 'file_b',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_unstow_with_read_only_dest(source_a, dest):
    dploy.stow([source_a], dest)
    utils.remove_write_permission(dest)
    with pytest.raises(PermissionError) as (e):
        dploy.unstow([source_a], dest)
    @py_assert1 = error.InsufficientPermissionsToSubcmdTo
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=dest)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.InsufficientPermissionsToSubcmdTo\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_unstow_with_read_only_dest_file(source_a, dest):
    dploy.stow([source_a], dest)
    utils.remove_write_permission(os.path.join(dest, 'aaa'))
    dploy.unstow([source_a], dest)


def test_unstow_with_write_only_source(source_a, dest):
    dploy.stow([source_a], dest)
    utils.remove_read_permission(source_a)
    with pytest.raises(PermissionError) as (e):
        dploy.unstow([source_a], dest)
    @py_assert1 = error.InsufficientPermissionsToSubcmdFrom
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=source_a)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.InsufficientPermissionsToSubcmdFrom\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(source_a) if 'source_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source_a) else 'source_a',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_unstow_with_dest_with_no_executue_permissions(source_a, dest):
    dploy.stow([source_a], dest)
    utils.remove_execute_permission(dest)
    with pytest.raises(PermissionError) as (e):
        dploy.unstow([source_a], dest)
    @py_assert1 = error.InsufficientPermissionsToSubcmdTo
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=dest)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.InsufficientPermissionsToSubcmdTo\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_unstow_with_dest_dir_with_no_executue_permissions(source_a, source_b, dest):
    dest_dir = os.path.join(dest, 'aaa')
    dploy.stow([source_a, source_b], dest)
    utils.remove_execute_permission(os.path.join(dest, 'aaa'))
    with pytest.raises(PermissionError) as (e):
        dploy.unstow([source_a, source_b], dest)
    @py_assert1 = error.InsufficientPermissionsToSubcmdTo
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=dest_dir)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.InsufficientPermissionsToSubcmdTo\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(dest_dir) if 'dest_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest_dir) else 'dest_dir',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_unstow_with_write_only_source_file(source_a, dest):
    dploy.stow([source_a], dest)
    utils.remove_read_permission(os.path.join(source_a, 'aaa', 'aaa'))
    dploy.unstow([source_a], dest)


def test_unstow_with_write_only_dest_file(source_a, dest):
    dploy.stow([source_a], dest)
    utils.remove_read_permission(os.path.join(dest, 'aaa'))
    dploy.unstow([source_a], dest)


def test_unstow_with_same_directory_used_as_source_and_dest(source_a):
    with pytest.raises(ValueError) as (e):
        dploy.unstow([source_a], source_a)
    @py_assert1 = utils.is_subcmd_error_message
    @py_assert3 = 'unstow'
    @py_assert6 = @py_assert1(@py_assert3, e)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.is_subcmd_error_message\n}(%(py4)s, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_unstow_with_same_simple_directory_used_as_source_and_dest(source_only_files):
    with pytest.raises(ValueError) as (e):
        dploy.unstow([source_only_files], source_only_files)
    @py_assert1 = error.SourceIsSameAsDest
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=source_only_files)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.SourceIsSameAsDest\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(source_only_files) if 'source_only_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source_only_files) else 'source_only_files',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_unstow_folding_basic(source_a, source_b, dest):
    dploy.stow([source_a, source_b], dest)
    dploy.unstow([source_b], dest)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.islink
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'aaa'
    @py_assert13 = @py_assert8(dest, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    if not @py_assert15:
        @py_format17 = ('' + 'assert %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.islink\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_unstow_folding_with_multiple_sources(source_a, source_b, source_d, dest):
    dploy.stow([source_a, source_b, source_d], dest)
    dploy.unstow([source_b, source_d], dest)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.islink
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'aaa'
    @py_assert13 = @py_assert8(dest, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    if not @py_assert15:
        @py_format17 = ('' + 'assert %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.islink\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_unstow_folding_with_stray_symlink_in_unfolded_dest_dir(source_a, source_b, source_d, dest):
    """
    Given a dest directory with stowed packages that share a unfolded directory,
    that also contains a stray link along with the links created by stowing.

    When the stowed packages are unstowed

    Then the folded directory remains with the single stray symlink
    """
    stray_path = os.path.join(dest, 'aaa', 'ggg')
    dploy.stow([source_a, source_b], dest)
    dploy.link(os.path.join(source_d, 'aaa', 'ggg'), stray_path)
    dploy.unstow([source_a, source_b], dest)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.islink
    @py_assert6 = @py_assert3(stray_path)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.islink\n}(%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(stray_path) if 'stray_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stray_path) else 'stray_path',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_unstow_folding_with_multiple_stowed_sources(source_a, source_b, source_d, dest):
    dploy.stow([source_a, source_b, source_d], dest)
    dploy.unstow([source_b], dest)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.islink
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'aaa'
    @py_assert13 = @py_assert8(dest, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    @py_assert17 = not @py_assert15
    if not @py_assert17:
        @py_format18 = ('' + 'assert not %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.islink\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None


def test_unstow_folding_with_multiple_sources_all_unstowed(source_a, source_b, dest):
    dploy.stow([source_a, source_b], dest, is_silent=False)
    dploy.unstow([source_a, source_b], dest, is_silent=False)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'aaa'
    @py_assert13 = @py_assert8(dest, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    @py_assert17 = not @py_assert15
    if not @py_assert17:
        @py_format18 = ('' + 'assert not %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None


def test_unstow_folding_with_existing_file_in_dest(source_a, source_b, dest):
    os.mkdir(os.path.join(dest, 'aaa'))
    a_file = os.path.join(dest, 'aaa', 'a_file')
    utils.create_file(a_file)
    dploy.stow([source_a, source_b], dest)
    dploy.unstow([source_a], dest)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = @py_assert3(a_file)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py5)s)\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(a_file) if 'a_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a_file) else 'a_file',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_unstow_folding_with_multiple_sources_with_execute_permission_unset(source_a, source_b, dest):
    dploy.stow([source_a, source_b], dest)
    utils.remove_execute_permission(source_b)
    with pytest.raises(PermissionError) as (e):
        dploy.unstow([source_a], dest)
    dest_dir = os.path.join(dest, 'aaa', 'ddd')
    @py_assert1 = error.PermissionDenied
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=dest_dir)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.PermissionDenied\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(dest_dir) if 'dest_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest_dir) else 'dest_dir',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None