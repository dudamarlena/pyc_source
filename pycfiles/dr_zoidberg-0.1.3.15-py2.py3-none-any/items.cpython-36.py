# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ginopalazzo/Magic/zoidberg/zoidberg/scraper/items.py
# Compiled at: 2018-03-07 16:29:37
# Size of source mod 2**32: 358 bytes
import scrapy

class CommentItem(scrapy.Item):
    author = scrapy.Field()
    text = scrapy.Field()
    source = scrapy.Field()
    date = scrapy.Field()