# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/tests/test_context_managers.py
# Compiled at: 2019-06-02 16:44:50
# Size of source mod 2**32: 892 bytes
from django.conf import settings
from django.core.cache import cache
from django.test import TestCase
from ultracache import _thread_locals
from ultracache.context_managers import Ultracache
from ultracache.tests.models import DummyModel

class ContextManagerTestCase(TestCase):
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        fixtures = [
         'sites.json']

    def setUp(self):
        super(ContextManagerTestCase, self).setUp()
        cache.clear()

    def test_context_manager(self):
        one = DummyModel.objects.create(title='One', code='one')
        uc = Ultracache(3600, 'a', 'b')
        self.failIf(uc)
        uc.cache(one.title)
        uc = Ultracache(3600, 'a', 'b')
        self.failUnless(uc)
        self.assertEqual(uc.cached, one.title)
        one.title = 'Onex'
        one.save()
        uc = Ultracache(3600, 'a', 'b')
        self.failIf(uc)