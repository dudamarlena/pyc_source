# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/tests/test_filters.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 569 bytes
from django.test import TestCase
from ovp_users.views.password_recovery import RecoveryTokenFilter
from ovp_users.views.password_recovery import RecoverPasswordFilter

def test_filter(c):
    obj = c()
    obj.filter_queryset('a', 'b', 'c')
    obj.get_fields('a')


class PasswordRecoveryFiltersTestCase(TestCase):

    def test_filters(self):
        """Assert filters do not throw error when instantiated"""
        test_filter(RecoveryTokenFilter)
        test_filter(RecoverPasswordFilter)