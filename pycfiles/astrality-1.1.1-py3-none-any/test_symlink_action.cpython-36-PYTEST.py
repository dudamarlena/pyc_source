# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/actions/test_symlink_action.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 7511 bytes
"""Tests for astrality.actions.SymlinkAction."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.actions import SymlinkAction
from astrality.persistence import CreatedFiles

def test_null_object_pattern():
    """Copy actions without options should do nothing."""
    symlink_action = SymlinkAction(options={}, directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    symlink_action.execute()


def test_symlink_dry_run(create_temp_files, caplog):
    """If dry_run is True, only log and not symlink."""
    content, target = create_temp_files(2)
    symlink_action = SymlinkAction(options={'content':str(content), 
     'target':str(target)},
      directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    caplog.clear()
    result = symlink_action.execute(dry_run=True)
    @py_assert0 = 'SKIPPED:'
    @py_assert3 = caplog.record_tuples[0][2]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert2 = str(content)
    @py_assert5 = caplog.record_tuples[0][2]
    @py_assert4 = @py_assert2 in @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} in %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = str(target)
    @py_assert5 = caplog.record_tuples[0][2]
    @py_assert4 = @py_assert2 in @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} in %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = {content: target}
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = target.is_symlink
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_symlink_action_using_all_parameters(tmpdir):
    """All three parameters should be respected."""
    temp_dir = Path(tmpdir) / 'content'
    temp_dir.mkdir()
    target = Path(tmpdir) / 'target'
    target.mkdir()
    file1 = temp_dir / 'file1'
    file1.touch()
    file2 = temp_dir / 'file2'
    file2.touch()
    recursive_dir = temp_dir / 'recursive'
    recursive_dir.mkdir()
    file3 = temp_dir / 'recursive' / 'file3'
    file3.touch()
    symlink_options = {'content':str(temp_dir), 
     'target':str(target), 
     'include':'file(\\d)'}
    symlink_action = SymlinkAction(options=symlink_options,
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    symlink_action.execute()
    @py_assert1 = '1'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.is_symlink
    @py_assert6 = @py_assert4()
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = None
    @py_assert1 = '2'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.is_symlink
    @py_assert6 = @py_assert4()
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = None
    @py_assert1 = 'recursive'
    @py_assert3 = target / @py_assert1
    @py_assert4 = '3'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.is_symlink
    @py_assert9 = @py_assert7()
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = None
    @py_assert1 = '1'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.resolve
    @py_assert6 = @py_assert4()
    @py_assert8 = @py_assert6 == file1
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).resolve\n}()\n} == %(py9)s', ), (@py_assert6, file1)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = '2'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.resolve
    @py_assert6 = @py_assert4()
    @py_assert8 = @py_assert6 == file2
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).resolve\n}()\n} == %(py9)s', ), (@py_assert6, file2)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(file2) if 'file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file2) else 'file2'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = 'recursive'
    @py_assert3 = target / @py_assert1
    @py_assert4 = '3'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.resolve
    @py_assert9 = @py_assert7()
    @py_assert11 = @py_assert9 == file3
    if not @py_assert11:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).resolve\n}()\n} == %(py12)s', ), (@py_assert9, file3)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(file3) if 'file3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file3) else 'file3'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_symlinking_without_renaming(tmpdir):
    """When include is not given, keep symlink name."""
    temp_dir = Path(tmpdir) / 'content'
    temp_dir.mkdir()
    target = Path(tmpdir) / 'target'
    target.mkdir()
    file1 = temp_dir / 'file1'
    file1.touch()
    file2 = temp_dir / 'file2'
    file2.touch()
    recursive_dir = temp_dir / 'recursive'
    recursive_dir.mkdir()
    file3 = temp_dir / 'recursive' / 'file3'
    file3.touch()
    symlink_options = {'content':str(temp_dir), 
     'target':str(target)}
    symlink_action = SymlinkAction(options=symlink_options,
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    symlink_action.execute()
    @py_assert1 = 'file1'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.is_symlink
    @py_assert6 = @py_assert4()
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = None
    @py_assert1 = 'file2'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.is_symlink
    @py_assert6 = @py_assert4()
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = None
    @py_assert1 = 'recursive'
    @py_assert3 = target / @py_assert1
    @py_assert4 = 'file3'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.is_symlink
    @py_assert9 = @py_assert7()
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = None
    @py_assert1 = 'file1'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.resolve
    @py_assert6 = @py_assert4()
    @py_assert8 = @py_assert6 == file1
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).resolve\n}()\n} == %(py9)s', ), (@py_assert6, file1)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = 'file2'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.resolve
    @py_assert6 = @py_assert4()
    @py_assert8 = @py_assert6 == file2
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).resolve\n}()\n} == %(py9)s', ), (@py_assert6, file2)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(file2) if 'file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file2) else 'file2'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = 'recursive'
    @py_assert3 = target / @py_assert1
    @py_assert4 = 'file3'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.resolve
    @py_assert9 = @py_assert7()
    @py_assert11 = @py_assert9 == file3
    if not @py_assert11:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).resolve\n}()\n} == %(py12)s', ), (@py_assert9, file3)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(file3) if 'file3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file3) else 'file3'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = None


def test_symlinking_file_to_directory(tmpdir):
    """If symlinking from directory to file, place file in directory."""
    temp_dir = Path(tmpdir) / 'content'
    temp_dir.mkdir()
    target = Path(tmpdir) / 'target'
    target.mkdir()
    file1 = temp_dir / 'file1'
    file1.touch()
    symlink_options = {'content':str(file1), 
     'target':str(target), 
     'include':'file1'}
    symlink_action = SymlinkAction(options=symlink_options,
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    symlink_action.execute()
    @py_assert1 = 'file1'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.is_symlink
    @py_assert6 = @py_assert4()
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = None
    @py_assert1 = 'file1'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.resolve
    @py_assert6 = @py_assert4()
    @py_assert8 = @py_assert6 == file1
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).resolve\n}()\n} == %(py9)s', ), (@py_assert6, file1)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = symlink_action.symlinked_files
    @py_assert4 = {file1: {target / 'file1'}}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.symlinked_files\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(symlink_action) if 'symlink_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(symlink_action) else 'symlink_action',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_running_symlink_action_twice(create_temp_files):
    """Symlink action should be idempotent."""
    content, target = create_temp_files(2)
    content.write_text('content')
    target.write_text('target')
    symlink_options = {'content':str(content), 
     'target':str(target)}
    symlink_action = SymlinkAction(options=symlink_options,
      directory=(content.parent),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    symlink_action.execute()
    @py_assert1 = target.is_symlink
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'content'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    backup = CreatedFiles().creations['test'][str(target)]['backup']
    @py_assert2 = Path(backup)
    @py_assert4 = @py_assert2.read_text
    @py_assert6 = @py_assert4()
    @py_assert9 = 'target'
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}.read_text\n}()\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py1':@pytest_ar._saferepr(backup) if 'backup' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backup) else 'backup',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    symlink_action.execute()
    @py_assert1 = target.is_symlink
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'content'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    backup = CreatedFiles().creations['test'][str(target)]['backup']
    @py_assert2 = Path(backup)
    @py_assert4 = @py_assert2.read_text
    @py_assert6 = @py_assert4()
    @py_assert9 = 'target'
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}.read_text\n}()\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py1':@pytest_ar._saferepr(backup) if 'backup' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backup) else 'backup',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_backup_of_symlink_target(create_temp_files):
    """Overwritten copy targets should be backed up."""
    target, content = create_temp_files(2)
    target.write_text('original')
    content.write_text('new')
    symlink_options = {'content':str(content.name), 
     'target':str(target)}
    symlink_action = SymlinkAction(options=symlink_options,
      directory=(content.parent),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    symlink_action.execute()
    @py_assert1 = target.resolve
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.read_text
    @py_assert7 = @py_assert5()
    @py_assert10 = 'new'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.resolve\n}()\n}.read_text\n}()\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    CreatedFiles().cleanup(module='test')
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'original'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_cleanup_of_created_directory(create_temp_files, tmpdir):
    """Created directories should be cleaned up."""
    tmpdir = Path(tmpdir)
    content, = create_temp_files(1)
    directory = tmpdir / 'dir'
    target = directory / 'target.tmp'
    symlink_options = {'content':str(content.name), 
     'target':str(target)}
    created_files = CreatedFiles().wrapper_for(module='test')
    symlink_action = SymlinkAction(options=symlink_options,
      directory=(content.parent),
      replacer=(lambda x: x),
      context_store={},
      creation_store=created_files)
    symlink_action.execute()
    @py_assert1 = directory.is_dir
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = created_files.creation_store
    @py_assert1 = directory in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s.creation_store\n}', ), (directory, @py_assert3)) % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(created_files) if 'created_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_files) else 'created_files',  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    CreatedFiles().cleanup(module='test')
    @py_assert1 = directory.is_dir
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None