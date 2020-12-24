# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/huobicny.py
# Compiled at: 2018-04-27 06:35:47
from anyex.huobipro import huobipro

class huobicny(huobipro):

    def describe(self):
        return self.deep_extend(super(huobicny, self).describe(), {'id': 'huobicny', 
           'name': 'Huobi CNY', 
           'hostname': 'be.huobi.com', 
           'has': {'CORS': False}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27766569-15aa7b9a-5edd-11e7-9e7f-44791f4ee49c.jpg', 
                    'api': 'https://be.huobi.com', 
                    'www': 'https://www.huobi.com', 
                    'doc': 'https://github.com/huobiapi/API_Docs/wiki/REST_api_reference'}})