# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/hadax.py
# Compiled at: 2018-04-27 06:35:49
from anyex.huobipro import huobipro

class hadax(huobipro):

    def describe(self):
        return self.deep_extend(super(hadax, self).describe(), {'id': 'hadax', 
           'name': 'HADAX', 
           'countries': 'CN', 
           'hostname': 'api.hadax.com', 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/38059952-4756c49e-32f1-11e8-90b9-45c1eccba9cd.jpg', 
                    'api': 'https://api.hadax.com', 
                    'www': 'https://www.hadax.com', 
                    'doc': 'https://github.com/huobiapi/API_Docs/wiki'}, 
           'has': {'fetchCurrencies': False}, 
           'api': {'public': {'get': [
                                    'hadax/common/symbols',
                                    'hadax/common/currencys',
                                    'common/timestamp',
                                    'hadax/settings/currencys']}}, 
           'options': {'fetchMarketsMethod': 'publicGetHadaxCommonSymbols'}})