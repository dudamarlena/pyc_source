# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/shinsheel/Documents/Data-Gathering/Pypi/anarcute/anarcute/google.py
# Compiled at: 2019-09-16 09:56:33
# Size of source mod 2**32: 2048 bytes
import hy.macros, requests
from anarcute import *
hy.macros.require('anarcute.lib', None, assignments='ALL', prefix='')

class GT(object):
    """GT"""

    def __init__(self, key):
        self.key = key
        self.api = 'https://translation.googleapis.com/language/translate/v2'

    def translate(self, source, target, q, format='text', model=None):
        params = {'key':self.key, 
         'q':q,  'source':source, 
         'target':target,  'format':format,  'model':model}
        return requests.get(self.api, params).json()


class GS(object):
    """GS"""

    def __init__(self, cx, key):
        self.api = 'https://www.googleapis.com/customsearch/v1/siterestrict'
        self.cx = cx
        self.key = key

    def search(self, q, follow=True, TIMEOUT=10, start=1):
        params = {'q':q, 
         'cx':self.cx,  'key':self.key, 
         'start':start}
        res = requests.get((self.api), params=params, timeout=TIMEOUT).json()
        if 'items' not in res:
            if follow:
                if 'spelling' in res:
                    if 'correctedQuery' in res['spelling']:
                        corrected = res['spelling']['correctedQuery']
                        print('REDIRECT from', q, 'to', corrected)
                        return self.search(corrected, follow=True, start=start, TIMEOUT=TIMEOUT)
        return res

    def items(self, q, start=1, end=None):
        r = self.search(q, start=start)
        try:
            items = r['items']
        except Exception:
            items = []

        if 'queries' in r:
            if 'nextPage' in r['queries']:
                if r['queries']['nextPage']:
                    if end:
                        if end < len(items):
                            return items + self.items(q, start=(r['queries']['nextPage'][0]['startIndex']))
        return items