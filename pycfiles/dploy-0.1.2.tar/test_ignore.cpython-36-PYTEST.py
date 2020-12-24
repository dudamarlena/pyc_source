# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/arecarn/Dropbox/projects/dploy/master/tests/test_ignore.py
# Compiled at: 2017-10-26 23:57:28
# Size of source mod 2**32: 1370 bytes
"""
Tests for the ignore feature
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, dploy
SUBCMD = 'stow'

def test_ignore_by_ignoring_everthing(source_a, source_c, dest):
    dploy.stow([source_a, source_c], dest, ignore_patterns=['*'])
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


def test_ignore_by_ignoring_only_subdirectory(source_a, source_c, dest):
    dploy.stow([source_a, source_c], dest, ignore_patterns=['aaa'])
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


def test_ignore_by_ignoring_everthing_(source_a, source_c, dest):
    dploy.stow([source_a, source_c], dest, ignore_patterns=['source_*/aaa'])
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


def test_ignore_by_ignoring_everthing__(source_a, source_c, dest):
    dploy.stow([source_a, source_c], dest, ignore_patterns=['*/aaa'])
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


def test_ignore_file_by_ignoring_everthing__(source_a, source_c, file_dploystowignore, dest):
    ignore_patterns = [
     '*/aaa']
    with open(file_dploystowignore, 'w') as (file):
        file.write('\n'.join(ignore_patterns))
    dploy.stow([source_a, source_c], dest)
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