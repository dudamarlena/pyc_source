# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_context_import.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 1515 bytes
"""Test module for all behaviour related to the import_context action."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from astrality.context import Context

def test_importing_all_context_sections_from_file(test_config_directory, action_block_factory, module_factory, module_manager_factory):
    context_file = test_config_directory / 'context' / 'several_sections.yml'
    original_context = Context({'section2':{'k2_1':'original_v2_1', 
      'k2_2':'original_v2_2'}, 
     'section3':{'k3_1':'original_v3_1', 
      'k3_2':'original_v3_2'}})
    import_context = action_block_factory(import_context={'from_path': str(context_file)})
    module = module_factory(on_startup=import_context)
    module_manager = module_manager_factory(module, context=original_context)
    @py_assert1 = module_manager.application_context
    @py_assert3 = @py_assert1 == original_context
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.application_context\n} == %(py4)s', ), (@py_assert1, original_context)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(original_context) if 'original_context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(original_context) else 'original_context'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    expected_context = Context({'section1':{'k1_1':'v1_1', 
      'k1_2':'v1_2'}, 
     'section2':{'k2_1':'v2_1', 
      'k2_2':'v2_2'}, 
     'section3':{'k3_1':'original_v3_1', 
      'k3_2':'original_v3_2'}})
    module_manager.finish_tasks()
    @py_assert1 = module_manager.application_context
    @py_assert3 = @py_assert1 == expected_context
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.application_context\n} == %(py4)s', ), (@py_assert1, expected_context)) % {'py0':@pytest_ar._saferepr(module_manager) if 'module_manager' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_manager) else 'module_manager',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected_context) if 'expected_context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_context) else 'expected_context'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None