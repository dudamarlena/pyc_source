# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_permissions.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 913 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
import pytest
from astrality.module import ModuleManager

@pytest.mark.parametrize('specified_permission,expected_permission', [
 ('777', 511),
 ('100', 64)])
def test_compiling_template_with_specific_permissions(test_config_directory, tmpdir, specified_permission, expected_permission):
    template = test_config_directory / 'templates' / 'empty.template'
    target = Path(tmpdir) / 'target'
    modules = {'test': {'on_startup': {'compile': {'content':str(template), 
                                         'target':str(target), 
                                         'permissions':specified_permission}}}}
    module_manager = ModuleManager(modules=modules)
    module_manager.finish_tasks()
    @py_assert1 = target.stat
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3.st_mode
    @py_assert7 = 511
    @py_assert9 = @py_assert5 & @py_assert7
    @py_assert10 = @py_assert9 == expected_permission
    if not @py_assert10:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('(%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stat\n}()\n}.st_mode\n} & %(py8)s) == %(py11)s', ), (@py_assert9, expected_permission)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(expected_permission) if 'expected_permission' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_permission) else 'expected_permission'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None