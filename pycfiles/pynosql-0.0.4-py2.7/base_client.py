# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynosql/clients/base_client.py
# Compiled at: 2019-03-09 18:37:41
from abc import ABCMeta, abstractmethod, abstractproperty

class InitializationError(Exception):
    """ Exception initializing client """

    def __init__(self, msg):
        self.message = msg


class ClientException(Exception):
    """ Exception calling client method """

    def __init__(self, msg):
        self.message = msg


class BaseClient:
    """ Base Client """
    __metaclass__ = ABCMeta

    @abstractproperty
    def client(self):
        """ Client property

        :return: obj client
        """
        pass

    @abstractmethod
    def initialize(self):
        """ Initialize client

        :return: obj client/session
        """
        pass

    @abstractmethod
    def call(self, client_method, **kwargs):
        """ Call client method

        :param client_method: str method
        :param kwargs: obj args
        :return: obj restuls
        """
        pass