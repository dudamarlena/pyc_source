# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Thoughtworker/Envs/wadl2swagger/lib/python2.7/site-packages/wadltools/wadlcrawler.py
# Compiled at: 2014-09-17 19:43:37
import mechanize, os, errno

class WADLCrawler:

    def __init__(self):
        self.browser = mechanize.Browser()

    def crawl(self, url):
        br = self.browser
        br.open(url)
        response = br.response()
        wadl_files = []
        for link in br.links():
            if link.url.endswith('.wadl'):
                wadl_files.append(link.absolute_url)

        return wadl_files

    def download(self, url, target_file):
        br = self.browser
        br.open(url)
        f = open(target_file, 'w')
        f.write(br.response().read())
        f.close