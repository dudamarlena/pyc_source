# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ginopalazzo/Magic/zoidberg/zoidberg/scraper/spiders/zoidberg_spider.py
# Compiled at: 2018-03-09 10:54:04
# Size of source mod 2**32: 935 bytes
import scrapy

class ZoidbergSpider(scrapy.Spider):
    __doc__ = "\n    Base Spider for all Zoidberg's spiders that implement scrapy.Spider.\n    "
    name = 'zoidberg'

    def __init__(self, doctor_regex=None, urls=None, path=None, source=None, name=None, *args, **kwargs):
        """
        Init Zoidberg base spider
        :param doctor_regex: regex string of the doctor to search in the source
        :param urls: urls to start crawling
        :param path: path to save the output file
        :param source: source of the information
        :param name: name of the spider
        :param args:
        :param kwargs:
        """
        (super(ZoidbergSpider, self).__init__)(*args, **kwargs)
        self.doctor_regex = doctor_regex
        self.source = source
        self.start_urls = urls
        self.path = path
        self.name = name

    def parse(self, response):
        pass