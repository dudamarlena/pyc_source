# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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