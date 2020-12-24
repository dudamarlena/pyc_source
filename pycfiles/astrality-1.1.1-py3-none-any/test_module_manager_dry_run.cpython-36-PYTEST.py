# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/module_manager/test_module_manager_dry_run.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 1397 bytes
"""Tests for finishing ModuleManager tasks with dry_run set to True."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from astrality.module import ModuleManager

def test_that_dry_run_is_respected(create_temp_files):
    """ModuleManager should pass on dry_run to its actions."""
    touched, copy_content, copy_target, compile_content, compile_target, symlink_content, symlink_target = create_temp_files(7)
    touched.unlink()
    copy_target.write_text('copy_original')
    compile_target.write_text('compile_original')
    modules = {'A': {'run':{'shell': 'touch ' + str(touched)}, 
           'copy':{'content':str(copy_content), 
            'target':str(copy_target)}, 
           'compile':{'content':str(compile_content), 
            'target':str(compile_target)}, 
           'symlink':{'content':str(symlink_content), 
            'target':str(symlink_target)}}}
    module_manager = ModuleManager(modules=modules,
      directory=(touched.parents[1]),
      dry_run=True)
    module_manager.finish_tasks()
    @py_assert1 = touched.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(touched) if 'touched' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(touched) else 'touched',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = copy_target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'copy_original'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(copy_target) if 'copy_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(copy_target) else 'copy_target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = compile_target.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = 'compile_original'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(compile_target) if 'compile_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compile_target) else 'compile_target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = symlink_target.is_symlink
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(symlink_target) if 'symlink_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(symlink_target) else 'symlink_target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None