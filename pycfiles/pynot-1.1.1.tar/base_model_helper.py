# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pynosql/common/base_model_helper.py
# Compiled at: 2019-03-09 18:37:41
from abc import ABCMeta, abstractmethod, abstractproperty

class BaseModelHelper(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def model(self):
        """ Return Model

        :return: obj model
        """
        pass

    @abstractmethod
    def reset(self):
        """ Reset model with base structure

        :return: None
        """
        pass

    @abstractmethod
    def load(self, values):
        """ Load model with passed values

        :param values: dict k/v to load into model
        :return: obj model
        """
        pass