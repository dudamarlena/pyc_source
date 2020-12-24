# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/corpcrawl_env/corpcrawl/corpcrawl/crawler.py
# Compiled at: 2013-03-12 00:01:00
from parser import Parser

class CorpCrawl(object):

    def __init__(self, backend, cache_path=''):
        self.cache_path = cache_path
        self.backend = backend

    def crawl(self, years, quarters):
        parse = Parser(self.cache_path, self.backend)
        parse.parse(years, quarters)