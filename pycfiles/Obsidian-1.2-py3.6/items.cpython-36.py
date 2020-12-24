# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/Obsidian/items.py
# Compiled at: 2018-01-07 08:54:16
# Size of source mod 2**32: 361 bytes
import scrapy

class ObsidianItem(scrapy.Item):
    status = scrapy.Field()
    title = scrapy.Field()
    crawl_time = scrapy.Field()
    url = scrapy.Field()