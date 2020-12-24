# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pynosql/common/model_helper.py
# Compiled at: 2019-03-17 11:51:47
import copy
from pynosql.common.base_model_helper import BaseModelHelper

class ModelHelper(BaseModelHelper):
    """ Model Common Methods """

    def __init__(self, base_model):
        """ Model Common Methods

        :param base_model: obj base model
        """
        self._base_model = copy.deepcopy(base_model)
        self._model = copy.deepcopy(self._base_model)
        self._model_list = []
        self._model_is_list = False

    @property
    def model(self):
        """ Return Model or List

        :return: obj model
        """
        if self._model_is_list:
            return self._model_list
        return self._model

    def reset(self):
        """ Reset Model

        :return: None
        """
        self._model = copy.deepcopy(self._base_model)

    def load(self, values, is_list=False):
        """ Load Model w/ Values

        :param values: obj values
        :param is_list: bool if list expected
        :return: obj model
        """
        self._model_is_list = is_list
        if isinstance(values, list):
            for item in values:
                for k, v in item.items():
                    self._load(k, v, self._model)

                self._model_list.append(copy.deepcopy(self._model))
                self.reset()

        else:
            for k, v in values.items():
                self._load(k, v, self._model)

        return self.model

    def _load(self, key, value, structure):
        """ Recursively Load K/V into Model Structure

            NOTE: this will not set any keys not in the original
            model which can lead to data loss if the model were
            to change.  This allows the ability to remove data
            from DB or add new values as required.

        :param key: str key
        :param value: obj value
        :param structure: obj structure
        :return: None
        """
        if isinstance(value, dict):
            if key in structure.keys():
                for k, v in value.items():
                    self._load(k, v, structure[key])

        elif key in structure.keys():
            structure[key] = value