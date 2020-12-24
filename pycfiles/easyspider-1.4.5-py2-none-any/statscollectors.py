# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/core/statscollectors.py
# Compiled at: 2018-04-04 22:37:34
from scrapy.statscollectors import MemoryStatsCollector

class easyspiderStatsCollector(MemoryStatsCollector):

    def __init__(self, crawler):
        super(easyspiderStatsCollector, self).__init__(crawler)