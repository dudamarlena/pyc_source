# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/auth/tests/basic.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import locale
from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands import createsuperuser
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.tests.custom_user import CustomUser
from django.contrib.auth.tests.utils import skipIfCustomUser
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.encoding import force_str
from django.utils.six import binary_type, PY3, StringIO

def mock_inputs(inputs):
    """
    Decorator to temporarily replace input/getpass to allow interactive
    createsuperuser.
    """

    def inner(test_func):

        def wrapped(*args):

            class mock_getpass:

                @staticmethod
                def getpass(prompt=b'Password: ', stream=None):
                    assert PY3 or isinstance(prompt, binary_type)
                    return inputs[b'password']

            def mock_input(prompt):
                prompt = str(prompt)
                assert str(b'__proxy__') not in prompt
                response = b''
                for key, val in inputs.items():
                    if force_str(key) in prompt.lower():
                        response = val
                        break

                return response

            old_getpass = createsuperuser.getpass
            old_input = createsuperuser.input
            createsuperuser.getpass = mock_getpass
            createsuperuser.input = mock_input
            try:
                test_func(*args)
            finally:
                createsuperuser.getpass = old_getpass
                createsuperuser.input = old_input

        return wrapped

    return inner


@skipIfCustomUser
class BasicTestCase(TestCase):

    def test_user(self):
        """Check that users can be created and can set their password"""
        u = User.objects.create_user(b'testuser', b'test@example.com', b'testpw')
        self.assertTrue(u.has_usable_password())
        self.assertFalse(u.check_password(b'bad'))
        self.assertTrue(u.check_password(b'testpw'))
        u.set_unusable_password()
        u.save()
        self.assertFalse(u.check_password(b'testpw'))
        self.assertFalse(u.has_usable_password())
        u.set_password(b'testpw')
        self.assertTrue(u.check_password(b'testpw'))
        u.set_password(None)
        self.assertFalse(u.has_usable_password())
        self.assertTrue(u.is_authenticated())
        self.assertFalse(u.is_staff)
        self.assertTrue(u.is_active)
        self.assertFalse(u.is_superuser)
        u2 = User.objects.create_user(b'testuser2', b'test2@example.com')
        self.assertFalse(u2.has_usable_password())
        return

    def test_user_no_email(self):
        """Check that users can be created without an email"""
        u = User.objects.create_user(b'testuser1')
        self.assertEqual(u.email, b'')
        u2 = User.objects.create_user(b'testuser2', email=b'')
        self.assertEqual(u2.email, b'')
        u3 = User.objects.create_user(b'testuser3', email=None)
        self.assertEqual(u3.email, b'')
        return

    def test_anonymous_user(self):
        """Check the properties of the anonymous user"""
        a = AnonymousUser()
        self.assertEqual(a.pk, None)
        self.assertFalse(a.is_authenticated())
        self.assertFalse(a.is_staff)
        self.assertFalse(a.is_active)
        self.assertFalse(a.is_superuser)
        self.assertEqual(a.groups.all().count(), 0)
        self.assertEqual(a.user_permissions.all().count(), 0)
        return

    def test_superuser(self):
        """Check the creation and properties of a superuser"""
        super = User.objects.create_superuser(b'super', b'super@example.com', b'super')
        self.assertTrue(super.is_superuser)
        self.assertTrue(super.is_active)
        self.assertTrue(super.is_staff)

    def test_createsuperuser_management_command(self):
        """Check the operation of the createsuperuser management command"""
        new_io = StringIO()
        call_command(b'createsuperuser', interactive=False, username=b'joe', email=b'joe@somewhere.org', stdout=new_io)
        command_output = new_io.getvalue().strip()
        self.assertEqual(command_output, b'Superuser created successfully.')
        u = User.objects.get(username=b'joe')
        self.assertEqual(u.email, b'joe@somewhere.org')
        self.assertFalse(u.has_usable_password())
        new_io = StringIO()
        call_command(b'createsuperuser', interactive=False, username=b'joe2', email=b'joe2@somewhere.org', verbosity=0, stdout=new_io)
        command_output = new_io.getvalue().strip()
        self.assertEqual(command_output, b'')
        u = User.objects.get(username=b'joe2')
        self.assertEqual(u.email, b'joe2@somewhere.org')
        self.assertFalse(u.has_usable_password())
        call_command(b'createsuperuser', interactive=False, username=b'joe+admin@somewhere.org', email=b'joe@somewhere.org', verbosity=0)
        u = User.objects.get(username=b'joe+admin@somewhere.org')
        self.assertEqual(u.email, b'joe@somewhere.org')
        self.assertFalse(u.has_usable_password())

    @mock_inputs({b'password': b'nopasswd'})
    def test_createsuperuser_nolocale(self):
        """
        Check that createsuperuser does not break when no locale is set. See
        ticket #16017.
        """
        old_getdefaultlocale = locale.getdefaultlocale
        try:
            try:
                locale.getdefaultlocale = lambda : (None, None)
                call_command(b'createsuperuser', interactive=True, username=b'nolocale@somewhere.org', email=b'nolocale@somewhere.org', verbosity=0)
            except TypeError:
                self.fail(b'createsuperuser fails if the OS provides no information about the current locale')

        finally:
            locale.getdefaultlocale = old_getdefaultlocale

        u = User.objects.get(username=b'nolocale@somewhere.org')
        self.assertEqual(u.email, b'nolocale@somewhere.org')

    @mock_inputs({b'password': b'nopasswd', 
       b'uživatel': b'foo', 
       b'email': b'nolocale@somewhere.org'})
    def test_createsuperuser_non_ascii_verbose_name(self):
        from django.utils.translation import ugettext_lazy as ulazy
        username_field = User._meta.get_field(b'username')
        old_verbose_name = username_field.verbose_name
        username_field.verbose_name = ulazy(b'uživatel')
        new_io = StringIO()
        try:
            call_command(b'createsuperuser', interactive=True, stdout=new_io)
        finally:
            username_field.verbose_name = old_verbose_name

        command_output = new_io.getvalue().strip()
        self.assertEqual(command_output, b'Superuser created successfully.')

    def test_get_user_model(self):
        """The current user model can be retrieved"""
        self.assertEqual(get_user_model(), User)

    @override_settings(AUTH_USER_MODEL=b'auth.CustomUser')
    def test_swappable_user(self):
        """The current user model can be swapped out for another"""
        self.assertEqual(get_user_model(), CustomUser)
        with self.assertRaises(AttributeError):
            User.objects.all()

    @override_settings(AUTH_USER_MODEL=b'badsetting')
    def test_swappable_user_bad_setting(self):
        """The alternate user setting must point to something in the format app.model"""
        with self.assertRaises(ImproperlyConfigured):
            get_user_model()

    @override_settings(AUTH_USER_MODEL=b'thismodel.doesntexist')
    def test_swappable_user_nonexistent_model(self):
        """The current user model must point to an installed model"""
        with self.assertRaises(ImproperlyConfigured):
            get_user_model()