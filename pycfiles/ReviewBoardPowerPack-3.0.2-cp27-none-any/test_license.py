# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/tests/test_license.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from cStringIO import StringIO
from datetime import datetime, timedelta
from django.test import TestCase
from beanbag_licensing.keys import TEST_PUBLIC_KEY
from beanbag_licensing.license import License
from beanbag_licensing.tests.keys import test_private_key

class LicenseTests(TestCase):
    """Unit tests for beanbag_licensing.license.License."""

    def test_has_user_cap_with_cap(self):
        """Testing License.has_user_cap with cap"""
        license = License(users=5)
        self.assertTrue(license.has_user_cap)

    def test_has_user_cap_without_cap(self):
        """Testing License.has_user_cap without cap"""
        license = License(users=0)
        self.assertFalse(license.has_user_cap)

    def test_has_user_cap_with_cap_in_perpetual_user_mode(self):
        """Testing License.has_user_cap with cap in perpetual user mode"""
        license = License(users=5, perpetual_user_count=2, trial=True, expiration=datetime.utcnow() - timedelta(days=5))
        self.assertTrue(license.has_user_cap)

    def test_user_cap(self):
        """Testing License.user_cap"""
        license = License(users=5)
        self.assertEqual(license.user_cap, 5)

    def test_user_cap_with_perpetual_users_count(self):
        """Testing License.user_cap with perpetual_users count"""
        license = License(users=5, perpetual_users=2, expiration=datetime.utcnow() + timedelta(days=5))
        self.assertEqual(license.user_cap, 7)

    def test_user_cap_in_perpetual_user_mode(self):
        """Testing License.user_cap with in_perpetual_users mode"""
        license = License(users=5, perpetual_users=2, trial=True, expiration=datetime.utcnow() - timedelta(days=5), grace_period=0)
        self.assertEqual(license.user_cap, 2)

    def test_expired_before_expiration(self):
        """Testing License.expired before expiration date"""
        license = License(expiration=datetime.utcnow() + timedelta(minutes=1), grace_period=3)
        self.assertFalse(license.expired)

    def test_expired_after_expiration(self):
        """Testing License.expired after expiration date"""
        license = License(expiration=datetime.utcnow() - timedelta(minutes=1), grace_period=3)
        self.assertTrue(license.expired)

    def test_expired_with_unlicensed(self):
        """Testing License.expired with unlicensed state"""
        license = License.make_unlicensed(product=b'MyProduct')
        self.assertFalse(license.expired)

    def test_time_left_with_unlicensed(self):
        """Testing License.time_left with unlicensed state"""
        license = License.make_unlicensed(product=b'MyProduct')
        self.assertFalse(license.time_left)

    def test_hard_expired_before_grace_period(self):
        """Testing License.hard_expired before grace period"""
        license = License(expiration=datetime.utcnow() - timedelta(minutes=1), grace_period=1)
        self.assertFalse(license.hard_expired)

    def test_hard_expired_after_grace_period(self):
        """Testing License.hard_expired after grace period"""
        license = License(expiration=datetime.utcnow() - timedelta(days=2), grace_period=1)
        self.assertTrue(license.hard_expired)

    def test_hard_expired_with_unlicensed(self):
        """Testing License.hard_expired with unlicensed state"""
        license = License.make_unlicensed(product=b'MyProduct')
        self.assertFalse(license.hard_expired)

    def test_in_perpetual_user_mode(self):
        """Testing License.in_perpetual_user_mode in trial mode when hard-expired and has user counts"""
        license = License(expiration=datetime.utcnow() - timedelta(days=2), perpetual_users=2, trial=True)
        self.assertTrue(license.in_perpetual_user_mode)

    def test_in_perpetual_user_mode_and_trial_hard_expired_no_users(self):
        """Testing License.in_perpetual_user_mode in trial mode when hard-expired and no user counts"""
        license = License(expiration=datetime.utcnow() - timedelta(days=2), trial=True)
        self.assertFalse(license.in_perpetual_user_mode)

    def test_in_perpetual_user_mode_not_expired(self):
        """Testing License.in_perpetual_user_mode when not expired"""
        license = License(expiration=datetime.utcnow() + timedelta(days=2), perpetual_users=2, trial=True)
        self.assertFalse(license.in_perpetual_user_mode)

    def test_in_perpetual_user_mode_not_trial(self):
        """Testing License.in_perpetual_user_mode when not trial"""
        license = License(expiration=datetime.utcnow() - timedelta(days=2), perpetual_users=2, trial=False)
        self.assertFalse(license.in_perpetual_user_mode)

    def test_in_perpetual_user_mode_with_unlicensed(self):
        """Testing License.in_perpetual_user_mode when unlicensed"""
        license = License.make_unlicensed(product=b'MyProduct')
        self.assertTrue(license.in_perpetual_user_mode)

    def test_valid_install_key_with_valid_key(self):
        """Testing License.valid_install_key with valid key"""
        license = License(install_keys=[b'abc123'])
        license.activate(b'abc123')
        self.assertTrue(license.valid_install_key)

    def test_valid_install_key_with_invalid_key(self):
        """Testing License.valid_install_key with invalid key"""
        license = License(install_keys=[b'abc123'])
        license.activate(b'def456')
        self.assertFalse(license.valid_install_key)

    def test_valid_install_key_with_empty_install_keys(self):
        """Testing License.valid_install_key with empty install_keys list"""
        license = License(install_keys=[])
        license.activate(b'foo')
        self.assertTrue(license.valid_install_key)

    def test_valid_install_key_with_unlicensed(self):
        """Testing License.valid_install_key with unlicensed state"""
        license = License.make_unlicensed(product=b'MyProduct')
        self.assertTrue(license.valid_install_key)

    def test_valid_with_unlicensed(self):
        """Testing License.valid with unlicensed state"""
        license = License.make_unlicensed(product=b'MyProduct')
        self.assertTrue(license.valid)

    def test_valid_with_unverified_public_key(self):
        """Testing License.valid with unverified license public key"""
        license = License(license_version=2, product=b'Power Pack', company=b'FooCorp', users=10, perpetual_users=2, expiration=datetime.utcnow() + timedelta(days=100), grace_period=3, trial=False, install_keys=[
         b'abc123'])
        encoded_license, signature = license.encode(test_private_key)
        license = License.decode(encoded_license, signature, TEST_PUBLIC_KEY)
        license.activate(b'abc123')
        license._verify_grace_start_time = None
        self.assertFalse(license._verified)
        self.assertFalse(license.valid)
        return

    def test_encode(self):
        """Testing License.encode"""
        license = License(license_version=2, product=b'Power Pack', company=b'FooCorp', users=10, perpetual_users=2, expiration=datetime(2020, 1, 1, 0, 0, 0), grace_period=3, trial=True, install_keys=[
         b'abc123'])
        encoded_license, signature = license.encode(test_private_key)
        self.assertEqual(encoded_license, b'Y19fYnVpbHRpbl9fCmRpY3QKcDEKKHRScDIKVmNvbXBhbnkKcDMKVkZvb0NvcnAKcDQKc1ZleHBpcmF0aW9uCnA1CmNkYXRldGltZQpkYXRldGltZQpwNgooUydceDA3XHhlNFx4MDFceDAxXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwJwp0UnA3CnNWZ3JhY2VfcGVyaW9kCnA4CkkzCnNWaW5zdGFsbF9rZXlzCnA5CihscDEwClZhYmMxMjMKcDExCmFzVmxpY2Vuc2VfdmVyc2lvbgpwMTIKSTIKc1ZwZXJwZXR1YWxfdXNlcnMKcDEzCkkyCnNWcHJvZHVjdApwMTQKVlBvd2VyIFBhY2sKcDE1CnNWdHJpYWwKcDE2CkkwMQpzVnVzZXJzCnAxNwpJMTAKcy4=')
        self.assertEqual(signature, b'spdNw3ugMBT8QB0fVgufMUcy4t5NUVVCXMPgK+yPtkHIej2CRjBBfoQ4xpI1JMNzugmvRAz9gLyeeK4o3JYjq83b9mvtJ/b/O0VtchfM0FkoDZgdwWbyfKqYKWx3elc82XKyK4OOqqYuOs23G8bGx1zmElhsUYj+rBAFyG2adgIhWPbx/aP81QmdTsfmgY6yf4ys2ksAmXo7gj/oRnHkRGSNo+WerbJ9tYdWYd1/kh2Fj3KcKa6rApqJrwm7ZXBNM8kZ3uK5yKN53R8w5Ep4XF9JdktQtL29YHbt6xHFIFv1V/0DuR5MLgc3YBaYmR1Xl5cMl+3hbvC5XVjGXGCXUQ==')

    def test_write(self):
        """Testing License.write"""
        license = License(license_version=2, product=b'Power Pack', company=b'FooCorp', users=10, perpetual_users=2, expiration=datetime(2020, 1, 1, 0, 0, 0), grace_period=3, trial=True, install_keys=[
         b'abc123'])
        s = StringIO()
        license.write(s, test_private_key)
        result = s.getvalue()
        s.close()
        self.assertEqual(result, b'[License]\nlicense = Y19fYnVpbHRpbl9fCmRpY3QKcDEKKHRScDIKVmNvbXBhbnkKcDMKVkZvb0NvcnAKcDQKc1ZleHBpcmF0aW9uCnA1CmNkYXRldGltZQpkYXRldGltZQpwNgooUydceDA3XHhlNFx4MDFceDAxXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwJwp0UnA3CnNWZ3JhY2VfcGVyaW9kCnA4CkkzCnNWaW5zdGFsbF9rZXlzCnA5CihscDEwClZhYmMxMjMKcDExCmFzVmxpY2Vuc2VfdmVyc2lvbgpwMTIKSTIKc1ZwZXJwZXR1YWxfdXNlcnMKcDEzCkkyCnNWcHJvZHVjdApwMTQKVlBvd2VyIFBhY2sKcDE1CnNWdHJpYWwKcDE2CkkwMQpzVnVzZXJzCnAxNwpJMTAKcy4=\nsignature = spdNw3ugMBT8QB0fVgufMUcy4t5NUVVCXMPgK+yPtkHIej2CRjBBfoQ4xpI1JMNzugmvRAz9gLyeeK4o3JYjq83b9mvtJ/b/O0VtchfM0FkoDZgdwWbyfKqYKWx3elc82XKyK4OOqqYuOs23G8bGx1zmElhsUYj+rBAFyG2adgIhWPbx/aP81QmdTsfmgY6yf4ys2ksAmXo7gj/oRnHkRGSNo+WerbJ9tYdWYd1/kh2Fj3KcKa6rApqJrwm7ZXBNM8kZ3uK5yKN53R8w5Ep4XF9JdktQtL29YHbt6xHFIFv1V/0DuR5MLgc3YBaYmR1Xl5cMl+3hbvC5XVjGXGCXUQ==\n\n')

    def test_read(self):
        """Testing License.read"""
        license_data = b'[License]\nlicense = KGRwMQpTJ2dyYWNlX3BlcmlvZCcKcDIKSTMKc1MndHJpYWwnCnAzCkkwMQpzUydwcm9kdWN0JwpwNApWUG93ZXIgUGFjawpwNQpzUydwZXJwZXR1YWxfdXNlcnMnCnA2CkkyCnNTJ3VzZXJzJwpwNwpJMTAKc1MnbGljZW5zZV92ZXJzaW9uJwpwOApJMgpzUydjb21wYW55JwpwOQpWRm9vQ29ycApwMTAKc1MnaW5zdGFsbF9rZXlzJwpwMTEKKGxwMTIKVmFiYzEyMwpwMTMKYXNTJ2V4cGlyYXRpb24nCnAxNApjZGF0ZXRpbWUKZGF0ZXRpbWUKcDE1CihTJ1x4MDdceGU0XHgwMVx4MDFceDAwXHgwMFx4MDBceDAwXHgwMFx4MDAnCnRScDE2CnMu\nsignature = dzhCPDHxE1Q1P1Kxnjsp5ioQzSrg3Da9pH8MQaVwLJtG4XMhL+JVaxDh8EhF80X3upouveSpT+R2qeEE7igpYcSeW/tcDOP3L9Hu7rUNkT9wIuJSx6R9ZIC5eRRlfRA53tRH2tc9QVmyi4LXfIT8TFwtV+AZVbdMtloym/DnsqHiOI/jVItWJbeOC2WY7FFNW8UNVgKiwyQ2PzwC3BqvHZ17mq+owQ8EhOyPTrtcJHrgFFfIE8GGAbHPeQ9yZuGeEWsmS5RcV1Ko2QAMyIlSc8ltY+GgFXphWz0VGwFmRVoJUM1SI2YhBu52UgutyjKO+VrEOfDHLAdEZXi/sh0Rdg==\n\n'
        license = License.read(license_data, TEST_PUBLIC_KEY)
        self.assertEqual(license.version, 2)
        self.assertEqual(license.product, b'Power Pack')
        self.assertEqual(license.company, b'FooCorp')
        self.assertEqual(license.num_users, 10)
        self.assertEqual(license.num_perpetual_users, 2)
        self.assertEqual(license.expiration, datetime(2020, 1, 1, 0, 0, 0))
        self.assertEqual(license.grace_period, 3)
        self.assertEqual(license.install_keys, [b'abc123'])
        self.assertTrue(license.trial)

    def test_decode(self):
        """Testing License.decode"""
        encoded_license = b'KGRwMQpTJ2dyYWNlX3BlcmlvZCcKcDIKSTMKc1MndHJpYWwnCnAzCkkwMQpzUydwcm9kdWN0JwpwNApWUG93ZXIgUGFjawpwNQpzUydwZXJwZXR1YWxfdXNlcnMnCnA2CkkyCnNTJ3VzZXJzJwpwNwpJMTAKc1MnbGljZW5zZV92ZXJzaW9uJwpwOApJMgpzUydjb21wYW55JwpwOQpWRm9vQ29ycApwMTAKc1MnaW5zdGFsbF9rZXlzJwpwMTEKKGxwMTIKVmFiYzEyMwpwMTMKYXNTJ2V4cGlyYXRpb24nCnAxNApjZGF0ZXRpbWUKZGF0ZXRpbWUKcDE1CihTJ1x4MDdceGU0XHgwMVx4MDFceDAwXHgwMFx4MDBceDAwXHgwMFx4MDAnCnRScDE2CnMu'
        signature = b'dzhCPDHxE1Q1P1Kxnjsp5ioQzSrg3Da9pH8MQaVwLJtG4XMhL+JVaxDh8EhF80X3upouveSpT+R2qeEE7igpYcSeW/tcDOP3L9Hu7rUNkT9wIuJSx6R9ZIC5eRRlfRA53tRH2tc9QVmyi4LXfIT8TFwtV+AZVbdMtloym/DnsqHiOI/jVItWJbeOC2WY7FFNW8UNVgKiwyQ2PzwC3BqvHZ17mq+owQ8EhOyPTrtcJHrgFFfIE8GGAbHPeQ9yZuGeEWsmS5RcV1Ko2QAMyIlSc8ltY+GgFXphWz0VGwFmRVoJUM1SI2YhBu52UgutyjKO+VrEOfDHLAdEZXi/sh0Rdg=='
        license = License.decode(encoded_license, signature, TEST_PUBLIC_KEY)
        self.assertEqual(license.version, 2)
        self.assertEqual(license.product, b'Power Pack')
        self.assertEqual(license.company, b'FooCorp')
        self.assertEqual(license.num_users, 10)
        self.assertEqual(license.num_perpetual_users, 2)
        self.assertEqual(license.expiration, datetime(2020, 1, 1, 0, 0, 0))
        self.assertEqual(license.grace_period, 3)
        self.assertTrue(license.trial)
        self.assertEqual(license.install_keys, [b'abc123'])

    def test_set_active_install_key_once(self):
        """Testing License.active_install_key being set initially"""
        license = License()
        license.active_install_key = b'abc123'

    def test_set_active_install_key_twice(self):
        """Testing License.active_install_key being set after already set fails
        """
        license = License()
        license.active_install_key = b'abc123'
        message = b'The active install key cannot be changed.'
        with self.assertRaisesMessage(AttributeError, message):
            license.active_install_key = b'def456'

    def test_set_verify_grace_start_time_to_none(self):
        """Testing License._verify_grace_start_time set to None"""
        license = License()
        license._verify_grace_start_time = None
        return

    def test_set_verify_grace_start_time_to_value(self):
        """Testing License._verify_grace_start_time set to non-None value fails
        """
        license = License()
        message = b'Cannot set private variable "_verify_grace_start_time".'
        with self.assertRaisesMessage(AttributeError, message):
            license._verify_grace_start_time = datetime.utcnow()

    def test_set_immutable_attrs(self):
        """Testing License and setting immutable attributes fails"""
        license = License()
        message = b'Cannot modify immutable attribute'
        for name in license.immutable_attrs:
            with self.assertRaisesMessage(AttributeError, message):
                setattr(license, name, 123)

        with self.assertRaisesMessage(AttributeError, message):
            license.some_new_attr = 123

    def test_delete_immutable_attrs(self):
        """Testing License and deleting immutable attributes fails"""
        license = License()
        message = b'Cannot delete immutable attribute'
        for name in license.immutable_attrs:
            with self.assertRaisesMessage(AttributeError, message):
                delattr(license, name)

        with self.assertRaisesMessage(AttributeError, message):
            del license.some_new_attr

    def test_set_class_attr(self):
        """Testing License and setting class attributes fails"""
        message = b'Class attributes cannot be modified.'
        with self.assertRaisesMessage(AttributeError, message):
            License.__setattr__ = lambda *args: None

    def test_delete_class_attr(self):
        """Testing License and deleting class attributes fails"""
        message = b'Class attributes cannot be deleted.'
        with self.assertRaisesMessage(AttributeError, message):
            del License.__setattr__