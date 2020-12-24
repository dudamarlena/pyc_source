# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pynosql/base/model.py
# Compiled at: 2019-03-17 11:48:41
from pynosql.base.base_model import BaseModel
from pynosql.common.model_helper import ModelHelper

class Model(BaseModel):
    """ Model """
    BASE = {}

    def __init__(self, base_model=BASE):
        self.mh = ModelHelper(base_model)

    @property
    def model(self):
        """ Return Model

        :return: obj model
        """
        return self.mh.model

    def reset(self):
        """ Reset Model

        :return: None
        """
        self.mh.reset()

    def load(self, values, is_list=False):
        """ Load Model Values

        :param values: obj values
        :param is_list: bool if list expected
        :return: obj model
        """
        return self.mh.load(values, is_list)