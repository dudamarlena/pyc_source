# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-country-dialcode/country_dialcode/tests/utils.py
# Compiled at: 2014-07-16 08:09:37
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.test.client import RequestFactory
import base64, unittest

def build_test_suite_from(test_cases):
    """Returns a single or group of unittest test suite(s) that's ready to be
    run. The function expects a list of classes that are subclasses of
    TestCase.

    The function will search the module where each class resides and
    build a test suite from that class and all subclasses of it.
    """
    test_suites = []
    for test_case in test_cases:
        mod = __import__(test_case.__module__)
        components = test_case.__module__.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)

        tests = []
        for item in mod.__dict__.values():
            if type(item) is type and issubclass(item, test_case):
                tests.append(item)

        test_suites.append(unittest.TestSuite(map(unittest.TestLoader().loadTestsFromTestCase, tests)))

    return unittest.TestSuite(test_suites)


class BaseAuthenticatedClient(TestCase):
    """Common Authentication"""
    fixtures = [
     'auth_user.json']

    def setUp(self):
        """To create admin user"""
        self.client = Client()
        self.user = User.objects.get(username='admin')
        auth = '%s:%s' % ('admin', 'admin')
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()
        self.extra = {'HTTP_AUTHORIZATION': auth}
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        self.factory = RequestFactory()