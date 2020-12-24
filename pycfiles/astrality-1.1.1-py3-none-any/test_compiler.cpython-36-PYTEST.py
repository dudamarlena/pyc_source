# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/test_compiler.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 6394 bytes
"""Tests for the compiler module."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, logging, os
from pathlib import Path
import pytest
from jinja2 import UndefinedError
from astrality.compiler import compile_template, compile_template_to_string, jinja_environment
from astrality.context import Context

@pytest.fixture
def test_templates_folder():
    return Path(__file__).parent / 'templates'


@pytest.fixture
def jinja_test_env(test_templates_folder):
    return jinja_environment(test_templates_folder,
      shell_command_working_directory=(Path('~').resolve()))


def test_rendering_environment_variables(jinja_test_env):
    template = jinja_test_env.get_template('env_vars')
    @py_assert1 = template.render
    @py_assert3 = @py_assert1()
    @py_assert6 = 'test_value\nfallback_value\n'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.render\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(template) if 'template' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template) else 'template',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_logging_undefined_variables(jinja_test_env, caplog):
    template = jinja_test_env.get_template('env_vars')
    template.render()
    @py_assert0 = ('astrality.compiler', logging.WARNING, 'Template variable warning: env_UNDEFINED_VARIABLE is undefined')
    @py_assert4 = caplog.record_tuples
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.record_tuples\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_integer_indexed_templates(jinja_test_env):
    template = jinja_test_env.get_template('integer_indexed')
    context = Context({'section': {1:'one',  2:'two'}})
    @py_assert1 = template.render
    @py_assert4 = @py_assert1(context)
    @py_assert7 = 'one\ntwo\ntwo'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.render\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(template) if 'template' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template) else 'template',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(context) if 'context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context) else 'context',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_compilation_of_jinja_template(test_templates_folder):
    template = test_templates_folder / 'env_vars'
    target = Path('/tmp/astrality') / template.name
    compile_template(template, target, {}, Path('/'))
    with open(target) as (target):
        @py_assert1 = target.read
        @py_assert3 = @py_assert1()
        @py_assert6 = 'test_value\nfallback_value\n'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_run_shell_template_filter(test_templates_folder):
    shell_template_path = test_templates_folder / 'shell_filter.template'
    compiled_shell_template_path = Path('/tmp/astrality', shell_template_path.name)
    compiled_shell_template_path.touch()
    context = {}
    compile_template(template=shell_template_path,
      target=compiled_shell_template_path,
      context=context,
      shell_command_working_directory=(Path('/')))
    with open(compiled_shell_template_path) as (target):
        @py_assert1 = target.read
        @py_assert3 = @py_assert1()
        @py_assert6 = 'quick\nanother_quick\nslow_but_allowed\n\nfallback'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    if compiled_shell_template_path.is_file():
        os.remove(compiled_shell_template_path)


def test_working_directory_of_shell_command_filter(test_templates_folder):
    shell_template_path = Path(test_templates_folder, 'shell_filter_working_directory.template')
    compiled_shell_template_path = Path('/tmp/astrality', shell_template_path.name)
    context = {}
    compile_template(template=shell_template_path,
      target=compiled_shell_template_path,
      context=context,
      shell_command_working_directory=(Path('/')))
    with open(compiled_shell_template_path) as (target):
        @py_assert1 = target.read
        @py_assert3 = @py_assert1()
        @py_assert6 = '/'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_environment_variable_interpolation_by_preprocessing_conf_yaml_file():
    test_conf = Path(__file__).parent / 'test_config' / 'test.yml'
    result = compile_template_to_string(template=test_conf,
      context={})
    expected_result = '\n'.join(('section1:', '    var1: value1', '    var2: value1/value2',
                                 '', '', 'section2:', '    # Comment', '    var3: value1',
                                 "    empty_string_var: ''", '', 'section3:', '    env_variable: test_value, hello',
                                 '', 'section4:', '    1: primary_value'))
    @py_assert1 = expected_result == result
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_result, result)) % {'py0':@pytest_ar._saferepr(expected_result) if 'expected_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_result) else 'expected_result',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


@pytest.mark.slow
def test_command_substition_by_preprocessing_yaml_file():
    test_conf = Path(__file__).parent / 'test_config' / 'commands.yml'
    result = compile_template_to_string(template=test_conf,
      context={})
    expected_result = '\n'.join(('section1:', '    key1: test', '    key2: test_value',
                                 '    key3: test_value', '    key4: '))
    @py_assert1 = expected_result == result
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_result, result)) % {'py0':@pytest_ar._saferepr(expected_result) if 'expected_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_result) else 'expected_result',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_handling_of_undefined_context(tmpdir, caplog):
    template = Path(tmpdir) / 'template'
    template.write_text('{{ this.is.not.defined }}')
    with pytest.raises(UndefinedError):
        compile_template_to_string(template=template,
          context={})
    @py_assert0 = "'this' is undefined"
    @py_assert3 = caplog.record_tuples[0][2]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_writing_template_file_with_default_permissions(tmpdir):
    tmpdir = Path(tmpdir)
    template = tmpdir / 'template'
    template.write_text('content')
    permission = 489
    template.chmod(permission)
    target = tmpdir / 'target'
    compile_template(template=template,
      target=target,
      context={},
      shell_command_working_directory=tmpdir)
    @py_assert1 = target.stat
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.st_mode
    @py_assert7 = 511
    @py_assert9 = @py_assert5 & @py_assert7
    @py_assert10 = @py_assert9 == permission
    if not @py_assert10:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}()\n}.st_mode\n} & %(py8)s) == %(py11)s', ), (@py_assert9, permission)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(permission) if 'permission' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(permission) else 'permission'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_writing_template_file_with_specific_octal_permissions(tmpdir):
    tmpdir = Path(tmpdir)
    template = tmpdir / 'template'
    template.write_text('content')
    target = tmpdir / 'target'
    permissions = '514'
    compile_template(template=template,
      target=target,
      context={},
      shell_command_working_directory=tmpdir,
      permissions=permissions)
    @py_assert1 = target.stat
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.st_mode
    @py_assert7 = 511
    @py_assert9 = @py_assert5 & @py_assert7
    @py_assert11 = 332
    @py_assert10 = @py_assert9 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}()\n}.st_mode\n} & %(py8)s) == %(py12)s', ), (@py_assert9, @py_assert11)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert11 = None


def test_writing_template_file_with_specific_modal_permissions(tmpdir):
    tmpdir = Path(tmpdir)
    template = tmpdir / 'template'
    template.write_text('content')
    permission = 420
    template.chmod(permission)
    target = tmpdir / 'target'
    permissions = 'uo+x'
    compile_template(template=template,
      target=target,
      context={},
      shell_command_working_directory=tmpdir,
      permissions=permissions)
    @py_assert1 = target.stat
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.st_mode
    @py_assert7 = 511
    @py_assert9 = @py_assert5 & @py_assert7
    @py_assert11 = 485
    @py_assert10 = @py_assert9 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}()\n}.st_mode\n} & %(py8)s) == %(py12)s', ), (@py_assert9, @py_assert11)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert11 = None


def test_writing_template_file_with_invalid_permissions(tmpdir):
    tmpdir = Path(tmpdir)
    template = tmpdir / 'template'
    template.write_text('content')
    permission = 474
    template.chmod(permission)
    target = tmpdir / 'target'
    permissions = 'invalid_argument'
    compile_template(template=template,
      target=target,
      context={},
      shell_command_working_directory=tmpdir,
      permissions=permissions)
    @py_assert1 = target.stat
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.st_mode
    @py_assert7 = 511
    @py_assert9 = @py_assert5 & @py_assert7
    @py_assert11 = 474
    @py_assert10 = @py_assert9 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}()\n}.st_mode\n} & %(py8)s) == %(py12)s', ), (@py_assert9, @py_assert11)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert11 = None