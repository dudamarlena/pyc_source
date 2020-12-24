# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ultracache/tests/test_drf.py
# Compiled at: 2019-12-31 02:49:50
# Size of source mod 2**32: 5648 bytes
import copy, json
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient
from ultracache.tests.models import DummyModel
from ultracache.tests.viewsets import DummyViewSet

class DRFTestCase(TestCase):
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        fixtures = [
         'sites.json']

    @classmethod
    def setUpTestData(cls):
        super(DRFTestCase, cls).setUpTestData()
        cls.user_model = get_user_model()
        cls.superuser = cls.user_model.objects.create(username='superuser',
          email='superuser@test.com',
          is_superuser=True,
          is_staff=True)
        cls.superuser.set_password('password')
        cls.superuser.save()
        cls.staff = cls.user_model.objects.create(username='staff',
          email='staff@test.com',
          is_staff=True)
        cls.staff.set_password('password')
        cls.staff.save()
        cls.user = cls.user_model.objects.create(username='user',
          email='user@test.com')
        cls.user.set_password('password')
        cls.user.save()

    def setUp(self):
        super(DRFTestCase, self).setUp()
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.client.logout()
        self.one = DummyModel.objects.create(title='One', code='one')
        self.two = DummyModel.objects.create(title='Two', code='two')

    def tearDown(self):
        self.client.logout()
        DummyModel.objects.all().delete()
        super(DRFTestCase, self).tearDown()

    def test_get_dummymodels(self):
        response = self.client.get('/api/dummies/')
        as_json_1 = response.json()
        DummyModel.objects.filter(pk=(self.one.pk)).update(title='Onae')
        response = self.client.get('/api/dummies/')
        as_json_2 = response.json()
        self.assertEqual(as_json_1, as_json_2)
        self.one.title = 'Onbe'
        self.one.save()
        response = self.client.get('/api/dummies/')
        as_json_3 = response.json()
        self.assertNotEqual(as_json_1, as_json_3)
        response = self.client.get('/api/dummies/')
        as_json_4 = response.json()
        self.assertEqual(as_json_3, as_json_4)
        data = {'title': 'Onze'}
        response = self.client.patch('/api/dummies/%s/' % self.one.pk, data)
        response = self.client.get('/api/dummies/')
        as_json_5 = response.json()
        self.assertNotEqual(as_json_4, as_json_5)
        DummyModel.objects.filter(pk=(self.one.pk)).update(title='Once')
        di = copy.deepcopy(settings.ULTRACACHE)
        di['drf'] = {'viewsets': {'*': {'evaluate': 'request.user.is_anonymous'}}}
        with override_settings(ULTRACACHE=di):
            response = self.client.get('/api/dummies/')
            as_json_6 = response.json()
            self.assertNotEqual(as_json_5, as_json_6)
        response = self.client.get('/api/dummies/')
        as_json_7 = response.json()
        DummyModel.objects.filter(pk=(self.one.pk)).update(title='Onde')
        di = copy.deepcopy(settings.ULTRACACHE)
        di['drf'] = {'viewsets': {object: {}}}
        with override_settings(ULTRACACHE=di):
            response = self.client.get('/api/dummies/')
            as_json_8 = response.json()
            self.assertNotEqual(as_json_7, as_json_8)
        response = self.client.get('/api/dummies/')
        as_json_9 = response.json()
        DummyModel.objects.filter(pk=(self.one.pk)).update(title='Onee')
        di = copy.deepcopy(settings.ULTRACACHE)
        di['drf'] = {'viewsets': {DummyViewSet: {}}}
        with override_settings(ULTRACACHE=di):
            response = self.client.get('/api/dummies/')
            as_json_10 = response.json()
            self.assertEqual(as_json_9, as_json_10)

    def test_get_dummymodel(self):
        url = '/api/dummies/%s/' % self.one.pk
        response = self.client.get(url)
        as_json_1 = response.json()
        DummyModel.objects.filter(pk=(self.one.pk)).update(title='Onfe')
        response = self.client.get(url)
        as_json_2 = response.json()
        self.assertEqual(as_json_1, as_json_2)
        self.one.title = 'Onge'
        self.one.save()
        response = self.client.get(url)
        as_json_3 = response.json()
        self.assertNotEqual(as_json_1, as_json_3)