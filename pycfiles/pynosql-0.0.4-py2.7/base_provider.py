# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynosql/providers/base_provider.py
# Compiled at: 2019-03-17 11:53:30
from abc import ABCMeta, abstractmethod

class UnhandledProviderException(Exception):
    """ Unhandled Exception """

    def __init__(self, msg):
        self.message = msg


class RecordNotFound(Exception):
    """ Record Not Found Exception """

    def __init__(self, msg):
        self.message = msg


class BaseProvider:
    """ Base NOSQL Provider """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_record(self, model, table, **kwargs):
        """ Get a single record from DB

        :param model: obj BaseModel
        :param table: str table
        :return: dict record
        :raises: ClientException
        """
        pass

    @abstractmethod
    def get_records(self, model, table, **kwargs):
        """ Get multiple records from DB

        :param model: obj BaseModel
        :param table: str table
        :param options: obj options
        :return: list records
        :raises: ClientException
        """
        pass

    @abstractmethod
    def scan_records(self, model, table, **kwargs):
        """ Get multiple records from DB through scan without index

        :param model: obj BaseModel
        :param table: str table
        :param options: obj options
        :return: list records
        :raises: ClientException
        """
        pass

    @abstractmethod
    def put_record(self, model, table, **kwargs):
        """ Put record into DB

        :param model: obj BaseModel
        :param table: str table
        :return: bool status
        :raises: ClientException
        """
        pass

    @abstractmethod
    def delete_record(self, model, table, **kwargs):
        """ Delete record from DB

        :param model: obj BaseModel
        :param table: str table
        :return: bool status
        :raises: ClientException
        """
        pass