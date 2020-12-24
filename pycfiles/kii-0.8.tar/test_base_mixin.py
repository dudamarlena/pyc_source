# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/base_models/tests/test_base_mixin.py
# Compiled at: 2014-12-31 04:01:40
from kii.app.tests import base
from kii.tests import test_base_models
import django

class TestBaseMixin(base.BaseTestCase):

    def test_can_get_url_namespace(self):
        m = test_base_models.models.TitleModel(title='Hello world!')
        m.save()
        self.assertEqual(m.url_namespace(), 'kii:test_base_models:titlemodel:')

    def test_model_reverse(self):
        m = test_base_models.models.TitleModel(title='Hello world!')
        m.save()
        self.assertEqual(m.reverse('detail'), ('/kii/test_base_models/titlemodel/{0}/').format(m.pk))
        self.assertEqual(m.reverse('list'), '/kii/test_base_models/titlemodel/')

    def test_model_class_reverse(self):
        m = test_base_models.models.TitleModel
        self.assertEqual(m.class_reverse('list'), '/kii/test_base_models/titlemodel/')