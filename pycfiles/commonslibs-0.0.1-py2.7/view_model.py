# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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