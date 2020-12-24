# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cache_headers/tests/test_middleware.py
# Compiled at: 2018-07-07 04:58:09
from django.contrib import auth
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation
from django.test import TestCase
from django.urls import reverse, reverse_lazy
all_users = reverse_lazy('all-users')
anonymous_only = reverse_lazy('anonymous-only')
anonymous_and_authenticated = reverse_lazy('anonymous-and-authenticated')
per_user = reverse_lazy('per-user')
custom_policy = reverse_lazy('custom-policy')
mylogin = reverse_lazy('mylogin')
mylogout = reverse_lazy('mylogout')

class CacheMiddlewareTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(CacheMiddlewareTest, cls).setUpTestData()
        cls.user = get_user_model().objects.create(username='user', email='user@test.com', is_active=True)
        cls.user.set_password('password')
        cls.user.save()

    def setUp(self):
        super(CacheMiddlewareTest, self).setUp()
        self.client.logout()

    def login(self):
        self.client.login(username='user', password='password')

    def test_auth_states(self):
        """We never cache during login or logout"""
        response = self.client.get(all_users)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'max-age=100, s-maxage=600'))
        response = self.client.post(mylogin, {'username': 'user', 'password': 'password'})
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'no-cache'))
        response = self.client.get(all_users)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'max-age=100, s-maxage=600'))
        response = self.client.get(mylogout)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'no-cache'))
        response = self.client.get(all_users)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'max-age=100, s-maxage=600'))

    def test_tampering(self):
        """Reject spoofed sessionid cookies by anonymous users"""
        self.client.cookies.load({settings.SESSION_COOKIE_NAME: '123'})
        response = self.client.get(all_users)
        self.assertEqual(response.status_code, 400)

    def test_all_users(self):
        response = self.client.get(all_users)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'max-age=100, s-maxage=600'))
        self.assertEqual(response._headers['x-accel-expires'], ('X-Accel-Expires',
                                                                '600'))
        self.login()
        response = self.client.get(all_users)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'max-age=100, s-maxage=600'))
        self.assertEqual(response._headers['x-accel-expires'], ('X-Accel-Expires',
                                                                '600'))

    def test_anonymous_only(self):
        response = self.client.get(anonymous_only)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'max-age=100, s-maxage=600'))
        self.assertEqual(response._headers['x-accel-expires'], ('X-Accel-Expires',
                                                                '600'))
        self.assertEqual(response._headers['x-hash-cookies'], ('X-Hash-Cookies', 'messages|isauthenticated'))
        self.login()
        response = self.client.get(anonymous_only)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'no-cache'))

    def test_anonymous_and_authenticated(self):
        response = self.client.get(anonymous_and_authenticated)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'max-age=100, s-maxage=600'))
        self.assertEqual(response._headers['x-accel-expires'], ('X-Accel-Expires',
                                                                '600'))
        self.assertEqual(response._headers['x-hash-cookies'], ('X-Hash-Cookies', 'messages|isauthenticated'))
        self.login()
        response = self.client.get(anonymous_and_authenticated)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'max-age=100, s-maxage=600'))
        self.assertEqual(response._headers['x-accel-expires'], ('X-Accel-Expires',
                                                                '600'))
        self.assertEqual(response._headers['x-hash-cookies'], ('X-Hash-Cookies', 'messages|isauthenticated'))

    def test_anonymous_and_authenticated_login_path(self):
        di = settings.CACHE_HEADERS.copy()
        di['enable-tampering-checks'] = True
        with self.settings(CACHE_HEADERS=di):
            response = self.client.post(mylogin, {'username': 'user', 'password': 'password'}, follow=True)
            self.assertEqual(response._headers['cache-control'], ('Cache-Control',
                                                                  'no-cache'))
            user = auth.get_user(response.client)
            self.assertTrue(user.is_authenticated)
            self.assertEqual(user, self.user)
            response = self.client.get(anonymous_and_authenticated)
            self.assertEqual(response._headers['cache-control'], ('Cache-Control',
                                                                  'max-age=100, s-maxage=600'))
            self.assertEqual(response._headers['x-accel-expires'], ('X-Accel-Expires',
                                                                    '600'))
            self.assertEqual(response._headers['x-hash-cookies'], ('X-Hash-Cookies',
                                                                   'messages|isauthenticated'))
            user = auth.get_user(response.client)
            self.assertTrue(user.is_authenticated)
            self.assertEqual(user, self.user)
            response = self.client.get(mylogout, follow=True)
            self.assertEqual(response._headers['cache-control'], ('Cache-Control',
                                                                  'no-cache'))
            self.assertTrue(len(response.client.session.keys()) == 0)
            response = self.client.get(anonymous_and_authenticated)
            self.assertEqual(response._headers['cache-control'], ('Cache-Control',
                                                                  'max-age=100, s-maxage=600'))
            self.assertEqual(response._headers['x-accel-expires'], ('X-Accel-Expires',
                                                                    '600'))
            self.assertEqual(response._headers['x-hash-cookies'], ('X-Hash-Cookies',
                                                                   'messages|isauthenticated'))
            self.assertTrue(len(response.client.session.keys()) == 0)

    def test_per_user(self):
        response = self.client.get(per_user)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'max-age=100, s-maxage=600'))
        self.assertEqual(response._headers['x-accel-expires'], ('X-Accel-Expires',
                                                                '600'))
        self.assertEqual(response._headers['x-hash-cookies'], (
         'X-Hash-Cookies', 'messages|%s' % settings.SESSION_COOKIE_NAME))
        self.login()
        response = self.client.get(per_user)
        self.assertEqual(response._headers['cache-control'], ('Cache-Control', 'max-age=100, s-maxage=600'))
        self.assertEqual(response._headers['x-accel-expires'], ('X-Accel-Expires',
                                                                '600'))
        self.assertEqual(response._headers['x-hash-cookies'], (
         'X-Hash-Cookies', 'messages|%s' % settings.SESSION_COOKIE_NAME))

    def test_custom_policy(self):
        response = self.client.get(custom_policy)
        self.assertEqual(response._headers['x-is-special-user'], ('X-Is-Special-User',
                                                                  '0'))
        self.failUnless('X-Is-Special-User' in response._headers['vary'][1])
        self.login()
        response = self.client.get(custom_policy)
        self.assertEqual(response._headers['x-is-special-user'], ('X-Is-Special-User',
                                                                  '1'))
        self.failUnless('X-Is-Special-User' in response._headers['vary'][1])