# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_newsletter/tests/test_mailchimp.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1042 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from constance.test import override_config
from django.conf import settings
import pytest
from pytest_data import use_data
from ..external_services.mailchimp import sync_mailing_lists, sync_subscribe, sync_unsubscribe
from ..models import MailingList

@pytest.mark.slow
@override_config(MAILCHIMP_USERNAME=settings.TEST_MAILCHIMP_USERNAME, MAILCHIMP_API_KEY=settings.TEST_MAILCHIMP_API_KEY)
def test_sync_mailing_lists_integrate():
    _test_sync_mailing_lists()


def test_sync_mailing_lists(mock_mailchimp):
    _test_sync_mailing_lists()


def _test_sync_mailing_lists():
    @py_assert1 = MailingList.objects
    @py_assert3 = @py_assert1.count
    @py_assert5 = @py_assert3()
    @py_assert8 = 0
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.objects\n}.count\n}()\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(MailingList) if 'MailingList' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MailingList) else 'MailingList'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    sync_mailing_lists()
    @py_assert1 = MailingList.objects
    @py_assert3 = @py_assert1.count
    @py_assert5 = @py_assert3()
    @py_assert8 = 2
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.objects\n}.count\n}()\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(MailingList) if 'MailingList' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MailingList) else 'MailingList'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


@use_data(cms_qe_mailchimp_subscribe_data={'id': 'subid'})
def test_sync_subscribe(mock_mailchimp):
    @py_assert0 = 'subid'
    @py_assert4 = 'listid'
    @py_assert6 = 'test@example.com'
    @py_assert8 = 'first'
    @py_assert10 = 'last'
    @py_assert12 = sync_subscribe(@py_assert4, @py_assert6, @py_assert8, @py_assert10)
    @py_assert2 = @py_assert0 == @py_assert12
    if not @py_assert2:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py13)s\n{%(py13)s = %(py3)s(%(py5)s, %(py7)s, %(py9)s, %(py11)s)\n}', ), (@py_assert0, @py_assert12)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(@py_assert0), 'py11': @pytest_ar._saferepr(@py_assert10), 'py3': @pytest_ar._saferepr(sync_subscribe) if 'sync_subscribe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sync_subscribe) else 'sync_subscribe', 'py5': @pytest_ar._saferepr(@py_assert4), 'py13': @pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_sync_unsubscribe(mock_mailchimp):
    sync_unsubscribe('listid', 'test@example.com')