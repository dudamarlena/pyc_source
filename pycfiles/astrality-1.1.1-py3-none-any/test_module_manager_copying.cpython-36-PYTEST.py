# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/module_manager/test_module_manager_copying.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 932 bytes
"""Tests for copying in ModuleManager."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.module import ModuleManager

def test_copying_in_on_modified_block(action_block_factory, create_temp_files, module_factory):
    """Module should copy properly."""
    file1, file2, file3, file4 = create_temp_files(4)
    file2.write_text('original')
    file4.write_text('some other content')
    action_block = action_block_factory(copy=[
     {'content':str(file1), 
      'target':str(file2)},
     {'content':str(file3), 
      'target':str(file4)}])
    module = module_factory(on_modified=action_block, path=(Path('/a/b/c')))
    module_manager = ModuleManager()
    module_manager.modules = {'test': module}
    module_manager.on_modified(Path('/a/b/c'))
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