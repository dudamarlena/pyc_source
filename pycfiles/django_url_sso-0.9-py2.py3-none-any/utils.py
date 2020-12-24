# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drbob/Development/hap-intra/env/src/django-url-sso/url_sso/tests/utils.py
# Compiled at: 2014-02-06 10:16:17
""" Test utils """
from django.test.client import RequestFactory
from django.contrib.auth.models import User

class UserTestMixin(object):
    """ TestCase mixin for tests requiring a logged in user. """

    def setUp(self):
        """ Create a local user and login """
        self.user = User.objects.create_user(username='john', email='john_lennon@beatles.com', password='top_secret')
        login_success = self.client.login(username='john', password='top_secret')
        assert login_success, 'Test login failed. Tests are broken.'
        super(UserTestMixin, self).setUp()


class RequestTestMixin(object):
    """ TestCase mixin for tests requiring a request. """

    def setUp(self):
        """ Create request object for '/' URL """
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        super(RequestTestMixin, self).setUp()