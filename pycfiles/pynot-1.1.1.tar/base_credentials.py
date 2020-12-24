# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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