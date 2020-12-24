# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_newsletter/tests/test_sync.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 2269 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest_data import use_data
from ..models import SubscribeTask
from ..external_services.sync import sync_tasks, sync_task

@use_data(cms_qe_mailing_list_data={'external_service': 99}, cms_qe_subscribe_task_data={'attempts': 0, 
 'last_error': 0})
def test_save_failure(cms_qe_subscribe_task):
    @py_assert1 = SubscribeTask.objects
    @py_assert3 = @py_assert1.all
    @py_assert5 = @py_assert3()
    @py_assert7 = @py_assert5.count
    @py_assert9 = @py_assert7()
    @py_assert12 = 1
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.objects\n}.all\n}()\n}.count\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py6': @pytest_ar._saferepr(@py_assert5), 'py13': @pytest_ar._saferepr(@py_assert12), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(SubscribeTask) if 'SubscribeTask' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SubscribeTask) else 'SubscribeTask'}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    result, message = list(sync_tasks())[0]
    @py_assert0 = 'Unsupported service 99'
    @py_assert2 = @py_assert0 in message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, message)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert2 = False
    @py_assert1 = result is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (result, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    cms_qe_subscribe_task.refresh_from_db()
    @py_assert1 = cms_qe_subscribe_task.attempts
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.attempts\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(cms_qe_subscribe_task) if 'cms_qe_subscribe_task' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cms_qe_subscribe_task) else 'cms_qe_subscribe_task'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = cms_qe_subscribe_task.last_error
    @py_assert4 = 'Unsupported service 99'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.last_error\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(cms_qe_subscribe_task) if 'cms_qe_subscribe_task' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cms_qe_subscribe_task) else 'cms_qe_subscribe_task'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@use_data(cms_qe_subscribe_task_data={'attempts': 10})
def test_warning_do_not_increment_failure(cms_qe_subscribe_task):
    @py_assert1 = SubscribeTask.objects
    @py_assert3 = @py_assert1.all
    @py_assert5 = @py_assert3()
    @py_assert7 = @py_assert5.count
    @py_assert9 = @py_assert7()
    @py_assert12 = 1
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.objects\n}.all\n}()\n}.count\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py6': @pytest_ar._saferepr(@py_assert5), 'py13': @pytest_ar._saferepr(@py_assert12), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(SubscribeTask) if 'SubscribeTask' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SubscribeTask) else 'SubscribeTask'}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    result, message = list(sync_tasks())[0]
    @py_assert0 = 'Skipped'
    @py_assert2 = @py_assert0 in message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, message)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert2 = None
    @py_assert1 = result is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (result, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    cms_qe_subscribe_task.refresh_from_db()
    @py_assert1 = cms_qe_subscribe_task.attempts
    @py_assert4 = 10
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.attempts\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(cms_qe_subscribe_task) if 'cms_qe_subscribe_task' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cms_qe_subscribe_task) else 'cms_qe_subscribe_task'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = cms_qe_subscribe_task.last_error
    @py_assert4 = ''
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.last_error\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(cms_qe_subscribe_task) if 'cms_qe_subscribe_task' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cms_qe_subscribe_task) else 'cms_qe_subscribe_task'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@use_data(cms_qe_subscribe_task_data={'attempts': 10})
def test_task_skip(cms_qe_subscribe_task):
    result, message = sync_task(cms_qe_subscribe_task)
    @py_assert0 = 'Skipped'
    @py_assert2 = @py_assert0 in message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, message)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert2 = None
    @py_assert1 = result is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (result, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@use_data(cms_qe_mailing_list_data={'external_service': 99}, cms_qe_subscribe_task_data={'attempts': 0, 
 'last_error': 0})
def test_task_unsupported_service(cms_qe_subscribe_task):
    result, message = sync_task(cms_qe_subscribe_task)
    @py_assert0 = 'Unsupported service 99'
    @py_assert2 = @py_assert0 in message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, message)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert2 = False
    @py_assert1 = result is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (result, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@use_data(cms_qe_subscribe_task_data={'email': '-no-subscriber-@example.com'})
def test_task_with_removed_subscriber(cms_qe_subscribe_task):
    result, message = sync_task(cms_qe_subscribe_task)
    @py_assert0 = 'Subscriber does not exist anymore, deleting task'
    @py_assert2 = @py_assert0 in message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, message)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert2 = None
    @py_assert1 = result is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (result, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@use_data(cms_qe_subscriber_data={'email': 'test@example.com'}, cms_qe_subscribe_task_data={'email': 'test@example.com'})
def test_task_synced(cms_qe_subscribe_task, cms_qe_subscriber, mock_mailchimp):
    result, message = sync_task(cms_qe_subscribe_task)
    @py_assert0 = 'OK'
    @py_assert2 = @py_assert0 in message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, message)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert2 = True
    @py_assert1 = result is @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (result, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None