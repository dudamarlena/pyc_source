# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/base_models/tests/test_content_mixin.py
# Compiled at: 2014-12-31 04:01:40
import django
from kii.app.tests import base
from kii.tests import test_base_models
from kii.tests.test_base_models import forms

class TestContentMixin(base.BaseTestCase):

    def test_get_renderered_field(self):
        m = self.G(test_base_models.models.ContentModel, content='#hello')
        self.assertEqual(m.content.rendered, '<h1>hello</h1>')

    def test_raw_field(self):
        m = self.G(test_base_models.models.ContentModel, content='#hello')
        self.assertEqual(m.content.raw, '#hello')


class TestContentMixinForm(base.BaseTestCase):

    def test_form(self):
        form_data = {'content': 'test'}
        form = forms.ContentModelForm(data=form_data)
        self.assertEqual(form.is_valid(), True)