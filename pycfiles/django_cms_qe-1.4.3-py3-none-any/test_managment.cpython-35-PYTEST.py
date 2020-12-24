# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_newsletter/tests/test_managment.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 886 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from unittest import mock

def test_not_set_mailchimp():
    with mock.patch('cms_qe_newsletter.external_services.sync.sync_tasks', return_value=[
     (True, 'ok'),
     (None, 'warning'),
     (False, 'error')]):
        from ..management.commands.cms_qe_newsletter_sync import Command
        with mock.patch('cms_qe_newsletter.management.commands.cms_qe_newsletter_sync.logger') as (log_mock):
            command = Command()
            command.handle()
            @py_assert1 = log_mock.info
            @py_assert3 = @py_assert1.call_args_list
            @py_assert6 = [
             mock.call('Newsletter sync started...'), mock.call('ok'), mock.call('Newsletter sync finished...')]
            @py_assert5 = @py_assert3 == @py_assert6
            if not @py_assert5:
                @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.info\n}.call_args_list\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(log_mock) if 'log_mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log_mock) else 'log_mock'}
                @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
            @py_assert1 = log_mock.warning
            @py_assert3 = @py_assert1.call_args_list
            @py_assert6 = [
             mock.call('warning')]
            @py_assert5 = @py_assert3 == @py_assert6
            if not @py_assert5:
                @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.warning\n}.call_args_list\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(log_mock) if 'log_mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log_mock) else 'log_mock'}
                @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
            @py_assert1 = log_mock.error
            @py_assert3 = @py_assert1.call_args_list
            @py_assert6 = [
             mock.call('error')]
            @py_assert5 = @py_assert3 == @py_assert6
            if not @py_assert5:
                @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.error\n}.call_args_list\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(log_mock) if 'log_mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(log_mock) else 'log_mock'}
                @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None