# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/tests/tests_fn_billing.py
# Compiled at: 2019-02-28 16:17:24
# Size of source mod 2**32: 698 bytes
from django.test import TestCase
from django.contrib.auth.models import User

class BillingAdminListViewTestCase(TestCase):
    __doc__ = ' Test billing model admin view '
    fixtures = ['test_billing_admin.yaml']

    def test_coworker_name_link_to_user(self):
        """ Test link to user view in BillAdmin list view """
        admin = User.objects.get(pk=1)
        self.client.force_login(admin)
        response = self.client.get('/admin/billjobs/bill/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<td class="field-coworker_name_link"><a href="/admin/auth/user/1/change/">Bill Jobs</a></td>')