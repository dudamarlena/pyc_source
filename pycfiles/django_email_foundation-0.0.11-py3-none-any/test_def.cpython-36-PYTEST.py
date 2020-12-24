# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/farpi/Workspace/cesc/django-email-foundation/django_email_foundation/tests/test_def.py
# Compiled at: 2019-03-22 07:26:30
# Size of source mod 2**32: 872 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, pytest
from django_email_foundation.utils import get_relative_from_manage_path

@pytest.mark.parametrize('getcwd,path,expected', [
 ('/home/demo/workspace/my_project/src', 'src/module/emails', 'module/emails'),
 ('/home/demo/workspace/my_project', 'module/emails', 'module/emails'),
 ('/home/demo/workspace/my_project/src', 'src/emails/sources', 'emails/sources'),
 ('/home/demo/workspace/my_project', 'test/emails/sources', 'test/emails/sources'),
 ('/home/demo/workspace/my_project', 'test_def_apsl/emails/static/emails', 'test_def_apsl/emails/static/emails')])
def test_get_relative_from_manage_path(getcwd, path, expected, monkeypatch):

    def getcwd_patched():
        return getcwd

    monkeypatch.setattr(os, 'getcwd', getcwd_patched)
    @py_assert2 = get_relative_from_manage_path(path)
    @py_assert4 = @py_assert2 == expected
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/farpi/Workspace/cesc/django-email-foundation/django_email_foundation/tests/test_def.py', lineno=21)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(get_relative_from_manage_path) if 'get_relative_from_manage_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_relative_from_manage_path) else 'get_relative_from_manage_path',  'py1':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None