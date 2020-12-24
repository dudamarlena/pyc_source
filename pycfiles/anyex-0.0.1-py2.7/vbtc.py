# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/vbtc.py
# Compiled at: 2018-04-27 06:35:17
from anyex.foxbit import foxbit

class vbtc(foxbit):

    def describe(self):
        return self.deep_extend(super(vbtc, self).describe(), {'id': 'vbtc', 
           'name': 'VBTC', 
           'countries': 'VN', 
           'has': {'CORS': False}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27991481-1f53d1d8-6481-11e7-884e-21d17e7939db.jpg', 
                    'api': {'public': 'https://api.blinktrade.com/api', 
                            'private': 'https://api.blinktrade.com/tapi'}, 
                    'www': 'https://vbtc.exchange', 
                    'doc': 'https://blinktrade.com/docs'}, 
           'options': {'brokerId': '3'}})