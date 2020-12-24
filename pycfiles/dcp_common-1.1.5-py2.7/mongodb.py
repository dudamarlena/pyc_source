# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dcp_common/pipelines/mongodb.py
# Compiled at: 2018-09-28 07:51:59
import pymongo
from twisted.internet.threads import deferToThread

class MongoDBPipeline(object):

    def __init__(self, mongodb_uri, mongodb_database):
        self.mongodb_uri = mongodb_uri
        self.mongodb_database = mongodb_database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongodb_uri=crawler.settings.get('MONGODB_URI'), mongodb_database=crawler.settings.get('MONGODB_DATABASE'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.database = self.client[self.mongodb_database]

    def _process_item(self, item, spider):
        self.database[spider.name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)