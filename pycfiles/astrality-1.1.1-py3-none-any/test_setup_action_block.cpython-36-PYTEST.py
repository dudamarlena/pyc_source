# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_setup_action_block.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 1011 bytes
"""Tests for handling setup action blocks in ModuleManager."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.module import ModuleManager

def test_that_setup_block_is_only_executed_once(tmpdir):
    """Setup blocks in modules should only be performed once."""
    touched = Path(tmpdir, 'touched.tmp')
    modules = {'A': {'on_setup': {'run': {'shell': f"touch {touched}"}}}}
    module_manager = ModuleManager(modules=modules)
    @py_assert1 = touched.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(touched) if 'touched' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(touched) else 'touched',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    module_manager.finish_tasks()
    @py_assert1 = touched.exists
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(touched) if 'touched' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(touched) else 'touched',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    del module_manager
    touched.unlink()
    module_manager = ModuleManager(modules=modules)
    module_manager.finish_tasks()
    @py_assert1 = touched.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}') % {'py0':@pytest_ar._saferepr(touched) if 'touched' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(touched) else 'touched',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None