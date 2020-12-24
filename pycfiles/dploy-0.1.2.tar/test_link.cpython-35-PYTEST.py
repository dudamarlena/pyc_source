# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /evtfs/home/rcarney/Dropbox/projects/dploy/master/tests/test_link.py
# Compiled at: 2017-03-25 02:31:45
# Size of source mod 2**32: 2255 bytes
"""
Tests for the link sub command
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, pytest, dploy, dploy.error as error, utils
SUBCMD = 'link'

def test_link_with_directory_as_source(source_a, dest):
    dploy.link(source_a, os.path.join(dest, 'source_a_link'))
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.islink
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'source_a_link'
    @py_assert13 = @py_assert8(dest, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    if not @py_assert15:
        @py_format17 = ('' + 'assert %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.islink\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest', 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py16': @pytest_ar._saferepr(@py_assert15), 'py9': @pytest_ar._saferepr(@py_assert8), 'py14': @pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_link_with_file_as_source(file_a, dest):
    dploy.link(file_a, os.path.join(dest, 'file_a'))
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.islink
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'file_a'
    @py_assert13 = @py_assert8(dest, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    if not @py_assert15:
        @py_format17 = ('' + 'assert %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.islink\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest', 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py16': @pytest_ar._saferepr(@py_assert15), 'py9': @pytest_ar._saferepr(@py_assert8), 'py14': @pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_link_with_non_existant_source(dest):
    non_existant_source = 'source_a'
    with pytest.raises(FileNotFoundError) as (e):
        dploy.link(non_existant_source, os.path.join(dest, 'source_a_link'))
    @py_assert1 = error.NoSuchFileOrDirectory
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=non_existant_source)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.NoSuchFileOrDirectory\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}',), (@py_assert7, @py_assert14)) % {'py4': @pytest_ar._saferepr(non_existant_source) if 'non_existant_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(non_existant_source) else 'non_existant_source', 'py11': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py15': @pytest_ar._saferepr(@py_assert14), 'py0': @pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD'}
        @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_link_with_non_existant_dest(source_a):
    non_existant_dest = 'dest'
    with pytest.raises(FileNotFoundError) as (e):
        dploy.link(source_a, os.path.join(non_existant_dest, 'source_a_link'))
    @py_assert1 = error.NoSuchFileOrDirectory
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=non_existant_dest)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.NoSuchFileOrDirectory\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}',), (@py_assert7, @py_assert14)) % {'py4': @pytest_ar._saferepr(non_existant_dest) if 'non_existant_dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(non_existant_dest) else 'non_existant_dest', 'py11': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py15': @pytest_ar._saferepr(@py_assert14), 'py0': @pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD'}
        @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_link_with_read_only_dest(file_a, dest):
    dest_file = os.path.join(dest, 'file_a_link')
    utils.remove_write_permission(dest)
    with pytest.raises(PermissionError) as (e):
        dploy.link(file_a, dest_file)
    @py_assert1 = error.InsufficientPermissionsToSubcmdTo
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=dest_file)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.InsufficientPermissionsToSubcmdTo\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}',), (@py_assert7, @py_assert14)) % {'py4': @pytest_ar._saferepr(dest_file) if 'dest_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest_file) else 'dest_file', 'py11': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py15': @pytest_ar._saferepr(@py_assert14), 'py0': @pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD'}
        @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_link_with_write_only_source(file_a, dest):
    dest_file = os.path.join(dest, 'file_a_link')
    utils.remove_read_permission(file_a)
    with pytest.raises(PermissionError) as (e):
        dploy.link(file_a, dest_file)
    @py_assert1 = error.InsufficientPermissions
    @py_assert5 = @py_assert1(subcmd=SUBCMD, file=file_a)
    @py_assert7 = @py_assert5.msg
    @py_assert12 = e.value
    @py_assert14 = str(@py_assert12)
    @py_assert9 = @py_assert7 in @py_assert14
    if not @py_assert9:
        @py_format16 = @pytest_ar._call_reprcompare(('in',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.InsufficientPermissions\n}(subcmd=%(py3)s, file=%(py4)s)\n}.msg\n} in %(py15)s\n{%(py15)s = %(py10)s(%(py13)s\n{%(py13)s = %(py11)s.value\n})\n}',), (@py_assert7, @py_assert14)) % {'py4': @pytest_ar._saferepr(file_a) if 'file_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_a) else 'file_a', 'py11': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py15': @pytest_ar._saferepr(@py_assert14), 'py0': @pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD'}
        @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None


def test_link_with_conflicting_broken_link_at_dest(file_a, dest):
    dest_file = os.path.join(dest, 'file_a_link')
    os.symlink('non_existant_source', dest_file)
    with pytest.raises(ValueError) as (e):
        dploy.link(file_a, dest_file)
    @py_assert1 = error.ConflictsWithExistingLink
    @py_assert6 = @py_assert1(subcmd=SUBCMD, source=file_a, dest=dest_file)
    @py_assert8 = @py_assert6.msg
    @py_assert13 = e.value
    @py_assert15 = str(@py_assert13)
    @py_assert10 = @py_assert8 in @py_assert15
    if not @py_assert10:
        @py_format17 = @pytest_ar._call_reprcompare(('in',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.ConflictsWithExistingLink\n}(subcmd=%(py3)s, source=%(py4)s, dest=%(py5)s)\n}.msg\n} in %(py16)s\n{%(py16)s = %(py11)s(%(py14)s\n{%(py14)s = %(py12)s.value\n})\n}',), (@py_assert8, @py_assert15)) % {'py4': @pytest_ar._saferepr(file_a) if 'file_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_a) else 'file_a', 'py5': @pytest_ar._saferepr(dest_file) if 'dest_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest_file) else 'dest_file', 'py2': @pytest_ar._saferepr(@py_assert1), 'py16': @pytest_ar._saferepr(@py_assert15), 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e', 'py0': @pytest_ar._saferepr(error) if 'error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(error) else 'error', 'py3': @pytest_ar._saferepr(SUBCMD) if 'SUBCMD' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SUBCMD) else 'SUBCMD', 'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert13 = @py_assert15 = None