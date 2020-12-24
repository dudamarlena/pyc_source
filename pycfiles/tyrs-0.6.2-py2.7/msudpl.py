# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/shorter/msudpl.py
# Compiled at: 2011-07-21 15:50:09
import re, urllib
from urlshorter import UrlShorter

class MsudplUrlShorter(UrlShorter):

    def __init__(self):
        self.base = 'http://msud.pl'
        self.pt = re.compile('<p>Whouah ! This a very beautiful url :\\) <a href="(.*?)">')
        self.pt_yet_in_base = re.compile('and whouah! It\'s very beautiful <a href="(.*?)">')

    def do_shorter(self, longurl):
        values = {'submit': 'Generate my sexy url', 'sexy_url': longurl}
        data = urllib.urlencode(values)
        resp = self._get_request(self.base, data)
        short = self.pt.findall(resp)
        if len(short) == 0:
            short = self.pt_yet_in_base.findall(resp)
        if len(short) > 0:
            return self.base + '/' + short[0]