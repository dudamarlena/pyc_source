# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/integration-tests/test_imports.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 1085 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys

def import_ok(module_name):
    try:
        module = __import__(module_name)
        sys.stdout.write('import succeeded: %s -> %s\n' % (
         module_name, module))
        return True
    except Exception as ex:
        sys.stderr.write('import failed: %s: %s\n' % (
         module_name, ex.message))
        return False


def test_imports():
    root = 'concrete'
    for parent_path, dir_entries, file_entries in os.walk(root):
        for basename in dir_entries:
            if not basename.endswith('__pycache__'):
                dir_path = os.path.join(parent_path, basename)
                module_name = dir_path.replace(os.sep, '.')
                @py_assert2 = import_ok(module_name)
                if not @py_assert2:
                    @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(import_ok) if 'import_ok' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(import_ok) else 'import_ok', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(module_name) if 'module_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_name) else 'module_name'}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format4))
                @py_assert2 = None

        for basename in file_entries:
            if basename.endswith('.py') and basename != '__init__.py':
                file_path = os.path.join(parent_path, basename)
                module_name = file_path[:-len('.py')].replace(os.sep, '.')
                @py_assert2 = import_ok(module_name)
                if not @py_assert2:
                    @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(import_ok) if 'import_ok' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(import_ok) else 'import_ok', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(module_name) if 'module_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_name) else 'module_name'}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format4))
                @py_assert2 = None