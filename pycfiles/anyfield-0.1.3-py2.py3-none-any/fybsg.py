# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/fybsg.py
# Compiled at: 2018-04-27 06:35:53
from anyex.fybse import fybse

class fybsg(fybse):

    def describe(self):
        return self.deep_extend(super(fybsg, self).describe(), {'id': 'fybsg', 
           'name': 'FYB-SG', 
           'countries': 'SG', 
           'has': {'CORS': False}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27766513-3364d56a-5edb-11e7-9e6b-d5898bb89c81.jpg', 
                    'api': 'https://www.fybsg.com/api/SGD', 
                    'www': 'https://www.fybsg.com', 
                    'doc': 'http://docs.fyb.apiary.io'}, 
           'markets': {'BTC/SGD': {'id': 'SGD', 'symbol': 'BTC/SGD', 'base': 'BTC', 'quote': 'SGD'}}})