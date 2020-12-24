# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/pipelines/easy_mongo_pipeline.py
# Compiled at: 2017-08-24 09:47:41
from easyspider.utils.DBService import MongoService
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread
default_mongo_url = 'mongodb://localhost:27017'
default_mongo_db_name = 'spider'
mongo_url_key = 'MONGO_URL'
mongo_db_name = 'MONGO_DB_NAME'
item_result_table_key = 'result_table'
item_update_key = 'update_record'
item_update_query_key = 'update_query_key'
item_keep_history = 'keep_history'
item_save_db = 'save_db'

class easyMongoPipeline(object):

    def __init__(self, mongoUrl, mongoDbName):
        self.server = MongoService(mongoUrl)
        self.server.select_db(mongoDbName)

    @classmethod
    def from_settings(cls, settings):
        mongoUrl = settings.get(mongo_url_key, default_mongo_url)
        mongoDbName = settings.get(mongo_db_name, default_mongo_db_name)
        return cls(mongoUrl, mongoDbName)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        result_table = item.get(item_result_table_key, spider.name)
        self.server.select_db(item.get(item_save_db, spider.name))
        if item.get(item_update_key):
            history_record = {}
            for key in item.get(item_update_query_key):
                history_record[key] = item.get(key)

            self.server.replace_one(result_table, item, history_record)
        else:
            self.server.insert(result_table, item)
        if item.get(item_keep_history):
            self.server.insert('%s_history' % result_table, item)
        return item