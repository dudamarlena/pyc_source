# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/example/scrapy_movie/pipelines.py
# Compiled at: 2019-12-25 23:33:32
# Size of source mod 2**32: 142 bytes


class MongodbPipeline(object):

    def process_item(self, item, spider):
        item.process()
        return item