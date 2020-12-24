# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/senko/tenants/tcms_tenants/tests/__init__.py
# Compiled at: 2019-05-05 08:45:29
# Size of source mod 2**32: 1346 bytes
from django.conf import settings
import factory
from factory.django import DjangoModelFactory
from django_tenants.test.client import TenantClient
from django_tenants.test.cases import FastTenantTestCase

class UserFactory(DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda n: 'User%d' % n)
    email = factory.LazyAttribute(lambda user: '%s@kiwitcms.org' % user.username)
    is_active = True
    is_staff = True


class LoggedInTestCase(FastTenantTestCase):

    @classmethod
    def setup_tenant(cls, tenant):
        tenant.owner = UserFactory()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tenant.authorized_users.add(cls.tenant.owner)
        cls.tester = UserFactory()
        cls.tester.set_password('password')
        cls.tester.save()
        cls.tenant.authorized_users.add(cls.tester)

    def setUp(self):
        super().setUp()
        self.client = TenantClient(self.tenant)
        self.client.login(username=(self.tester.username), password='password')