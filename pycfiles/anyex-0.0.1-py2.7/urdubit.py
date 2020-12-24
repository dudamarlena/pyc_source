# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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