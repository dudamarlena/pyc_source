# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/commonslib/view_model.py
# Compiled at: 2015-04-04 05:19:06
from decorated.base.dict import DefaultDict
__author__ = 'freeway'

class ViewModel(DefaultDict):

    def __init__(self, default='', **kw):
        super(ViewModel, self).__init__(default, **kw)

    @staticmethod
    def to_views(biz_models):
        if biz_models is None or len(biz_models) == 0:
            return []
        return [ ViewModel(**biz_model.attributes) for biz_model in biz_models ]
        return

    @staticmethod
    def to_view(biz_model):
        return ViewModel(**biz_model.attributes)