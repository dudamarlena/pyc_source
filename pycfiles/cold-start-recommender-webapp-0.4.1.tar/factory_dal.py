# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mal/pCloud/Python/cold-start-recommender/csrec/factory_dal.py
# Compiled at: 2017-12-01 12:35:53
__author__ = 'elegans.io Ltd'
__email__ = 'info@elegans.io'
from csrec.exceptions import *

class Dal:

    @staticmethod
    def get_implemented_dal():
        """
        get the implemented dal
        :return: a set of implemented dal
        """
        implemented_dal = {
         'mem'}
        return implemented_dal

    @staticmethod
    def get_dal_supported_parameters(name):
        """
        get a list of supported parameters by a dal implementation and their description

        :param name: the name of any DAL implementation i.e. mem
        :return: the dictionary with the supported parameters and the description
        """
        if name == 'mem':
            import csrec.mem_dal as mem_dal
            return mem_dal.Database.get_init_parameters_description()
        raise NotImplementedError

    @staticmethod
    def get_dal(name, **params):
        """
        database abstraction layer factory

        exception: raise a InitializationError if any error occur

        :param name: the name of any DAL implementation i.e. mem
        :param params: the dictionary of the parameters supported by the implementation. Refer to the
            help of the init process of the specific instance for the supported parameters.
        :return: an instance of the DAL implementation if the initialization was successfully executed
        """
        if name == 'mem':
            import csrec.mem_dal as mem_dal
            try:
                dal_instance = mem_dal.Database()
            except InitializationException as exc:
                raise InitializationException('unable to initialize: ' % name)

        else:
            raise NotImplementedError
        dal_instance.init(**params)
        return dal_instance