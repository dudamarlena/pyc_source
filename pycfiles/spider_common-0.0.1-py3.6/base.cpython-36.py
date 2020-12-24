# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spider_common/persistent/items/base.py
# Compiled at: 2019-04-16 05:50:15
# Size of source mod 2**32: 251 bytes
from scrapy.item import Item, Field

class BaseItem(Item):
    name = Field()
    channel = Field()
    crawled_time = Field()
    src_id = Field()
    src = Field()