# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Es\WebGeter.py
# Compiled at: 2019-12-18 21:44:29
# Size of source mod 2**32: 2349 bytes
import requests
from bs4 import BeautifulSoup
import time
from .BugReporter import BugReporter

class WebGeter:

    def __init__(self, inputUrl):
        self.url = inputUrl
        self.head = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ', 
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
         'Accept-Language':'zh-CN', 
         'Connection':'keep-alive', 
         'Accept-Charset':'utf-8;q=0.7,*;q=0.7'}
        self.getRawData()

    def getRawData(self):
        try:
            r = requests.get((self.url), timeout=30, headers=(self.head), allow_redirects=False)
            r.raise_for_status()
            r.encoding = 'utf-8'
            self.raw_data = r.text
            try:
                self.raw_data = BeautifulSoup(self.raw_data, 'lxml')
            except:
                self.raw_data = BeautifulSoup(self.raw_data, 'html.parser')

        except Exception as e:
            try:
                with open('error.log', 'w') as (f):
                    f.write('errorcode:1001\n\ntime:' + str(time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))) + '\n\nraise : ' + str(e))
                    BugReporter()
            finally:
                e = None
                del e