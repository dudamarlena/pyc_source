# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/module_manager/test_module_manager_stowing.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 1078 bytes
"""Tests for ModuleManager stow action."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.module import ModuleManager

def test_stowing(action_block_factory, create_temp_files, module_factory):
    """ModuleManager should stow properly."""
    template, target = create_temp_files(2)
    template.write_text('{{ env.EXAMPLE_ENV_VARIABLE }}')
    symlink_target = template.parent / 'symlink_me'
    symlink_target.touch()
    action_block = action_block_factory(stow={'content':str(template.parent), 
     'target':str(target.parent), 
     'templates':'file(0).temp', 
     'non_templates':'symlink'})
    module = module_factory(on_exit=action_block)
    module_manager = ModuleManager()
    module_manager.modules = {'test': module}
    module_manager.exit()
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