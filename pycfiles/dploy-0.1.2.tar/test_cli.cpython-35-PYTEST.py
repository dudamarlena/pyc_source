# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /evtfs/home/rcarney/Dropbox/projects/dploy/master/tests/test_cli.py
# Compiled at: 2017-05-29 01:36:19
# Size of source mod 2**32: 3057 bytes
"""
Tests for the CLI interface
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, re, pytest, dploy.cli

def test_cli_with_stow_with_simple_senario(source_only_files, dest, capsys):
    args = [
     'stow', source_only_files, dest]
    dploy.cli.run(args)
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
        @py_format29 = @pytest_ar._call_reprcompare(('==',), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.readlink\n}(%(py12)s\n{%(py12)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.path\n}.join\n}(%(py8)s, %(py10)s)\n})\n} == %(py28)s\n{%(py28)s = %(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py16)s.path\n}.join\n}(%(py22)s, %(py24)s, %(py26)s)\n}',), (@py_assert13, @py_assert27)) % {'py24': @pytest_ar._saferepr(@py_assert23), 'py2': @pytest_ar._saferepr(@py_assert1), 'py18': @pytest_ar._saferepr(@py_assert17), 'py8': @pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest', 'py28': @pytest_ar._saferepr(@py_assert27), 'py3': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py5': @pytest_ar._saferepr(@py_assert4), 'py26': @pytest_ar._saferepr(@py_assert25), 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 
         'py12': @pytest_ar._saferepr(@py_assert11), 'py7': @pytest_ar._saferepr(@py_assert6), 'py22': @pytest_ar._saferepr(@py_assert21), 'py20': @pytest_ar._saferepr(@py_assert19), 'py16': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format31 = ('' + 'assert %(py30)s') % {'py30': @py_format29}
        raise AssertionError(@pytest_ar._format_explanation(@py_format31))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert27 = None
    out, _ = capsys.readouterr()
    d = os.path.join(dest, 'aaa')
    s = os.path.relpath(os.path.join(source_only_files, 'aaa'), dest)
    @py_assert2 = 'dploy stow: link {dest} => {source}\n'
    @py_assert4 = @py_assert2.format
    @py_assert8 = @py_assert4(source=s, dest=d)
    @py_assert1 = out == @py_assert8
    if not @py_assert1:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.format\n}(source=%(py6)s, dest=%(py7)s)\n}',), (out, @py_assert8)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd', 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py3': @pytest_ar._saferepr(@py_assert2), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert2 = @py_assert4 = @py_assert8 = None


def test_cli_unstow_with_basic_senario(source_a, dest, capsys):
    args_stow = [
     'stow', source_a, dest]
    dploy.cli.run(args_stow)
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
        @py_format29 = @pytest_ar._call_reprcompare(('==',), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.readlink\n}(%(py12)s\n{%(py12)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.path\n}.join\n}(%(py8)s, %(py10)s)\n})\n} == %(py28)s\n{%(py28)s = %(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py16)s.path\n}.join\n}(%(py22)s, %(py24)s, %(py26)s)\n}',), (@py_assert13, @py_assert27)) % {'py24': @pytest_ar._saferepr(@py_assert23), 'py2': @pytest_ar._saferepr(@py_assert1), 'py18': @pytest_ar._saferepr(@py_assert17), 'py8': @pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest', 'py28': @pytest_ar._saferepr(@py_assert27), 'py3': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py5': @pytest_ar._saferepr(@py_assert4), 'py26': @pytest_ar._saferepr(@py_assert25), 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 
         'py12': @pytest_ar._saferepr(@py_assert11), 'py7': @pytest_ar._saferepr(@py_assert6), 'py22': @pytest_ar._saferepr(@py_assert21), 'py20': @pytest_ar._saferepr(@py_assert19), 'py16': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format31 = ('' + 'assert %(py30)s') % {'py30': @py_format29}
        raise AssertionError(@pytest_ar._format_explanation(@py_format31))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert27 = None
    args_unstow = [
     'unstow', source_a, dest]
    dploy.cli.run(args_unstow)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'aaa'
    @py_assert13 = @py_assert8(dest, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    @py_assert17 = not @py_assert15
    if not @py_assert17:
        @py_format18 = ('' + 'assert not %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest', 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py16': @pytest_ar._saferepr(@py_assert15), 'py9': @pytest_ar._saferepr(@py_assert8), 'py14': @pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    out, _ = capsys.readouterr()
    src_dir = os.path.relpath(os.path.join(source_a, 'aaa'), dest)
    dest_dir = os.path.join(dest, 'aaa')
    expected_output = 'dploy stow: link {dest_dir} => {src_dir}\ndploy unstow: unlink {dest_dir} => {src_dir}\n'.format(src_dir=src_dir, dest_dir=dest_dir)
    @py_assert1 = out == expected_output
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py2)s',), (out, expected_output)) % {'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output'}
        @py_format5 = ('' + 'assert %(py4)s') % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_cli_with_link_directory(source_a, dest, capsys):
    args = [
     'link', source_a, os.path.join(dest, 'source_a_link')]
    dploy.cli.run(args)
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
    output, _ = capsys.readouterr()
    expected_output_unformatted = 'dploy link: link {dest} => {source}\n'
    expected_output = expected_output_unformatted.format(source=os.path.relpath(source_a, dest), dest=os.path.join(dest, 'source_a_link'))
    @py_assert1 = output == expected_output
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py2)s',), (output, expected_output)) % {'py0': @pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output', 'py2': @pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output'}
        @py_format5 = ('' + 'assert %(py4)s') % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_cli_with_dry_run_option_with_stow_with_simple_senario(source_only_files, dest, capsys):
    args = [
     '--dry-run', 'stow', source_only_files, dest]
    dploy.cli.run(args)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = os.path
    @py_assert8 = @py_assert6.join
    @py_assert11 = 'aaa'
    @py_assert13 = @py_assert8(dest, @py_assert11)
    @py_assert15 = @py_assert3(@py_assert13)
    @py_assert17 = not @py_assert15
    if not @py_assert17:
        @py_format18 = ('' + 'assert not %(py16)s\n{%(py16)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py14)s\n{%(py14)s = %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.path\n}.join\n}(%(py10)s, %(py12)s)\n})\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest', 'py7': @pytest_ar._saferepr(@py_assert6), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py16': @pytest_ar._saferepr(@py_assert15), 'py9': @pytest_ar._saferepr(@py_assert8), 'py14': @pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    out, _ = capsys.readouterr()
    d = os.path.join(dest, 'aaa')
    s = os.path.relpath(os.path.join(source_only_files, 'aaa'), dest)
    @py_assert2 = 'dploy stow: link {dest} => {source}\n'
    @py_assert4 = @py_assert2.format
    @py_assert8 = @py_assert4(source=s, dest=d)
    @py_assert1 = out == @py_assert8
    if not @py_assert1:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.format\n}(source=%(py6)s, dest=%(py7)s)\n}',), (out, @py_assert8)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd', 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py3': @pytest_ar._saferepr(@py_assert2), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert2 = @py_assert4 = @py_assert8 = None


def test_cli_with_silent_option_with_stow_with_simple_senario(source_only_files, dest, capsys):
    args = [
     '--silent', 'stow', source_only_files, dest]
    dploy.cli.run(args)
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
        @py_format29 = @pytest_ar._call_reprcompare(('==',), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.readlink\n}(%(py12)s\n{%(py12)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.path\n}.join\n}(%(py8)s, %(py10)s)\n})\n} == %(py28)s\n{%(py28)s = %(py20)s\n{%(py20)s = %(py18)s\n{%(py18)s = %(py16)s.path\n}.join\n}(%(py22)s, %(py24)s, %(py26)s)\n}',), (@py_assert13, @py_assert27)) % {'py24': @pytest_ar._saferepr(@py_assert23), 'py2': @pytest_ar._saferepr(@py_assert1), 'py18': @pytest_ar._saferepr(@py_assert17), 'py8': @pytest_ar._saferepr(dest) if 'dest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dest) else 'dest', 'py28': @pytest_ar._saferepr(@py_assert27), 'py3': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py5': @pytest_ar._saferepr(@py_assert4), 'py26': @pytest_ar._saferepr(@py_assert25), 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 
         'py12': @pytest_ar._saferepr(@py_assert11), 'py7': @pytest_ar._saferepr(@py_assert6), 'py22': @pytest_ar._saferepr(@py_assert21), 'py20': @pytest_ar._saferepr(@py_assert19), 'py16': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format31 = ('' + 'assert %(py30)s') % {'py30': @py_format29}
        raise AssertionError(@pytest_ar._format_explanation(@py_format31))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert25 = @py_assert27 = None
    out, _ = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (out, @py_assert2)) % {'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = ('' + 'assert %(py5)s') % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_cli_with_version_option(capsys):
    args = [
     '--version']
    with pytest.raises(SystemExit):
        dploy.cli.run(args)
        out, _ = capsys.readouterr()
        @py_assert1 = re.match
        @py_assert3 = 'dploy \\d+.\\d+\\.\\d+(-\\w+)?\\n'
        @py_assert6 = @py_assert1(@py_assert3, out)
        @py_assert9 = None
        @py_assert8 = @py_assert6 != @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.match\n}(%(py4)s, %(py5)s)\n} != %(py10)s', ), (@py_assert6, @py_assert9)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None