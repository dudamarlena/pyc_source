# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/base_models/tests/test_owner_mixin.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 3277 bytes
from kii.user.tests import base
from kii.tests import test_base_models
import django
from django.conf import settings

class TestOwnerMixin(base.UserTestCase):

    def test_owner_is_required(self):
        m = test_base_models.models.OwnerModel()
        with self.assertRaises(django.db.IntegrityError):
            m.save()

    def test_can_retrieve_owned_item_via_user(self):
        m = self.G(test_base_models.models.OwnerModel, owner=self.users[0])
        self.assertEqual(m, self.users[0].ownermodels.first())

    def test_owned_item_is_deleted_with_user(self):
        m = self.G(test_base_models.models.OwnerModel, owner=self.users[0])
        pk = m.pk
        self.users[0].delete()
        with self.assertRaises(test_base_models.models.OwnerModel.DoesNotExist):
            test_base_models.models.OwnerModel.objects.get(pk=pk)

    def test_can_check_if_user_is_owner_of_object(self):
        m = self.G(test_base_models.models.OwnerModel, owner=self.users[0])
        self.assertEqual(m.owned_by(self.users[0]), True)

    def test_owner_mixin_create_requires_authenticated_user(self):
        url = test_base_models.models.OwnerModel.class_reverse('create')
        response = self.client.get(url)
        self.assertRedirectsLogin(response, url)
        self.login(self.users[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_owner_mixin_create_view_set_owner_to_request_user(self):
        url = test_base_models.models.OwnerModel.class_reverse('create')
        self.login(self.users[0])
        response = self.client.post(url, {'useless_field': 'myinstance'})
        i = test_base_models.models.OwnerModel.objects.get(useless_field='myinstance')
        self.assertEqual(i.owner, self.users[0])

    def test_owner_mixin_update_requires_owner(self):
        instance = self.G(test_base_models.models.OwnerModel, owner=self.users[0])
        url = instance.reverse('update')
        response = self.client.get(url)
        self.assertRedirectsLogin(response, url)
        self.login(self.users[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.logout()
        self.login(self.users[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_owner_mixin_delete_requires_owner(self):
        instance = self.G(test_base_models.models.OwnerModel, owner=self.users[0])
        url = instance.reverse('delete')
        response = self.client.get(url)
        self.assertRedirectsLogin(response, url)
        self.login(self.users[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.logout()
        self.login(self.users[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)