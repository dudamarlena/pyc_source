# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/base_models/tests/test_timestamp_mixin.py
# Compiled at: 2014-10-12 10:22:28
# Size of source mod 2**32: 921 bytes
from kii.app.tests import base
from kii.tests import test_base_models
import django
from django.utils import timezone
import datetime

class TestTimestampMixin(base.BaseTestCase):

    def test_creation_and_modification_date(self):
        now = timezone.now()
        m = self.G(test_base_models.models.TimestampModel)
        self.assertEqual(m.created > now, True)
        self.assertEqual(m.last_modified > now, True)

    def test_can_provide_a_value_to_modified_and_not_use_default(self):
        d = datetime.datetime(1992, 10, 8, 4, 30, 25)
        m = self.G(test_base_models.models.TimestampModel, created=d)
        self.assertEqual(m.created, d)

    def test_can_provide_a_value_to_last_modified_and_not_use_default(self):
        d = datetime.datetime(1992, 10, 8, 4, 30, 25)
        m = self.G(test_base_models.models.TimestampModel, last_modified=d)
        self.assertEqual(m.last_modified, d)