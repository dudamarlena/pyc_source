# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/actions/test_compile_action.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 15819 bytes
"""Tests for compile action class."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from pathlib import Path
from astrality.actions import CompileAction
from astrality.persistence import CreatedFiles

def test_null_object_pattern():
    """Compilation action with no parameters should be a null object."""
    compile_action = CompileAction(options={}, directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    target = compile_action.execute()
    @py_assert2 = {}
    @py_assert1 = target == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (target, @py_assert2)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_compilation_of_template_to_temporary_file(template_directory):
    """Compile template to temporary file in absence of `target`."""
    compile_dict = {'content': 'no_context.template'}
    compile_action = CompileAction(options=compile_dict,
      directory=template_directory,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    compilations = compile_action.execute()
    template = template_directory / 'no_context.template'
    @py_assert1 = template in compilations
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (template, compilations)) % {'py0':@pytest_ar._saferepr(template) if 'template' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template) else 'template',  'py2':@pytest_ar._saferepr(compilations) if 'compilations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compilations) else 'compilations'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert0 = compilations[template]
    @py_assert2 = @py_assert0.read_text
    @py_assert4 = @py_assert2()
    @py_assert7 = 'one\ntwo\nthree'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.read_text\n}()\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_that_dry_run_skips_compilation(template_directory, tmpdir, caplog):
    """If dry_run is True, skip compilation of template"""
    compilation_target = Path(tmpdir, 'target.tmp')
    template = template_directory / 'no_context.template'
    compile_dict = {'content':'no_context.template', 
     'target':str(compilation_target)}
    compile_action = CompileAction(options=compile_dict,
      directory=template_directory,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    caplog.clear()
    compilations = compile_action.execute(dry_run=True)
    @py_assert0 = 'SKIPPED:'
    @py_assert3 = caplog.record_tuples[0][2]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert2 = str(template)
    @py_assert5 = caplog.record_tuples[0][2]
    @py_assert4 = @py_assert2 in @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} in %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(template) if 'template' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template) else 'template',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = str(compilation_target)
    @py_assert5 = caplog.record_tuples[0][2]
    @py_assert4 = @py_assert2 in @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} in %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(compilation_target) if 'compilation_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compilation_target) else 'compilation_target',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = template in compilations
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (template, compilations)) % {'py0':@pytest_ar._saferepr(template) if 'template' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template) else 'template',  'py2':@pytest_ar._saferepr(compilations) if 'compilations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compilations) else 'compilations'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = compile_action.performed_compilations
    @py_assert3 = @py_assert1()
    @py_assert6 = {template: {compilation_target}}
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.performed_compilations\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(compile_action) if 'compile_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compile_action) else 'compile_action',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = compilations[template]
    @py_assert2 = @py_assert0.exists
    @py_assert4 = @py_assert2()
    @py_assert6 = not @py_assert4
    if not @py_assert6:
        @py_format7 = ('' + 'assert not %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.exists\n}()\n}') % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_compilation_to_specific_absolute_file_path(template_directory, tmpdir):
    """
    Compile to specified absolute target path.

    The template is specified relatively.
    """
    target = Path(tmpdir) / 'target'
    compile_dict = {'content':'no_context.template', 
     'target':str(target)}
    compile_action = CompileAction(options=compile_dict,
      directory=template_directory,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    return_target = list(compile_action.execute().values())[0]
    @py_assert1 = return_target == target
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (return_target, target)) % {'py0':@pytest_ar._saferepr(return_target) if 'return_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(return_target) else 'return_target',  'py2':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'one\ntwo\nthree'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_compilation_to_specific_relative_file_path(template_directory, tmpdir):
    """
    Compile to specified absolute target path.

    The template is specified absolutely.
    """
    target = Path(tmpdir) / 'target'
    compile_dict = {'content':str(template_directory / 'no_context.template'), 
     'target':str(target.name)}
    compile_action = CompileAction(options=compile_dict,
      directory=(Path(tmpdir)),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    return_target = list(compile_action.execute().values())[0]
    @py_assert1 = return_target == target
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (return_target, target)) % {'py0':@pytest_ar._saferepr(return_target) if 'return_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(return_target) else 'return_target',  'py2':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'one\ntwo\nthree'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_compilation_with_context(template_directory):
    """
    Templates should be compiled with the context store.

    It should compile differently after mutatinig the store.
    """
    compile_dict = {'content': 'test_template.conf'}
    context_store = {}
    compile_action = CompileAction(options=compile_dict,
      directory=template_directory,
      replacer=(lambda x: x),
      context_store=context_store,
      creation_store=CreatedFiles().wrapper_for(module='test'))
    context_store['fonts'] = {2: 'ComicSans'}
    target = list(compile_action.execute().values())[0]
    username = os.environ.get('USER')
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = f"some text\n{username}\nComicSans"
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    context_store['fonts'] = {2: 'TimesNewRoman'}
    target = list(compile_action.execute().values())[0]
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = f"some text\n{username}\nTimesNewRoman"
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_setting_permissions_of_target_template(template_directory):
    """Template target permission bits should be settable."""
    compile_dict = {'content':'empty.template', 
     'permissions':'707'}
    compile_action = CompileAction(options=compile_dict,
      directory=template_directory,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    target = list(compile_action.execute().values())[0]
    @py_assert1 = target.stat
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.st_mode
    @py_assert7 = 511
    @py_assert9 = @py_assert5 & @py_assert7
    @py_assert11 = 455
    @py_assert10 = @py_assert9 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}()\n}.st_mode\n} & %(py8)s) == %(py12)s', ), (@py_assert9, @py_assert11)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert11 = None


def test_use_of_replacer(template_directory, tmpdir):
    """All options should be run through the replacer."""
    compile_dict = {'content':'template', 
     'target':'target', 
     'permissions':'permissions'}
    template = template_directory / 'no_context.template'
    target = Path(tmpdir) / 'target'

    def replacer(string):
        """Trivial replacer."""
        if string == 'template':
            return template.name
        else:
            if string == 'target':
                return str(target)
            if string == 'permissions':
                return '777'
            return string

    compile_action = CompileAction(options=compile_dict,
      directory=template_directory,
      replacer=replacer,
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    target = list(compile_action.execute().values())[0]
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'one\ntwo\nthree'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = target.stat
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.st_mode
    @py_assert7 = 511
    @py_assert9 = @py_assert5 & @py_assert7
    @py_assert11 = 511
    @py_assert10 = @py_assert9 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}()\n}.st_mode\n} & %(py8)s) == %(py12)s', ), (@py_assert9, @py_assert11)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert11 = None


def test_that_current_directory_is_set_correctly(template_directory, tmpdir):
    """Shell commmand filters should be run from `directory`."""
    compile_dict = {'content': str(template_directory / 'shell_filter_working_directory.template')}
    directory = Path(tmpdir)
    compile_action = CompileAction(options=compile_dict,
      directory=directory,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    target = list(compile_action.execute().values())[0]
    @py_assert1 = target.read_text
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == tmpdir
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py6)s', ), (@py_assert3, tmpdir)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_retrieving_all_compiled_templates(template_directory, tmpdir):
    """Compile actions should return all compiled templates."""
    target1, target2 = Path(tmpdir) / 'target.tmp', Path(tmpdir) / 'target2'
    targets = [target1, target2]
    template = Path('no_context.template')
    compile_dict = {'content':str(template), 
     'target':'{target}'}
    compile_action = CompileAction(options=compile_dict,
      directory=template_directory,
      replacer=(lambda x: x.format(target=(targets.pop())) if x == '{target}' else x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    @py_assert1 = compile_action.performed_compilations
    @py_assert3 = @py_assert1()
    @py_assert6 = {}
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.performed_compilations\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(compile_action) if 'compile_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compile_action) else 'compile_action',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    compile_action.execute()
    @py_assert1 = compile_action.performed_compilations
    @py_assert3 = @py_assert1()
    @py_assert6 = {template_directory / template: {target2}}
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.performed_compilations\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(compile_action) if 'compile_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compile_action) else 'compile_action',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    compile_action.execute()
    @py_assert1 = compile_action.performed_compilations
    @py_assert3 = @py_assert1()
    @py_assert6 = {template_directory / template: {target1, target2}}
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.performed_compilations\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(compile_action) if 'compile_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compile_action) else 'compile_action',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_contains_special_method(template_directory, tmpdir):
    """Compile actions should 'contain' its compiled template."""
    temp_dir = Path(tmpdir)
    compile_dict = {'content':'empty.template', 
     'permissions':'707', 
     'target':str(temp_dir / 'target.tmp')}
    compile_action = CompileAction(options=compile_dict,
      directory=template_directory,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    compile_action.execute()
    @py_assert1 = 'empty.template'
    @py_assert3 = template_directory / @py_assert1
    @py_assert4 = @py_assert3 in compile_action
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('(%(py0)s / %(py2)s) in %(py5)s', ), (@py_assert3, compile_action)) % {'py0':@pytest_ar._saferepr(template_directory) if 'template_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template_directory) else 'template_directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(compile_action) if 'compile_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compile_action) else 'compile_action'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = '/no/template'
    @py_assert3 = Path(@py_assert1)
    @py_assert5 = @py_assert3 not in compile_action
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} not in %(py6)s', ), (@py_assert3, compile_action)) % {'py0':@pytest_ar._saferepr(Path) if 'Path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Path) else 'Path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(compile_action) if 'compile_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compile_action) else 'compile_action'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_contains_with_uncompiled_template(template_directory, tmpdir):
    """Compile action only contains *compiled* templates."""
    temp_dir = Path(tmpdir)
    compile_dict = {'content':'empty.template', 
     'permissions':'707', 
     'target':str(temp_dir / 'target.tmp')}
    compile_action = CompileAction(options=compile_dict,
      directory=template_directory,
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    @py_assert1 = 'empty.template'
    @py_assert3 = template_directory / @py_assert1
    @py_assert4 = @py_assert3 not in compile_action
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert4,), ('(%(py0)s / %(py2)s) not in %(py5)s', ), (@py_assert3, compile_action)) % {'py0':@pytest_ar._saferepr(template_directory) if 'template_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template_directory) else 'template_directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(compile_action) if 'compile_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compile_action) else 'compile_action'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    compile_action.execute()
    @py_assert1 = 'empty.template'
    @py_assert3 = template_directory / @py_assert1
    @py_assert4 = @py_assert3 in compile_action
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('(%(py0)s / %(py2)s) in %(py5)s', ), (@py_assert3, compile_action)) % {'py0':@pytest_ar._saferepr(template_directory) if 'template_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template_directory) else 'template_directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(compile_action) if 'compile_action' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compile_action) else 'compile_action'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_compiling_entire_directory(test_config_directory, tmpdir):
    """All directory contents should be recursively compiled."""
    temp_dir = Path(tmpdir).resolve()
    templates = test_config_directory / 'test_modules' / 'using_all_actions'
    for file in templates.glob('**/*.tmp'):
        file.unlink()

    compile_dict = {'content':str(templates), 
     'target':str(temp_dir)}
    compile_action = CompileAction(options=compile_dict,
      directory=test_config_directory,
      replacer=(lambda x: x),
      context_store={'geography': {'capitol': 'Berlin'}},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    results = compile_action.execute()
    @py_assert1 = 'module.template'
    @py_assert3 = templates / @py_assert1
    @py_assert4 = @py_assert3 in results
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('(%(py0)s / %(py2)s) in %(py5)s', ), (@py_assert3, results)) % {'py0':@pytest_ar._saferepr(templates) if 'templates' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(templates) else 'templates',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = results[(templates / 'module.template')]
    @py_assert4 = 'module.template'
    @py_assert6 = temp_dir / @py_assert4
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == (%(py3)s / %(py5)s)', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(temp_dir) if 'temp_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temp_dir) else 'temp_dir',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
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


def test_filtering_compiled_templates(test_config_directory, tmpdir):
    """Users should be able to restrict compilable templates."""
    temp_dir = Path(tmpdir)
    templates = test_config_directory / 'test_modules' / 'using_all_actions'
    compile_dict = {'content':str(templates), 
     'target':str(temp_dir), 
     'include':'.+\\.template'}
    compile_action = CompileAction(options=compile_dict,
      directory=test_config_directory,
      replacer=(lambda x: x),
      context_store={'geography': {'capitol': 'Berlin'}},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    compile_action.execute()
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
    compile_dict = {'content':str(templates), 
     'target':str(temp_dir), 
     'include':'(?:^template\\.(.+)$|^(.+)\\.template$)'}
    compile_action = CompileAction(options=compile_dict,
      directory=test_config_directory,
      replacer=(lambda x: x),
      context_store={'geography': {'capitol': 'Berlin'}},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    compile_action.execute()
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


def test_that_temporary_compile_targets_have_deterministic_paths(tmpdir):
    """Created compilation targets should be deterministic."""
    template_source = Path(tmpdir, 'template.tmp')
    template_source.write_text('content')
    compile_dict = {'content': str(template_source)}
    compile_action1 = CompileAction(options=(compile_dict.copy()),
      directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    compile_action2 = CompileAction(options=(compile_dict.copy()),
      directory=(Path('/')),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    target1 = compile_action1.execute()[template_source]
    target2 = compile_action2.execute()[template_source]
    @py_assert1 = target1 == target2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (target1, target2)) % {'py0':@pytest_ar._saferepr(target1) if 'target1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target1) else 'target1',  'py2':@pytest_ar._saferepr(target2) if 'target2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target2) else 'target2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_creation_of_backup(create_temp_files):
    """Existing external files should be backed up."""
    target, template = create_temp_files(2)
    target.write_text('original')
    template.write_text('new')
    compile_dict = {'content':str(template.name), 
     'target':str(target)}
    compile_action = CompileAction(options=compile_dict,
      directory=(template.parent),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    compile_action.execute()
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


def test_cleanup_of_created_directories(create_temp_files, tmpdir):
    """Directories created during compilation should be cleaned up."""
    tmpdir = Path(tmpdir)
    template, = create_temp_files(1)
    directory = tmpdir / 'subdir' / 'dir'
    target = directory / 'target.tmp'
    compile_dict = {'content':str(template.name), 
     'target':str(target)}
    compile_action = CompileAction(options=compile_dict,
      directory=(template.parent),
      replacer=(lambda x: x),
      context_store={},
      creation_store=CreatedFiles().wrapper_for(module='test'))
    @py_assert1 = target.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = directory.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = directory.parent
    @py_assert3 = @py_assert1.exists
    @py_assert5 = @py_assert3()
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parent\n}.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    compile_action.execute()
    @py_assert1 = target.exists
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = directory.exists
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = directory.parent
    @py_assert3 = @py_assert1.exists
    @py_assert5 = @py_assert3()
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parent\n}.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    CreatedFiles().cleanup(module='test')
    @py_assert1 = target.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = directory.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = directory.parent
    @py_assert3 = @py_assert1.exists
    @py_assert5 = @py_assert3()
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parent\n}.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(directory) if 'directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(directory) else 'directory',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None