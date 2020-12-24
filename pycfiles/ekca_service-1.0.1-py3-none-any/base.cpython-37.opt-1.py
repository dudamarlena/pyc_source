# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ekca_service/plugins/password/base.py
# Compiled at: 2019-12-12 04:34:35
# Size of source mod 2**32: 1486 bytes
"""
ekca_service.plugins.password - Module package for password checker plugins
"""
__all__ = [
 'PasswordChecker']
from collections import defaultdict

class PasswordCheckFailed(Exception):
    __doc__ = '\n    base exception class for all password failures\n    '


class PasswordChecker:
    __doc__ = '\n    Base class for password checker plugin classes, not directly used!\n    '

    def __init__(self, cfg, logger):
        """
        :cfg: is config dict
        """
        self._log = logger
        self._cfg = cfg

    def check(self, user_name, password, remote_addr):
        """
        actually check whether password is valid for username
        """
        raise PasswordCheckFailed()


class Dummy(PasswordChecker):
    __doc__ = '\n    Dummy OTP checker always returning True for pre-defined set of OTP values\n    '
    cfg_key_values = 'PASSWORD_DUMMY_VALUES'
    values_default = 'secret123456 12345678 supersecret'

    def __init__(self, cfg, logger):
        PasswordChecker.__init__(self, cfg, logger)
        self._valid_passwords = frozenset([val for val in self._cfg.get(self.cfg_key_values, self.values_default).replace(',', ' ').split(' ') if val])

    def check(self, user_name, password, remote_addr):
        if password not in self._valid_passwords:
            raise PasswordCheckFailed()
        return dict(attributes=(defaultdict(lambda : [])))