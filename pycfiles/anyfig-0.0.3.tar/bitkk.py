# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/bitkk.py
# Compiled at: 2018-04-27 06:36:18
from anyex.zb import zb

class bitkk(zb):

    def describe(self):
        return self.deep_extend(super(bitkk, self).describe(), {'id': 'bitkk', 
           'name': 'bitkk', 
           'comment': 'a Chinese ZB clone', 
           'urls': {'api': {'public': 'http://api.bitkk.com/data', 
                            'private': 'https://trade.bitkk.com/api'}, 
                    'www': 'https://www.bitkk.com', 
                    'doc': 'https://www.bitkk.com/i/developer', 
                    'fees': 'https://www.bitkk.com/i/rate'}})