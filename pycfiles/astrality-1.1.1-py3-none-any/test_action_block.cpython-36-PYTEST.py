# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/actions/test_action_block.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 6771 bytes
"""Tests for ActionBlock class."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.actions import ActionBlock
from astrality.context import Context

def test_null_object_pattern(global_modules_config):
    """An empty action block should have no behaviour."""
    action_block = ActionBlock(action_block={}, directory=(Path('/')),
      replacer=(lambda x: x),
      context_store=(Context()),
      global_modules_config=global_modules_config,
      module_name='test')
    action_block.execute(default_timeout=1)


def test_executing_action_block_with_one_action(global_modules_config, test_config_directory, tmpdir):
    """Action block behaviour with only one action specified."""
    temp_dir = Path(tmpdir)
    touched = temp_dir / 'touched.tmp'
    action_block_dict = {'run': [{'shell': 'touch ' + str(touched)}]}
    action_block = ActionBlock(action_block=action_block_dict,
      directory=test_config_directory,
      replacer=(lambda x: x),
      context_store=(Context()),
      global_modules_config=global_modules_config,
      module_name='test')
    action_block.execute(default_timeout=1)
    @py_assert1 = touched.is_file
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(touched) if 'touched' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(touched) else 'touched',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_executing_several_action_blocks(test_config_directory, tmpdir, global_modules_config):
    """Invoking execute() should execute all actions."""
    temp_dir = Path(tmpdir)
    target = temp_dir / 'target.tmp'
    touched = temp_dir / 'touched.tmp'
    action_block_dict = {'import_context':{'from_path': 'context/mercedes.yml'}, 
     'compile':[
      {'content':'templates/a_car.template', 
       'target':str(target)}], 
     'run':{'shell': 'touch ' + str(touched)}, 
     'trigger':{'block': 'on_startup'}}
    context_store = Context()
    action_block = ActionBlock(action_block=action_block_dict,
      directory=test_config_directory,
      replacer=(lambda x: x),
      context_store=context_store,
      global_modules_config=global_modules_config,
      module_name='test')
    action_block.execute(default_timeout=1)
    @py_assert2 = {'car': {'manufacturer': 'Mercedes'}}
    @py_assert1 = context_store == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (context_store, @py_assert2)) % {'py0':@pytest_ar._saferepr(context_store) if 'context_store' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context_store) else 'context_store',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'My car is a Mercedes'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = touched.is_file
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(touched) if 'touched' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(touched) else 'touched',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_retrieving_triggers_from_action_block(global_modules_config):
    """All trigger instructions should be returned."""
    action_block_dict = {'trigger': [
                 {'block': 'on_startup'},
                 {'block':'on_modified', 
                  'path':'test.template'}]}
    action_block = ActionBlock(action_block=action_block_dict,
      directory=(Path('/')),
      replacer=(lambda x: x),
      context_store=(Context()),
      global_modules_config=global_modules_config,
      module_name='test')
    startup_trigger, on_modified_trigger = action_block.triggers()
    @py_assert1 = startup_trigger.block
    @py_assert4 = 'on_startup'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.block\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(startup_trigger) if 'startup_trigger' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(startup_trigger) else 'startup_trigger',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = on_modified_trigger.block
    @py_assert4 = 'on_modified'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.block\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(on_modified_trigger) if 'on_modified_trigger' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(on_modified_trigger) else 'on_modified_trigger',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = on_modified_trigger.specified_path
    @py_assert4 = 'test.template'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.specified_path\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(on_modified_trigger) if 'on_modified_trigger' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(on_modified_trigger) else 'on_modified_trigger',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = on_modified_trigger.relative_path
    @py_assert5 = 'test.template'
    @py_assert7 = Path(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.relative_path\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(on_modified_trigger) if 'on_modified_trigger' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(on_modified_trigger) else 'on_modified_trigger',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = on_modified_trigger.absolute_path
    @py_assert5 = '/test.template'
    @py_assert7 = Path(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.absolute_path\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(on_modified_trigger) if 'on_modified_trigger' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(on_modified_trigger) else 'on_modified_trigger',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_retrieving_triggers_from_action_block_without_triggers(global_modules_config):
    """Action block with no triggers should return empty tuple."""
    action_block = ActionBlock(action_block={}, directory=(Path('/')),
      replacer=(lambda x: x),
      context_store=(Context()),
      global_modules_config=global_modules_config,
      module_name='test')
    @py_assert1 = action_block.triggers
    @py_assert3 = @py_assert1()
    @py_assert7 = tuple()
    @py_assert5 = @py_assert3 == @py_assert7
    if not @py_assert5:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.triggers\n}()\n} == %(py8)s\n{%(py8)s = %(py6)s()\n}', ), (@py_assert3, @py_assert7)) % {'py0':@pytest_ar._saferepr(action_block) if 'action_block' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(action_block) else 'action_block',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_retrieving_all_compiled_templates(global_modules_config, template_directory, tmpdir):
    """All earlier compilations should be retrievable."""
    template1 = template_directory / 'empty.template'
    template2 = template_directory / 'no_context.template'
    temp_dir = Path(tmpdir)
    target1 = temp_dir / 'target1.tmp'
    target2 = temp_dir / 'target2.tmp'
    target3 = temp_dir / 'target3.tmp'
    action_block_dict = {'compile': [
                 {'content':str(template1), 
                  'target':str(target1)},
                 {'content':str(template1), 
                  'target':str(target2)},
                 {'content':str(template2), 
                  'target':str(target3)}]}
    action_block = ActionBlock(action_block=action_block_dict,
      directory=template_directory,
      replacer=(lambda x: x),
      context_store=(Context()),
      global_modules_config=global_modules_config,
      module_name='test')
    @py_assert1 = action_block.performed_compilations
    @py_assert3 = @py_assert1()
    @py_assert6 = {}
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.performed_compilations\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(action_block) if 'action_block' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(action_block) else 'action_block',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    action_block.execute(default_timeout=1)
    @py_assert1 = action_block.performed_compilations
    @py_assert3 = @py_assert1()
    @py_assert6 = {template1: {target1, target2}, template2: {target3}}
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.performed_compilations\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(action_block) if 'action_block' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(action_block) else 'action_block',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_symlinking(action_block_factory, create_temp_files):
    """Action blocks should symlink properly."""
    file1, file2, file3, file4 = create_temp_files(4)
    file2.write_text('original')
    action_block = action_block_factory(symlink=[
     {'content':str(file1), 
      'target':str(file2)},
     {'content':str(file3), 
      'target':str(file4)}])
    action_block.symlink()
    @py_assert1 = file2.is_symlink
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(file2) if 'file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file2) else 'file2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = file2.resolve
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == file1
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.resolve\n}()\n} == %(py6)s', ), (@py_assert3, file1)) % {'py0':@pytest_ar._saferepr(file2) if 'file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file2) else 'file2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = file4.is_symlink
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(file4) if 'file4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file4) else 'file4',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = file4.resolve
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == file3
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.resolve\n}()\n} == %(py6)s', ), (@py_assert3, file3)) % {'py0':@pytest_ar._saferepr(file4) if 'file4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file4) else 'file4',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(file3) if 'file3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file3) else 'file3'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_copying(action_block_factory, create_temp_files):
    """Action blocks should copy properly."""
    file1, file2, file3, file4 = create_temp_files(4)
    file2.write_text('original')
    file4.write_text('some other content')
    action_block = action_block_factory(copy=[
     {'content':str(file1), 
      'target':str(file2)},
     {'content':str(file3), 
      'target':str(file4)}])
    action_block.copy()
    @py_assert1 = file2.read_text
    @py_assert3 = @py_assert1()
    @py_assert7 = file1.read_text
    @py_assert9 = @py_assert7()
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.read_text\n}()\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(file2) if 'file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file2) else 'file2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = file4.read_text
    @py_assert3 = @py_assert1()
    @py_assert7 = file3.read_text
    @py_assert9 = @py_assert7()
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.read_text\n}()\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(file4) if 'file4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file4) else 'file4',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(file3) if 'file3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file3) else 'file3',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_stowing(action_block_factory, create_temp_files):
    """Action blocks should stow properly."""
    template, target = create_temp_files(2)
    template.write_text('{{ env.EXAMPLE_ENV_VARIABLE }}')
    symlink_target = template.parent / 'symlink_me'
    symlink_target.touch()
    action_block = action_block_factory(stow={'content':str(template.parent), 
     'target':str(target.parent), 
     'templates':'file(0).temp', 
     'non_templates':'symlink'})
    action_block.stow()
    @py_assert2 = target.parent
    @py_assert4 = '0'
    @py_assert6 = @py_assert2 / @py_assert4
    @py_assert7 = Path(@py_assert6)
    @py_assert9 = @py_assert7.read_text
    @py_assert11 = @py_assert9()
    @py_assert14 = 'test_value'
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py0)s((%(py3)s\n{%(py3)s = %(py1)s.parent\n} / %(py5)s))\n}.read_text\n}()\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py1':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None
    @py_assert1 = template.parent
    @py_assert3 = 'symlink_me'
    @py_assert5 = @py_assert1 / @py_assert3
    @py_assert6 = @py_assert5.resolve
    @py_assert8 = @py_assert6()
    @py_assert10 = @py_assert8 == symlink_target
    if not @py_assert10:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = (%(py2)s\n{%(py2)s = %(py0)s.parent\n} / %(py4)s).resolve\n}()\n} == %(py11)s', ), (@py_assert8, symlink_target)) % {'py0':@pytest_ar._saferepr(template) if 'template' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template) else 'template',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(symlink_target) if 'symlink_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(symlink_target) else 'symlink_target'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = @py_assert10 = None