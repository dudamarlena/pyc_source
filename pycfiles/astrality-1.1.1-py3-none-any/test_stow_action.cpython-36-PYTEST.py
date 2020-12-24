# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/actions/test_stow_action.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 5271 bytes
"""Tests for astrality.actions.StowAction."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.actions import StowAction
from astrality.persistence import CreatedFiles

def test_null_object_pattern():
    """Copy actions without options should do nothing."""
    stow_action = StowAction(options={}, directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    stow_action.execute()


def test_filtering_stowed_templates(test_config_directory, tmpdir):
    """Users should be able to restrict compilable templates with ignore."""
    temp_dir = Path(tmpdir)
    templates = test_config_directory / 'test_modules' / 'using_all_actions'
    stow_dict = {'content':str(templates), 
     'target':str(temp_dir), 
     'templates':'.+\\.template', 
     'non_templates':'ignore'}
    stow_action = StowAction(options=stow_dict,
      directory=test_config_directory,
      replacer=(lambda x: x),
      context_store={'geography': {'capitol': 'Berlin'}},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    stow_action.execute(dry_run=True)
    @py_assert3 = temp_dir.iterdir
    @py_assert5 = @py_assert3()
    @py_assert7 = list(@py_assert5)
    @py_assert9 = len(@py_assert7)
    @py_assert12 = 0
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.iterdir\n}()\n})\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    stow_action.execute()
    @py_assert3 = temp_dir.iterdir
    @py_assert5 = @py_assert3()
    @py_assert7 = list(@py_assert5)
    @py_assert9 = len(@py_assert7)
    @py_assert12 = 2
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.iterdir\n}()\n})\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert3 = 'recursive'
    @py_assert5 = temp_dir / @py_assert3
    @py_assert6 = @py_assert5.iterdir
    @py_assert8 = @py_assert6()
    @py_assert10 = list(@py_assert8)
    @py_assert12 = len(@py_assert10)
    @py_assert15 = 1
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py0)s(%(py11)s\n{%(py11)s = %(py1)s(%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = (%(py2)s / %(py4)s).iterdir\n}()\n})\n})\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    @py_assert1 = 'module.template'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = @py_assert3.is_file
    @py_assert6 = @py_assert4()
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = None
    @py_assert1 = 'recursive'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = 'empty.template'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.is_file
    @py_assert9 = @py_assert7()
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = None


def test_renaming_templates(test_config_directory, tmpdir):
    """Templates targets should be renameable with a capture group."""
    temp_dir = Path(tmpdir)
    templates = test_config_directory / 'test_modules' / 'using_all_actions'
    stow_dict = {'content':str(templates), 
     'target':str(temp_dir), 
     'templates':'(?:^template\\.(.+)$|^(.+)\\.template$)', 
     'non_templates':'ignore'}
    stow_action = StowAction(options=stow_dict,
      directory=test_config_directory,
      replacer=(lambda x: x),
      context_store={'geography': {'capitol': 'Berlin'}},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    stow_action.execute()
    @py_assert3 = temp_dir.iterdir
    @py_assert5 = @py_assert3()
    @py_assert7 = list(@py_assert5)
    @py_assert9 = len(@py_assert7)
    @py_assert12 = 2
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s(%(py8)s\n{%(py8)s = %(py1)s(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.iterdir\n}()\n})\n})\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert3 = 'recursive'
    @py_assert5 = temp_dir / @py_assert3
    @py_assert6 = @py_assert5.iterdir
    @py_assert8 = @py_assert6()
    @py_assert10 = list(@py_assert8)
    @py_assert12 = len(@py_assert10)
    @py_assert15 = 1
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py0)s(%(py11)s\n{%(py11)s = %(py1)s(%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = (%(py2)s / %(py4)s).iterdir\n}()\n})\n})\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None
    @py_assert1 = 'module'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = @py_assert3.is_file
    @py_assert6 = @py_assert4()
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = None
    @py_assert1 = 'recursive'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = 'empty'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.is_file
    @py_assert9 = @py_assert7()
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = None


def test_symlinking_non_templates(test_config_directory, tmpdir):
    """Non-templates files should be implicitly symlinked."""
    temp_dir = Path(tmpdir)
    templates = test_config_directory / 'test_modules' / 'using_all_actions'
    stow_dict = {'content':str(templates), 
     'target':str(temp_dir), 
     'templates':'.+\\.template'}
    stow_action = StowAction(options=stow_dict,
      directory=test_config_directory,
      replacer=(lambda x: x),
      context_store={'geography': {'capitol': 'Berlin'}},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    stow_action.execute()
    target_dir_content = list(temp_dir.iterdir())
    @py_assert2 = len(target_dir_content)
    @py_assert5 = 6
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(target_dir_content) if 'target_dir_content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target_dir_content) else 'target_dir_content',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = 'module.template'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = @py_assert3 in target_dir_content
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('(%(py0)s / %(py2)s) in %(py5)s', ), (@py_assert3, target_dir_content)) % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(target_dir_content) if 'target_dir_content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target_dir_content) else 'target_dir_content'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = 'module.template'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = @py_assert3.is_symlink
    @py_assert6 = @py_assert4()
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = 'recursive'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = 'empty.template'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.is_file
    @py_assert9 = @py_assert7()
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = None
    @py_assert1 = 'modules.yml'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = @py_assert3.is_symlink
    @py_assert6 = @py_assert4()
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = None
    @py_assert1 = 'modules.yml'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = @py_assert3.resolve
    @py_assert6 = @py_assert4()
    @py_assert10 = 'modules.yml'
    @py_assert12 = templates / @py_assert10
    @py_assert8 = @py_assert6 == @py_assert12
    if not @py_assert8:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).resolve\n}()\n} == (%(py9)s / %(py11)s)', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(templates) if 'templates' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(templates) else 'templates',  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None
    @py_assert1 = 'modules.yml'
    @py_assert3 = templates / @py_assert1
    @py_assert6 = stow_action.managed_files
    @py_assert8 = @py_assert6()
    @py_assert4 = @py_assert3 not in @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert4,), ('(%(py0)s / %(py2)s) not in %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.managed_files\n}()\n}', ), (@py_assert3, @py_assert8)) % {'py0':@pytest_ar._saferepr(templates) if 'templates' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(templates) else 'templates',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(stow_action) if 'stow_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stow_action) else 'stow_action',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_copying_non_template_files(test_config_directory, tmpdir):
    """Non-templates files can be copied."""
    temp_dir = Path(tmpdir)
    templates = test_config_directory / 'test_modules' / 'using_all_actions'
    stow_dict = {'content':str(templates), 
     'target':str(temp_dir), 
     'templates':'.+\\.template', 
     'non_templates':'copy'}
    stow_action = StowAction(options=stow_dict,
      directory=test_config_directory,
      replacer=(lambda x: x),
      context_store={'geography': {'capitol': 'Berlin'}},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    stow_action.execute()
    target_dir_content = list(temp_dir.iterdir())
    @py_assert2 = len(target_dir_content)
    @py_assert5 = 6
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(target_dir_content) if 'target_dir_content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target_dir_content) else 'target_dir_content',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = 'module.template'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = @py_assert3 in target_dir_content
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('(%(py0)s / %(py2)s) in %(py5)s', ), (@py_assert3, target_dir_content)) % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(target_dir_content) if 'target_dir_content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target_dir_content) else 'target_dir_content'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = 'recursive'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = 'empty.template'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.is_file
    @py_assert9 = @py_assert7()
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = None
    @py_assert1 = 'modules.yml'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = @py_assert3.is_file
    @py_assert6 = @py_assert4()
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = None
    @py_assert1 = 'modules.yml'
    @py_assert3 = temp_dir / @py_assert1
    @py_assert4 = @py_assert3.read_text
    @py_assert6 = @py_assert4()
    @py_assert10 = 'modules.yml'
    @py_assert12 = templates / @py_assert10
    @py_assert13 = @py_assert12.read_text
    @py_assert15 = @py_assert13()
    @py_assert8 = @py_assert6 == @py_assert15
    if not @py_assert8:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).read_text\n}()\n} == %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = (%(py9)s / %(py11)s).read_text\n}()\n}', ), (@py_assert6, @py_assert15)) % {'py0':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(templates) if 'templates' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(templates) else 'templates',  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = @py_assert15 = None
    @py_assert1 = 'modules.yml'
    @py_assert3 = templates / @py_assert1
    @py_assert6 = stow_action.managed_files
    @py_assert8 = @py_assert6()
    @py_assert4 = @py_assert3 in @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('(%(py0)s / %(py2)s) in %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.managed_files\n}()\n}', ), (@py_assert3, @py_assert8)) % {'py0':@pytest_ar._saferepr(templates) if 'templates' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(templates) else 'templates',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(stow_action) if 'stow_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stow_action) else 'stow_action',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = None