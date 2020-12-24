# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/tests/test_modelbase_admin.py
# Compiled at: 2017-05-03 05:57:29
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory
from jmbo.models import ModelBase
from jmbo.admin import ModelBaseAdmin
from jmbo.tests.models import DummyModel

class ModelBaseAdminTestCase(TestCase):
    fixtures = [
     'sites.json']

    @classmethod
    def setUpTestData(cls):
        super(ModelBaseAdminTestCase, cls).setUpTestData()
        cls.user, cls.created = get_user_model().objects.get_or_create(username='test', email='test@test.com')

    def test_field_hookup(self):
        model_admin = ModelBaseAdmin(DummyModel, AdminSite())
        self.failIf('test_editable_field' not in model_admin.fieldsets[0][1]['fields'])
        self.failIf('test_foreign_field' not in model_admin.fieldsets[0][1]['fields'])
        self.failIf('test_many_field' not in model_admin.fieldsets[0][1]['fields'])
        self.failIf('test_non_editable_field' in model_admin.fieldsets[0][1]['fields'])
        self.failIf('test_member' in model_admin.fieldsets[0][1]['fields'])

    def test_save_model(self):
        admin_obj = ModelBaseAdmin(ModelBase, 1)
        request = RequestFactory().get('/')
        request.user = self.user
        obj = ModelBase()
        admin_obj.save_model(request, obj, admin_obj.form, 1)
        self.failUnless(obj.owner == self.user)
        obj.save()