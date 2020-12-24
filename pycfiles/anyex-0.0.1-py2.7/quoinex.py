# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/quoinex.py
# Compiled at: 2018-04-27 06:35:22
from anyex.qryptos import qryptos

class quoinex(qryptos):

    def describe(self):
        return self.deep_extend(super(quoinex, self).describe(), {'id': 'quoinex', 
           'name': 'QUOINEX', 
           'countries': [
                       'JP', 'SG', 'VN'], 
           'version': '2', 
           'rateLimit': 1000, 
           'has': {'CORS': False, 
                   'fetchTickers': True}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/35047114-0e24ad4a-fbaa-11e7-96a9-69c1a756083b.jpg', 
                    'api': 'https://api.quoine.com', 
                    'www': 'https://quoinex.com/', 
                    'doc': [
                          'https://developers.quoine.com',
                          'https://developers.quoine.com/v2'], 
                    'fees': 'https://news.quoinex.com/fees/'}})