# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/base_models/tests/test_status_mixin.py
# Compiled at: 2014-12-31 04:01:40
import django
from django.utils import timezone
from kii.app.tests import base
from kii.tests import test_base_models
from ..forms import StatusMixinForm

class TestStatusMixin(base.BaseTestCase):

    def test_setting_status_to_published_set_publication_date(self):
        m = self.G(test_base_models.models.StatusModel, status='dra')
        self.assertEqual(m.publication_date, None)
        now = timezone.now()
        m.status = 'pub'
        m.save()
        self.assertEqual(m.publication_date > now, True)
        return


class TestStatusMixinForm(base.BaseTestCase):

    def test_form(self):
        form_data = {'status': 'dra'}
        form = StatusMixinForm(data=form_data)
        self.assertEqual(form.is_valid(), True)