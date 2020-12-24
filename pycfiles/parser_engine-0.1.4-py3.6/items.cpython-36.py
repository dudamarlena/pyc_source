# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/clue/items.py
# Compiled at: 2019-03-22 03:43:37
# Size of source mod 2**32: 263 bytes
from scrapy.item import Item, Field

class ClueItem(Item):
    channel = Field()
    business = Field()
    url = Field()
    from_clue_id = Field()
    req = Field()
    project = Field()
    spider = Field()