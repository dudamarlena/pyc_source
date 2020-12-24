# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/cli/test_cleanup.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 1758 bytes
"""Tests for the --cleanup cli flag."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from pathlib import Path
import pytest
from astrality.module import ModuleManager

@pytest.mark.parametrize('method', ['compile', 'copy', 'symlink'])
def test_that_cleanup_cli_works(method, create_temp_files, patch_xdg_directory_standard):
    """--cleanup module_name, all module created files should be deleted"""
    template1, template2, template3, target1, target2, target3 = create_temp_files(6)
    for template in (template1, template2, template3):
        template.write_text('new content')

    for target in (target1, target2, target3):
        target.write_text('original content')

    modules = {'A':{method: [
               {'content':str(template1), 
                'target':str(target1)},
               {'content':str(template2), 
                'target':str(target2)}]}, 
     'B':{method: {'content':str(template3), 
               'target':str(target3)}}}
    module_manager = ModuleManager(modules=modules)
    module_manager.finish_tasks()
    for target in (target1, target2, target3):
        @py_assert1 = target.resolve
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3.read_text
        @py_assert7 = @py_assert5()
        @py_assert10 = 'new content'
        @py_assert9 = @py_assert7 == @py_assert10
        if not @py_assert9:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.resolve\n}()\n}.read_text\n}()\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None

    bin_script = str(Path(__file__).parents[3] / 'bin' / 'astrality')
    data_home = 'XDG_DATA_HOME="' + str(patch_xdg_directory_standard) + '/.." '
    command = data_home + bin_script + ' --cleanup A --cleanup B'
    os.system(command)
    for target in (target1, target2, target3):
        @py_assert1 = target.resolve
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3.read_text
        @py_assert7 = @py_assert5()
        @py_assert10 = 'original content'
        @py_assert9 = @py_assert7 == @py_assert10
        if not @py_assert9:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.resolve\n}()\n}.read_text\n}()\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None