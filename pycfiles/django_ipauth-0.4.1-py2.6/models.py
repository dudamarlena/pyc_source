# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/ipauth/tests/models.py
# Compiled at: 2011-06-17 10:46:50
from django.core.exceptions import ValidationError
from django.test import TestCase
from ipauth import models

class IPToLongTestCase(TestCase):

    def test_valid_ip(self):
        """ Test the ip_to_long function with valid IP addresses """
        self.assertEqual(models.ip_to_long('128.1.1.1'), 2147549441)
        self.assertEqual(models.ip_to_long('128.1.0.1'), 2147549185)
        self.assertEqual(models.ip_to_long('128.0.1.1'), 2147483905)
        self.assertEqual(models.ip_to_long('128.1.1.0'), 2147549440)
        self.assertEqual(models.ip_to_long('10.0.0.0'), 167772160)

    def test_invalid_ip(self):
        """ Test the ip_to_long function with some invalid IP addresses. """
        self.assertRaises(ValidationError, models.ip_to_long, 'completely invalid')
        self.assertRaises(ValidationError, models.ip_to_long, '128.0.0.a')
        self.assertRaises(ValidationError, models.ip_to_long, '256.0.0.1')


class LongToIPTestCase(TestCase):

    def test_valid_ip(self):
        """ Test the long_to_ip function with valid IP addresses """
        self.assertEqual(models.long_to_ip(2147549441), '128.1.1.1')
        self.assertEqual(models.long_to_ip(2147549185), '128.1.0.1')
        self.assertEqual(models.long_to_ip(2147483905), '128.0.1.1')
        self.assertEqual(models.long_to_ip(2147549440), '128.1.1.0')
        self.assertEqual(models.long_to_ip(167772160), '10.0.0.0')


__all__ = [
 'IPToLongTestCase', 'LongToIPTestCase']