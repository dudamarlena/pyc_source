# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/actions/test_copy_action.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 7064 bytes
"""Tests for astrality.actions.CopyAction."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.actions import CopyAction
from astrality.persistence import CreatedFiles

def test_null_object_pattern():
    """Copy actions without options should do nothing."""
    copy_action = CopyAction(options={}, directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    copy_action.execute()


def test_if_dry_run_is_respected(create_temp_files, caplog):
    """When dry_run is True, the copy action should only be logged."""
    content, target = create_temp_files(2)
    content.write_text('content')
    target.write_text('target')
    copy_action = CopyAction(options={'content':str(content), 
     'target':str(target)},
      directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    caplog.clear()
    result = copy_action.execute(dry_run=True)
    @py_assert2 = {content: target}
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
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
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'target'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_copy_action_using_all_parameters(tmpdir):
    """All three parameters should be respected."""
    temp_dir = Path(tmpdir) / 'content'
    temp_dir.mkdir()
    target = Path(tmpdir) / 'target'
    target.mkdir()
    file1 = temp_dir / 'file1'
    file1.write_text('file1 content')
    file2 = temp_dir / 'file2'
    file2.write_text('file2 content')
    recursive_dir = temp_dir / 'recursive'
    recursive_dir.mkdir()
    file3 = temp_dir / 'recursive' / 'file3'
    file3.write_text('file3 content')
    copy_options = {'content':str(temp_dir), 
     'target':str(target), 
     'include':'file(\\d)'}
    copy_action = CopyAction(options=copy_options,
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    copy_action.execute()
    @py_assert1 = '1'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.read_text
    @py_assert6 = @py_assert4()
    @py_assert10 = file1.read_text
    @py_assert12 = @py_assert10()
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).read_text\n}()\n} == %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s.read_text\n}()\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = '2'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.read_text
    @py_assert6 = @py_assert4()
    @py_assert10 = file2.read_text
    @py_assert12 = @py_assert10()
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).read_text\n}()\n} == %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s.read_text\n}()\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(file2) if 'file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file2) else 'file2',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = 'recursive'
    @py_assert3 = target / @py_assert1
    @py_assert4 = '3'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.read_text
    @py_assert9 = @py_assert7()
    @py_assert13 = file3.read_text
    @py_assert15 = @py_assert13()
    @py_assert11 = @py_assert9 == @py_assert15
    if not @py_assert11:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).read_text\n}()\n} == %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py12)s.read_text\n}()\n}', ), (@py_assert9, @py_assert15)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(file3) if 'file3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file3) else 'file3',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert1 = copy_action.copied_files
    @py_assert4 = {file1: {target / '1'}, file2: {target / '2'}, file3: {target / 'recursive' / '3'}}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.copied_files\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(copy_action) if 'copy_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(copy_action) else 'copy_action',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = file1 in copy_action
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (file1, copy_action)) % {'py0':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1',  'py2':@pytest_ar._saferepr(copy_action) if 'copy_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(copy_action) else 'copy_action'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_copying_without_renaming(tmpdir):
    """When include is not given, keep copy name."""
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
    copy_options = {'content':str(temp_dir), 
     'target':str(target)}
    copy_action = CopyAction(options=copy_options,
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    copy_action.execute()
    @py_assert1 = 'file1'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.read_text
    @py_assert6 = @py_assert4()
    @py_assert10 = file1.read_text
    @py_assert12 = @py_assert10()
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).read_text\n}()\n} == %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s.read_text\n}()\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = 'file2'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.read_text
    @py_assert6 = @py_assert4()
    @py_assert10 = file2.read_text
    @py_assert12 = @py_assert10()
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).read_text\n}()\n} == %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s.read_text\n}()\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(file2) if 'file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file2) else 'file2',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = 'recursive'
    @py_assert3 = target / @py_assert1
    @py_assert4 = 'file3'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.read_text
    @py_assert9 = @py_assert7()
    @py_assert13 = file3.read_text
    @py_assert15 = @py_assert13()
    @py_assert11 = @py_assert9 == @py_assert15
    if not @py_assert11:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).read_text\n}()\n} == %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py12)s.read_text\n}()\n}', ), (@py_assert9, @py_assert15)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(file3) if 'file3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file3) else 'file3',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_copying_file_to_directory(tmpdir):
    """If copying from directory to file, place file in directory."""
    temp_dir = Path(tmpdir) / 'content'
    temp_dir.mkdir()
    target = Path(tmpdir) / 'target'
    target.mkdir()
    file1 = temp_dir / 'file1'
    file1.touch()
    copy_options = {'content':str(file1), 
     'target':str(target), 
     'include':'file1'}
    copy_action = CopyAction(options=copy_options,
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    copy_action.execute()
    @py_assert1 = 'file1'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.read_text
    @py_assert6 = @py_assert4()
    @py_assert10 = file1.read_text
    @py_assert12 = @py_assert10()
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).read_text\n}()\n} == %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s.read_text\n}()\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_setting_permissions_on_target_copy(tmpdir):
    """If permissions is provided, use it for the target."""
    temp_dir = Path(tmpdir) / 'content'
    temp_dir.mkdir()
    target = Path(tmpdir) / 'target'
    target.mkdir()
    file1 = temp_dir / 'file1'
    file1.touch()
    file1.chmod(504)
    copy_options = {'content':str(file1), 
     'target':str(target), 
     'include':'file1', 
     'permissions':'777'}
    copy_action = CopyAction(options=copy_options,
      directory=temp_dir,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    copy_action.execute()
    @py_assert1 = 'file1'
    @py_assert3 = target / @py_assert1
    @py_assert4 = @py_assert3.stat
    @py_assert6 = @py_assert4()
    @py_assert8 = @py_assert6.st_mode
    @py_assert10 = 511
    @py_assert12 = @py_assert8 & @py_assert10
    @py_assert14 = 511
    @py_assert13 = @py_assert12 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('(%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).stat\n}()\n}.st_mode\n} & %(py11)s) == %(py15)s', ), (@py_assert12, @py_assert14)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = @py_assert14 = None


def test_backup_of_copy_target(create_temp_files):
    """Overwritten copy targets should be backed up."""
    target, content = create_temp_files(2)
    target.write_text('original')
    content.write_text('new')
    copy_options = {'content':str(content.name), 
     'target':str(target)}
    copy_action = CopyAction(options=copy_options,
      directory=(content.parent),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    copy_action.execute()
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'new'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
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
    copy_options = {'content':str(content.name), 
     'target':str(target)}
    created_files = CreatedFiles().wrapper_for(module='test')
    copy_action = CopyAction(options=copy_options,
      directory=(content.parent),
      replacer=(lambda x: x),
      context_store={},
      creation_store=created_files)
    copy_action.execute()
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
    created_files.creation_store.cleanup(module='test')
    @py_assert1 = directory.is_dir
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_dir\n}()\n}') % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None