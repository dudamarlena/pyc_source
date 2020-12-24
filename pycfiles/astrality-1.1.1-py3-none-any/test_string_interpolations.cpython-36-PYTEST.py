# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_string_interpolations.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 3157 bytes
"""Tests for string interpolations in ModuleManager class."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
import logging
from astrality.module import ModuleManager

def test_use_of_string_interpolations_of_module(tmpdir, caplog, template_directory):
    """Path placeholders should be replaced with compilation target."""
    temp_dir = Path(tmpdir)
    a_template = temp_dir / 'a.template'
    a_template.write_text('foobar')
    b_template = temp_dir / 'b.template'
    b_template.write_text('')
    b_target = temp_dir / 'b.target'
    b_on_modified = template_directory / 'empty.template'
    c_template = temp_dir / 'c.template'
    c_template.write_text('')
    c_target = temp_dir / 'c.target'
    modules = {'A':{'on_startup': {'compile': [
                                 {'content': str(a_template)}]}}, 
     'B':{'on_modified': {str(b_on_modified): {'compile': [
                                                       {'content':str(b_template), 
                                                        'target':str(b_target)}]}}}, 
     'C':{'on_exit': {'compile': {'content':str(c_template), 
                              'target':str(c_target)}}}}
    module_manager = ModuleManager(modules=modules,
      directory=temp_dir)
    module_manager.modules['A'].execute(action='compile',
      block='on_startup')
    module_manager.modules['A'].execute(action='compile',
      block='on_startup')
    a_target = list(module_manager.modules['A'].performed_compilations().values())[0].pop()
    @py_assert0 = module_manager.modules['A']
    @py_assert2 = @py_assert0.interpolate_string
    @py_assert4 = 'one two {'
    @py_assert8 = str(a_template)
    @py_assert10 = @py_assert4 + @py_assert8
    @py_assert11 = '}'
    @py_assert13 = @py_assert10 + @py_assert11
    @py_assert14 = @py_assert2(@py_assert13)
    @py_assert17 = 'one two '
    @py_assert21 = str(a_target)
    @py_assert23 = @py_assert17 + @py_assert21
    @py_assert16 = @py_assert14 == @py_assert23
    if not @py_assert16:
        @py_format24 = @pytest_ar._call_reprcompare(('==', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py3)s\n{%(py3)s = %(py1)s.interpolate_string\n}(((%(py5)s + %(py9)s\n{%(py9)s = %(py6)s(%(py7)s)\n}) + %(py12)s))\n} == (%(py18)s + %(py22)s\n{%(py22)s = %(py19)s(%(py20)s)\n})', ), (@py_assert14, @py_assert23)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py7':@pytest_ar._saferepr(a_template) if 'a_template' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a_template) else 'a_template',  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17),  'py19':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py20':@pytest_ar._saferepr(a_target) if 'a_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a_target) else 'a_target',  'py22':@pytest_ar._saferepr(@py_assert21)}
        @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
        raise AssertionError(@pytest_ar._format_explanation(@py_format26))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert14 = @py_assert16 = @py_assert17 = @py_assert21 = @py_assert23 = None
    @py_assert0 = module_manager.modules['A']
    @py_assert2 = @py_assert0.interpolate_string
    @py_assert4 = '{leave/me/alone}'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = '{leave/me/alone}'
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.interpolate_string\n}(%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    module_manager.modules['B'].execute(action='compile',
      block='on_modified',
      path=b_on_modified)
    @py_assert0 = module_manager.modules['B']
    @py_assert2 = @py_assert0.interpolate_string
    @py_assert4 = '{'
    @py_assert8 = str(b_template)
    @py_assert10 = @py_assert4 + @py_assert8
    @py_assert11 = '}'
    @py_assert13 = @py_assert10 + @py_assert11
    @py_assert14 = @py_assert2(@py_assert13)
    @py_assert19 = str(b_target)
    @py_assert16 = @py_assert14 == @py_assert19
    if not @py_assert16:
        @py_format21 = @pytest_ar._call_reprcompare(('==', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py3)s\n{%(py3)s = %(py1)s.interpolate_string\n}(((%(py5)s + %(py9)s\n{%(py9)s = %(py6)s(%(py7)s)\n}) + %(py12)s))\n} == %(py20)s\n{%(py20)s = %(py17)s(%(py18)s)\n}', ), (@py_assert14, @py_assert19)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py7':@pytest_ar._saferepr(b_template) if 'b_template' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(b_template) else 'b_template',  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py18':@pytest_ar._saferepr(b_target) if 'b_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(b_target) else 'b_target',  'py20':@pytest_ar._saferepr(@py_assert19)}
        @py_format23 = 'assert %(py22)s' % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert14 = @py_assert16 = @py_assert19 = None
    module_manager.modules['C'].execute(action='compile',
      block='on_exit')
    @py_assert0 = module_manager.modules['C']
    @py_assert2 = @py_assert0.interpolate_string
    @py_assert4 = '{c.template/into/..}'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert11 = str(c_target)
    @py_assert8 = @py_assert6 == @py_assert11
    if not @py_assert8:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.interpolate_string\n}(%(py5)s)\n} == %(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}', ), (@py_assert6, @py_assert11)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py10':@pytest_ar._saferepr(c_target) if 'c_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c_target) else 'c_target',  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = None
    caplog.clear()
    module_manager.modules['C'].interpolate_string('{/not/here}')
    @py_assert1 = caplog.record_tuples
    @py_assert4 = [
     (
      'astrality.module', logging.ERROR, 'String placeholder {/not/here} could not be replaced. "/not/here" has not been compiled.')]
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.record_tuples\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None