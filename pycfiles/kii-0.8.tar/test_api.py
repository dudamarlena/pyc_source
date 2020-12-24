# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/api/tests/test_api.py
# Compiled at: 2014-12-31 04:01:40
from kii.app.tests import base
from django.core.urlresolvers import reverse

class TestBaseMixin(base.BaseTestCase):

    def test_can_collect_api_views(self):
        reverse('kii:api:test_api0:index')
        reverse('kii:api:test_api1:index')