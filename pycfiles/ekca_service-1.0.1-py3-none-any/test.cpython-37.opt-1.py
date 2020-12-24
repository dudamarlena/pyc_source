# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ekca_service/test.py
# Compiled at: 2019-10-23 10:49:07
# Size of source mod 2**32: 870 bytes
"""
stuff for testing
"""
import unittest, pkg_resources
from ekca_service.__about__ import PASSWORD_PLUGIN_NAMESPACE, OTP_PLUGIN_NAMESPACE

class PasswordPluginTestCase(unittest.TestCase):
    __doc__ = '\n    base unit test class (not directly used)\n    '
    plugin_name = None

    def setUp(self):
        self.password_plugins = {entry_point.name:entry_point.load() for entry_point in pkg_resources.iter_entry_points(PASSWORD_PLUGIN_NAMESPACE)}


class OTPPluginTestCase(unittest.TestCase):
    __doc__ = '\n    base unit test class (not directly used)\n    '
    plugin_name = None

    def setUp(self):
        self.otp_plugins = {entry_point.name:entry_point.load() for entry_point in pkg_resources.iter_entry_points(OTP_PLUGIN_NAMESPACE)}