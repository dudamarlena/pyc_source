# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/base_models/tests/test_templates.py
# Compiled at: 2014-10-22 09:35:57
# Size of source mod 2**32: 1636 bytes
from kii.app.tests import base
from kii.tests import test_base_models
import django
from django.core.urlresolvers import reverse

class TestTemplates(base.BaseTestCase):

    def test_model_detail_uses_basemixin_detail(self):
        m = self.G(test_base_models.models.TitleModel2, title='hello')
        url = reverse('kii:test_base_models:titlemodel2:detail', kwargs={'pk': m.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'base_models/basemixin/detail.html')

    def test_model_delete_uses_basemixin_delete(self):
        m = self.G(test_base_models.models.TitleModel2, title='hello')
        url = reverse('kii:test_base_models:titlemodel2:delete', kwargs={'pk': m.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'base_models/basemixin/delete.html')

    def test_model_list_uses_basemixin_list(self):
        url = reverse('kii:test_base_models:titlemodel2:list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'base_models/basemixin/list.html')

    def test_model_create_uses_basemixin_create(self):
        url = reverse('kii:test_base_models:titlemodel2:create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'base_models/basemixin/create.html')

    def test_model_list_uses_basemixin_list_item(self):
        m = self.G(test_base_models.models.TitleModel2, title='hello')
        url = reverse('kii:test_base_models:titlemodel2:list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'base_models/basemixin/list_item.html')