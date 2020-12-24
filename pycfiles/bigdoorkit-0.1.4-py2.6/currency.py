# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/bigdoorkit/resources/currency.py
# Compiled at: 2010-09-16 19:25:53
from bigdoorkit.resources.base import BDResource

class Currency(BDResource):
    endpoint = 'currency'

    def __init__(self, **kw):
        self.currency_type_id = kw.get('currency_type_id', None)
        self.currency_type_description = kw.get('currency_type_description', None)
        self.currency_type_title = kw.get('currency_type_title', None)
        self.exchange_rate = kw.get('exchange_rate', None)
        self.relative_weight = kw.get('relative_weight', None)
        super(Currency, self).__init__(**kw)
        return