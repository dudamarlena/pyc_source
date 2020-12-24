# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynosql/credentials/base_credentials.py
# Compiled at: 2019-02-23 11:05:46
from abc import ABCMeta, abstractmethod

class InvalidCredentials(Exception):
    """ Invalid Credentials Exception

        Check if the credentials are not None and are
        valid strings.

    """

    def __init__(self, msg):
        self.message = msg


class BaseCredentials:
    """ Base Credentials Class """
    __metaclass__ = ABCMeta

    @abstractmethod
    def check_credentials(self):
        """ Check for valid credentials

        :return: None
        :raises: InvalidCredentials
        """
        pass