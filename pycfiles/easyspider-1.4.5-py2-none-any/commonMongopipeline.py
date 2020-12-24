# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/pipelines/commonMongopipeline.py
# Compiled at: 2018-04-04 22:37:34
from DBService import MongoService
from easyspider.pipelines.commonpipeline import commonpipeline
import logging, time
logger = logging.getLogger(__name__)
item_result_table_key = 'result_table'
item_update_key = 'update_record'
item_update_query_key = 'update_query_key'
item_keep_history = 'keep_history'
item_save_db = 'save_db'
default_mongo_url = 'mongodb://localhost:27017'
default_mongo_db_name = 'spider'
mongo_url_key = 'MONGO_URL'
mongo_db_name = 'MONGO_DB_NAME'

class commonMongopipeline(commonpipeline):

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

    def _process_item(self, item, spider, response, db=None, collection=None, update=False, hash_check_item=None, hash_check_item_dict_type=False):
        easyspider_meta = item.get('easyspider', {}).get('mongo_config', {})
        if not easyspider_meta:
            easyspider_meta = item.get('easyspider', {}).get('save_mongo', {})
        db = easyspider_meta.get('db')
        collection = easyspider_meta.get('collection')
        update = easyspider_meta.get('update')
        hash_check_item = easyspider_meta.get('hash_check_item')
        hash_check_item_dict_type = easyspider_meta.get('hash_check_item_dict_type')
        force_replace = easyspider_meta.get('force_replace')
        error_flag = False
        error_limit = 3
        error_count = 1
        while error_count <= error_limit:
            try:
                self._insert_or_update(item, spider, db, collection, update, hash_check_item, hash_check_item_dict_type, force_replace)
                error_flag = False
                break
            except Exception:
                error_flag = True
                logger.exception('第[%s / %s]操作数据库失败，下次再尝试' % (error_count, error_limit))
                time.sleep(2)

            error_count += 1

        if error_flag:
            self._insert_or_update(item, spider, db, collection, update, hash_check_item, hash_check_item_dict_type, force_replace)
        return item

    def _insert_or_update(self, item, spider, db=None, collection=None, update=False, hash_check_item=None, hash_check_item_dict_type=False, force_replace=None):
        _save_item = item.copy()
        if not db:
            self.server.select_db(_save_item.get(item_save_db, spider.name))
        else:
            self.server.select_db(db)
        if not collection:
            collection = _save_item.get(item_result_table_key, spider.name)
        if not update:
            self.server.insert(collection, _save_item)
            return item
        if not force_replace:
            force_replace = False
        else:
            force_replace = True
        if hash_check_item_dict_type:
            last_result = hash_check_item
        else:
            last_result = {}
            for k in hash_check_item:
                last_result[k] = _save_item.get(k)

        if force_replace:
            self.server.replace_one(collection, last_result, _save_item, upsert=True)
        else:
            self.server.update_one(collection, last_result, {'$set': _save_item}, upsert=True)
        return item