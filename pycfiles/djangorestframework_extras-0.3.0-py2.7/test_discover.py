# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest_framework_extras/tests/test_discover.py
# Compiled at: 2018-04-26 08:15:23
import unittest
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from rest_framework_extras import get_settings

class DiscoverTestCase(unittest.TestCase):

    def test_discovered(self):
        from rest_framework_extras.tests.urls import router
        n = 0
        for name, klass, model_name in router.registry:
            if name == 'tests-vanilla':
                self.assertEqual(klass.__name__, 'TestsVanillaViewSet')
                n += 1
            elif name == 'tests-withform':
                self.assertEqual(klass.__name__, 'TestsWithFormViewSet')
                n += 1
            elif name == 'tests-withadminclass':
                self.assertEqual(klass.__name__, 'TestsWithAdminClassViewSet')
                n += 1
            elif name == 'tests-bar':
                self.assertEqual(klass.__name__, 'TestsBarViewSet')
                n += 1

        if n != 4:
            self.fail('Found %s of 4 items in router registry' % n)

    def test_blacklist(self):
        from rest_framework_extras.tests.urls import router
        for name, klass, model_name in router.registry:
            self.failIf(name in get_settings()['blacklist'])