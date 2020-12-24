# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_newsletter/tests/test_views.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 449 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from ..models import MailingList

def test_get_lists_from_mailchimp(mock_mailchimp, admin_client):
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
    admin_client.get('/cms-qe/newsletter/sync-lists')
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


def test_get_lists_from_mailchimp_not_staff(mock_mailchimp, client):
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
    client.get('/cms-qe/newsletter/sync-lists')
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