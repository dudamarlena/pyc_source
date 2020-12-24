# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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