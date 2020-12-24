# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\verification\verification.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 2359 bytes
from mysqlmapper.verification.rule import *

class Helper:
    """Helper"""
    _dict_parameter = None
    _configs = None
    _rules = [
     Required(), Length(), Range(), DateTime(), Regexp()]

    def __init__(self, dict_parameter, configs):
        """
        Initialize verification help tool class
        :param dict_parameter: Parameter dictionary
        :param configs: Rule dictionary
        """
        self._dict_parameter = dict_parameter
        self._configs = configs

    def weak_check(self):
        """
        Weak check, skip when parameter does not exist
        :return: Verification result
        """
        for config in self._configs.items():
            name = config[0]
            expr = config[1]
            if name not in self._dict_parameter:
                continue
            flag = False
            for rule in self._rules:
                if rule.know(expr):
                    flag = True
                    b, message = rule.check(self._dict_parameter, expr, name, self._dict_parameter[name])
                    if not b:
                        return (b, message)
                    break

            if not flag:
                return (False, 'Validation rule does not exist')

        return (True, 'success')

    def check(self):
        """
        Strong check. When the parameter does not exist, a check error is returned
        :return: Verification result
        """
        for config in self._configs.items():
            name = config[0]
            expr = config[1]
            if name not in self._dict_parameter:
                return (False, name + ' Parameter does not exist')
                flag = False
                for rule in self._rules:
                    if rule.know(expr):
                        flag = True
                        b, message = rule.check(self._dict_parameter, expr, name, self._dict_parameter[name])
                        if not b:
                            return (b, message)
                        break

                return flag or (False, 'Validation rule does not exist')

        return (True, 'success')