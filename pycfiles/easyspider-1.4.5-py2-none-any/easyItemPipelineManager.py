# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/core/easyItemPipelineManager.py
# Compiled at: 2018-03-07 09:04:57
from scrapy.pipelines import ItemPipelineManager

class easyItemPipelineManager(ItemPipelineManager):

    def process_item(self, item, spider, response):
        return self._process_chain('process_item', item, spider, response)