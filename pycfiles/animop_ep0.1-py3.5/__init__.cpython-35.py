# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/main/__init__.py
# Compiled at: 2016-12-15 06:27:50
# Size of source mod 2**32: 902 bytes
import urllib.request
from bs4 import BeautifulSoup
import re, unshortenit

class AnimeOp:

    def __init__(self):
        self.url = ''
        self.first = ''
        self.last = ''
        self.fname = ''

    def link(self):
        resp = urllib.urlopen(self.url)
        soup = BeautifulSoup(resp.read())
        link = soup.find_all('a', href=re.compile('http:\\/\\/adf.ly\\/[\\s\\S].....'), text=re.compile('\\d'))
        i = 0
        for value in link:
            i += 1
            if i > self.first and i < self.last:
                unshortened_uri, status = unshortenit.unshorten_only(value['href'])
                print(unshortened_uri, value.contents[0])
                with open(self.fname + '.txt', 'a') as (myfile):
                    myfile.write(unshortened_uri + ' - ' + value.contents[0] + '\n')
                continue

        return 'Done!'