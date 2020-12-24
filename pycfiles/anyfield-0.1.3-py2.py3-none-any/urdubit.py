# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/urdubit.py
# Compiled at: 2018-04-27 06:35:18
from anyex.foxbit import foxbit

class urdubit(foxbit):

    def describe(self):
        return self.deep_extend(super(urdubit, self).describe(), {'id': 'urdubit', 
           'name': 'UrduBit', 
           'countries': 'PK', 
           'has': {'CORS': False}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27991453-156bf3ae-6480-11e7-82eb-7295fe1b5bb4.jpg', 
                    'api': {'public': 'https://api.blinktrade.com/api', 
                            'private': 'https://api.blinktrade.com/tapi'}, 
                    'www': 'https://urdubit.com', 
                    'doc': 'https://blinktrade.com/docs'}, 
           'options': {'brokerId': '8'}})