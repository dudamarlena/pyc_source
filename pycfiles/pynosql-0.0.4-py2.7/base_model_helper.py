# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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