# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_symlinking.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 735 bytes
"""Tests for symlink actions in Module object."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_symlinking_in_on_startup_block(action_block_factory, module_factory, create_temp_files):
    """Action blocks should symlink properly."""
    file1, file2, file3, file4 = create_temp_files(4)
    file2.write_text('original')
    action_block = action_block_factory(symlink=[
     {'content':str(file1), 
      'target':str(file2)},
     {'content':str(file3), 
      'target':str(file4)}])
    module = module_factory(on_startup=action_block)
    module.execute(action='all', block='on_startup')
    @py_assert1 = file2.is_symlink
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(file2) if 'file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file2) else 'file2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = file2.resolve
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == file1
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.resolve\n}()\n} == %(py6)s', ), (@py_assert3, file1)) % {'py0':@pytest_ar._saferepr(file2) if 'file2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file2) else 'file2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(file1) if 'file1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file1) else 'file1'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = file4.is_symlink
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_symlink\n}()\n}') % {'py0':@pytest_ar._saferepr(file4) if 'file4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file4) else 'file4',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = file4.resolve
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == file3
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.resolve\n}()\n} == %(py6)s', ), (@py_assert3, file3)) % {'py0':@pytest_ar._saferepr(file4) if 'file4' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file4) else 'file4',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(file3) if 'file3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file3) else 'file3'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None