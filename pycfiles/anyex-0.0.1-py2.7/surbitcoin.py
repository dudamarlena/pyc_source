# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/surbitcoin.py
# Compiled at: 2018-04-27 06:35:21
from anyex.foxbit import foxbit

class surbitcoin(foxbit):

    def describe(self):
        return self.deep_extend(super(surbitcoin, self).describe(), {'id': 'surbitcoin', 
           'name': 'SurBitcoin', 
           'countries': 'VE', 
           'has': {'CORS': False}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27991511-f0a50194-6481-11e7-99b5-8f02932424cc.jpg', 
                    'api': {'public': 'https://api.blinktrade.com/api', 
                            'private': 'https://api.blinktrade.com/tapi'}, 
                    'www': 'https://surbitcoin.com', 
                    'doc': 'https://blinktrade.com/docs'}, 
           'options': {'brokerId': '1'}})