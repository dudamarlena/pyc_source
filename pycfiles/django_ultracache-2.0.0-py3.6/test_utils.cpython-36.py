# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ultracache/tests/test_utils.py
# Compiled at: 2019-12-31 02:49:50
# Size of source mod 2**32: 1505 bytes
from django.conf import settings
from django.core.cache import cache
from django.test import TestCase
from ultracache import _thread_locals
from ultracache.utils import Ultracache
from ultracache.tests.models import DummyModel

class UtilsTestCase(TestCase):
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        fixtures = [
         'sites.json']

    def setUp(self):
        super(UtilsTestCase, self).setUp()
        cache.clear()

    def test_context_manager_like_thing(self):
        one = DummyModel.objects.create(title='One', code='one')
        two = DummyModel.objects.create(title='Two', code='two')
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
        uc = Ultracache(3600, 'c', 'd')
        self.failIf(uc)
        uc.cache(two.title)
        uc = Ultracache(3600, 'c', 'd')
        self.failUnless(uc)
        self.assertEqual(uc.cached, two.title)
        two.title = 'Onez'
        one.save()
        uc = Ultracache(3600, 'c', 'd')
        self.failUnless(uc)
        two.title = 'Twox'
        two.save()
        uc = Ultracache(3600, 'c', 'd')
        self.failIf(uc)