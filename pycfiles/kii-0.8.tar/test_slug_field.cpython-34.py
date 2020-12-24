# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/base_models/tests/test_slug_field.py
# Compiled at: 2014-10-23 06:59:01
# Size of source mod 2**32: 355 bytes
from __future__ import unicode_literals
from kii.app.tests import base
from kii.tests import test_base_models
import django

class TestSlugField(base.BaseTestCase):

    def test_can_set_slug_from_other_field(self):
        m = self.G(test_base_models.models.SlugModel, title='This is my title')
        self.assertEqual(m.slug, 'this-is-my-title')