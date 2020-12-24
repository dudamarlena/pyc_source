# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/example/scrapy_movie/pipelines.py
# Compiled at: 2019-12-25 23:33:32
# Size of source mod 2**32: 142 bytes


class MongodbPipeline(object):

    def process_item(self, item, spider):
        item.process()
        return item