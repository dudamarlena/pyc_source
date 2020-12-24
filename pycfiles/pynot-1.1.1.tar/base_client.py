# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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