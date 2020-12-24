# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/shorter/ur1ca.py
# Compiled at: 2011-07-11 18:11:51
import re, urllib
from urlshorter import UrlShorter

class Ur1caUrlShorter(UrlShorter):

    def __init__(self):
        self.base = 'http://ur1.ca'
        self.pt = re.compile('<p class="success">Your ur1 is: <a href="(.*?)">')

    def do_shorter(self, longurl):
        values = {'submit': 'Make it an ur1!', 'longurl': longurl}
        data = urllib.urlencode(values)
        resp = self._get_request(self.base, data)
        short = self.pt.findall(resp)
        if len(short) > 0:
            return short[0]