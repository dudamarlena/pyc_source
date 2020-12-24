# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/arecarn/Dropbox/projects/dploy/master/tests/test_stow.py
# Compiled at: 2017-10-27 00:13:45
# Size of source mod 2**32: 8526 bytes
"""
Tests for the stow stub command
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, pytest, dploy
from dploy import error
import utils
SUBCMD = 'stow'

def test_stow_with_simple_senario(source_only_files, dest):
    dploy.stow([source_only_files], dest)
    @py_assert1 = os.readlink
    @py_assert4 = os.path
    @py_assert6 = @py_assert4.join
    @py_assert9 = 'aaa'
    @py_assert11 = @py_assert6(dest, @py_assert9)
    @py_assert13 = @py_assert1(@py_assert11)
    @py_assert17 = os.path
    @py_assert19 = @py_assert17.join
    @py_assert21 = '..'
    @py_assert23 = 'source_only_files'
    @py_assert25 = 'aaa'
    @py_assert27 = @py_assert19(@py_assert21, @py_assert23, @py_assert25)
    @py_assert15 = @py_assert13 == @py_assert27
    if not @py_assert15:
        @py_format29 = @pytest_ar._call_reprcompare(('==',), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.readlink\n}(%(py12)s\n{%(py12)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.path\n}.join\n}(%(py8)s, %(py10)s)\n})\n} == %(py28)s\n{%(py28)s = %(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py16)s.path\n}.join\n}(%(py22)s, %(py24)s, %(py26)s)\n}',), (@py_assert13, @py_assert27)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py24':@pytest_ar._saferepr(@py_assert23),  'py26':@pytest_ar._saferepr(@py_assert25),  'py28':@pytest_ar._saferepr(@py_assert27)}
        @py_format31 = ('' + 'assert %(py30)s') % {'py30': @py_format29}
        raise AssertionError(@pytest_ar._format_explanation(@py_format31))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert27 = None


def test_stow_with_basic_senario(source_a, dest):
    dploy.stow([source_a], dest)
    @py_assert1 = os.readlink
    @py_assert4 = os.path
    @py_assert6 = @py_assert4.join
    @py_assert9 = 'aaa'
    @py_assert11 = @py_assert6(dest, @py_assert9)
    @py_assert13 = @py_assert1(@py_assert11)
    @py_assert17 = os.path
    @py_assert19 = @py_assert17.join
    @py_assert21 = '..'
    @py_assert23 = 'source_a'
    @py_assert25 = 'aaa'
    @py_assert27 = @py_assert19(@py_assert21, @py_assert23, @py_assert25)
    @py_assert15 = @py_assert13 == @py_assert27
    if not @py_assert15:
        @py_format29 = @pytest_ar._call_reprcompare(('==',), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.readlink\n}(%(py12)s\n{%(py12)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.path\n}.join\n}(%(py8)s, %(py10)s)\n})\n} == %(py28)s\n{%(py28)s = %(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py16)s.path\n}.join\n}(%(py22)s, %(py24)s, %(py26)s)\n}',), (@py_assert13, @py_assert27)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py24':@pytest_ar._saferepr(@py_assert23),  'py26':@pytest_ar._saferepr(@py_assert25),  'py28':@pytest_ar._saferepr(@py_assert27)}
        @py_format31 = ('' + 'assert %(py30)s') % {'py30': @py_format29}
        raise AssertionError(@pytest_ar._format_explanation(@py_format31))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert27 = None


def test_stow_with_the_same_tree_twice(source_a, dest):
    dploy.stow([source_a], dest)
    dploy.stow([source_a], dest)
    @py_assert1 = os.readlink
    @py_assert4 = os.path
    @py_assert6 = @py_assert4.join
    @py_assert9 = 'aaa'
    @py_assert11 = @py_assert6(dest, @py_assert9)
    @py_assert13 = @py_assert1(@py_assert11)
    @py_assert17 = os.path
    @py_assert19 = @py_assert17.join
    @py_assert21 = '..'
    @py_assert23 = 'source_a'
    @py_assert25 = 'aaa'
    @py_assert27 = @py_assert19(@py_assert21, @py_assert23, @py_assert25)
    @py_assert15 = @py_assert13 == @py_assert27
    if not @py_assert15:
        @py_format29 = @pytest_ar._call_reprcompare(('==',), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.readlink\n}(%(py12)s\n{%(py12)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.path\n}.join\n}(%(py8)s, %(py10)s)\n})\n} == %(py28)s\n{%(py28)s = %(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py16)s.path\n}.join\n}(%(py22)s, %(py24)s, %(py26)s)\n}',), (@py_assert13, @py_assert27)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py24':@pytest_ar._saferepr(@py_assert23),  'py26':@pytest_ar._saferepr(@py_assert25),  'py28':@pytest_ar._saferepr(@py_assert27)}
        @py_format31 = ('' + 'assert %(py30)s') % {'py30': @py_format29}
        raise AssertionError(@pytest_ar._format_explanation(@py_format31))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert27 = None


def test_stow_with_existing_file_conflicts(source_a, source_c, dest):
    dploy.stow([source_a], dest)
    with pytest.raises(ValueError) as (e):
        dploy.stow([source_c], dest)
    source_file = os.path.join(source_c, 'aaa', 'aaa')
    conflicting_file = os.path.join(dest, 'aaa', 'aaa')
    @py_assert1 = error.ConflictsWithExistingFile
    @py_assert6 = @py_assert1(subcmd=SUBCMD, source=source_file, dest=conflicting_file)
    @py_assert8 = @py_assert6.msg
    @py_assert13 = e.value
    @py_assert15 = str(@py_assert13)
    @py_assert10 = @py_assert8 in @py_assert15
    if not @py_assert10:
        @py_format17 = @pytest_ar._call_reprcompare(('in',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.ConflictsWithExistingFile\n}(subcmd=%(py3)s, source=%(py4)s, dest=%(py5)s)\n}.msg\n} in %(py16)s\n{%(py16)s = %(py11)s(%(py14)s\n{%(py14)s = %(py12)s.value\n})\n}',), (@py_assert8, @py_assert15)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(source_file) if 'source_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source_file) else 'source_file',  'py5':@pytest_ar._saferepr(conflicting_file) if 'conflicting_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conflicting_file) else 'conflicting_file',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py12':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert13 = @py_assert15 = None


def test_stow_with_existing_broken_link(source_a, dest):
    conflicting_link = os.path.join(dest, 'aaa')
    os.symlink('non_existant_source', conflicting_link)
    with pytest.raises(ValueError) as (e):
        dploy.stow([source_a], dest)
    source_file = os.path.join(source_a, 'aaa')
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


def test_stow_with_source_conflicts(source_a, source_c, dest):
    with pytest.raises(ValueError) as (e):
        dploy.stow([source_a, source_c], dest)
    conflicting_source_files = [os.path.join(source_a, 'aaa', 'aaa'),
     os.path.join(source_c, 'aaa', 'aaa')]
    @py_assert1 = error.ConflictsWithAnotherSource
    @py_assert5 = @py_assert1(subcmd=SUBCMD, files=conflicting_source_files)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.ConflictsWithAnotherSource\n}(subcmd=%(py3)s, files=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(conflicting_source_files) if 'conflicting_source_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conflicting_source_files) else 'conflicting_source_files',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_stow_with_non_existant_source(dest):
    non_existant_source = 'source'
    with pytest.raises(NotADirectoryError) as (e):
        dploy.stow([non_existant_source], dest)
    @py_assert1 = error.NoSuchDirectory
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=non_existant_source)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.NoSuchDirectory\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(non_existant_source) if 'non_existant_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(non_existant_source) else 'non_existant_source',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_stow_with_duplicate_source(source_a, dest):
    with pytest.raises(ValueError) as (e):
        dploy.stow([source_a, source_a], dest)
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


def test_stow_with_non_existant_dest(source_a):
    non_existant_dest = 'dest'
    with pytest.raises(NotADirectoryError) as (e):
        dploy.stow([source_a], 'dest')
    @py_assert1 = error.NoSuchDirectoryToSubcmdInto
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=non_existant_dest)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.NoSuchDirectoryToSubcmdInto\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(non_existant_dest) if 'non_existant_dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(non_existant_dest) else 'non_existant_dest',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_stow_with_file_as_source(file_a, dest):
    with pytest.raises(NotADirectoryError) as (e):
        dploy.stow([file_a], dest)
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


def test_stow_with_file_as_dest(source_a, file_a):
    with pytest.raises(NotADirectoryError) as (e):
        dploy.stow([source_a], file_a)
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


def test_stow_with_file_as_dest_and_source(file_a, file_b):
    with pytest.raises(NotADirectoryError) as (e):
        dploy.stow([file_a], file_b)
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


def test_stow_with_same_directory_used_as_source_and_dest(source_a):
    with pytest.raises(ValueError) as (e):
        dploy.stow([source_a], source_a)
    @py_assert1 = error.SourceIsSameAsDest
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=source_a)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.SourceIsSameAsDest\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(source_a) if 'source_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source_a) else 'source_a',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_stow_with_same_simple_directory_used_as_source_and_dest(source_only_files):
    with pytest.raises(ValueError) as (e):
        dploy.stow([source_only_files], source_only_files)
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


def test_stow_with_read_only_dest(source_a, dest):
    utils.remove_write_permission(dest)
    with pytest.raises(PermissionError) as (e):
        dploy.stow([source_a], dest)
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


def test_stow_with_write_only_source(source_a, source_c, dest):
    utils.remove_read_permission(source_a)
    with pytest.raises(PermissionError) as (e):
        dploy.stow([source_a, source_c], dest)
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


def test_stow_with_source_with_no_executue_permissions(source_a, source_c, dest):
    utils.remove_execute_permission(source_a)
    with pytest.raises(PermissionError) as (e):
        dploy.stow([source_a, source_c], dest)
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


def test_stow_with_source_dir_with_no_executue_permissions(source_a, source_c, dest):
    source_dir = os.path.join(source_a, 'aaa')
    utils.remove_execute_permission(source_dir)
    with pytest.raises(PermissionError) as (e):
        dploy.stow([source_a, source_c], dest)
    @py_assert1 = error.InsufficientPermissionsToSubcmdFrom
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=source_dir)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.InsufficientPermissionsToSubcmdFrom\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(source_dir) if 'source_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source_dir) else 'source_dir',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_stow_with_write_only_source_file(source_a, dest):
    source_file = os.path.join(source_a, 'aaa')
    utils.remove_read_permission(source_file)
    dploy.stow([source_a], dest)


def verify_unfolded_source_a_and_source_b(dest):
    common_dest_dir = os.path.join(dest, 'aaa')
    common_source_a_dir = os.path.join('..', '..', 'source_a', 'aaa')
    common_source_b_dir = os.path.join('..', '..', 'source_b', 'aaa')
    file_maps = (
     {'dest':os.path.join(common_dest_dir, 'aaa'), 
      'source':os.path.join(common_source_a_dir, 'aaa')},
     {'dest':os.path.join(common_dest_dir, 'bbb'), 
      'source':os.path.join(common_source_a_dir, 'bbb')},
     {'dest':os.path.join(common_dest_dir, 'ccc'), 
      'source':os.path.join(common_source_a_dir, 'ccc')},
     {'dest':os.path.join(common_dest_dir, 'ddd'), 
      'source':os.path.join(common_source_b_dir, 'ddd')},
     {'dest':os.path.join(common_dest_dir, 'eee'), 
      'source':os.path.join(common_source_b_dir, 'eee')},
     {'dest':os.path.join(common_dest_dir, 'fff'), 
      'source':os.path.join(common_source_b_dir, 'fff')})
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isdir
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = @py_assert8(common_dest_dir)
    @py_assert13 = @py_assert3(@py_assert11)
    if not @py_assert13:
        @py_format15 = ('' + 'assert %(py14)s\n{%(py14)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isdir\n}(%(py12)s\n{%(py12)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s)\n})\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(common_dest_dir) if 'common_dest_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(common_dest_dir) else 'common_dest_dir',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = None
    for file_map in file_maps:
        @py_assert1 = os.readlink
        @py_assert3 = file_map['dest']
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = file_map['source']
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.readlink\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_stow_unfolding_with_two_invocations(source_a, source_b, dest):
    dploy.stow([source_a], dest)
    @py_assert1 = os.readlink
    @py_assert4 = os.path
    @py_assert6 = @py_assert4.join
    @py_assert9 = 'aaa'
    @py_assert11 = @py_assert6(dest, @py_assert9)
    @py_assert13 = @py_assert1(@py_assert11)
    @py_assert17 = os.path
    @py_assert19 = @py_assert17.join
    @py_assert21 = '..'
    @py_assert23 = 'source_a'
    @py_assert25 = 'aaa'
    @py_assert27 = @py_assert19(@py_assert21, @py_assert23, @py_assert25)
    @py_assert15 = @py_assert13 == @py_assert27
    if not @py_assert15:
        @py_format29 = @pytest_ar._call_reprcompare(('==',), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.readlink\n}(%(py12)s\n{%(py12)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.path\n}.join\n}(%(py8)s, %(py10)s)\n})\n} == %(py28)s\n{%(py28)s = %(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py16)s.path\n}.join\n}(%(py22)s, %(py24)s, %(py26)s)\n}',), (@py_assert13, @py_assert27)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py24':@pytest_ar._saferepr(@py_assert23),  'py26':@pytest_ar._saferepr(@py_assert25),  'py28':@pytest_ar._saferepr(@py_assert27)}
        @py_format31 = ('' + 'assert %(py30)s') % {'py30': @py_format29}
        raise AssertionError(@pytest_ar._format_explanation(@py_format31))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert27 = None
    dploy.stow([source_b], dest)
    verify_unfolded_source_a_and_source_b(dest)


def test_stow_unfolding_with_mutliple_sources(source_a, source_b, dest):
    dploy.stow([source_a, source_b], dest)
    verify_unfolded_source_a_and_source_b(dest)


def test_stow_unfolding_with_first_sources_execute_permission_removed(source_a, source_b, dest):
    dploy.stow([source_a], dest)
    utils.remove_execute_permission(source_a)
    with pytest.raises(PermissionError) as (e):
        dploy.stow([source_b], dest)
    dest_dir = os.path.join(dest, 'aaa')
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


def test_stow_unfolding_with_write_only_source_file(source_a, source_b, dest):
    source_file = os.path.join(source_a, 'aaa')
    utils.remove_read_permission(source_file)
    with pytest.raises(PermissionError) as (e):
        dploy.stow([source_a, source_b], dest)
    @py_assert1 = error.InsufficientPermissionsToSubcmdFrom
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=source_file)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.InsufficientPermissionsToSubcmdFrom\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD',  'py4':@pytest_ar._saferepr(source_file) if 'source_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(source_file) else 'source_file',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py11':@pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None