# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/pipelines/commonMysqlpipeline.py
# Compiled at: 2018-09-15 04:30:53
import json, time, logging, hashlib
from DBService import MysqlService
from twisted.internet.threads import deferToThread
from easyspider.pipelines.commonpipeline import commonpipeline
import copy
logger = logging.getLogger(__name__)

def md5_from_dict(item):
    u"""注意一个严重问题：！！
            Duplicate entry '001071' for key 'hash_check_item'")

            >>> md5_from_dict({"code": "001071"})
            '05e9ab87d2f88fbc29cf070b6241c0ea'
            >>> md5_from_dict({"code": u"001071"})
            '98f46fdaffc7e924e1c565c9f182ee6e'

    带不带u 差距巨大
    """
    sort_list = sorted(item.iteritems(), key=lambda x: x[0])
    sort_list = map(lambda s: map(str, s), sort_list)
    return hashlib.md5(str(sort_list)).hexdigest()


def current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def process_item(server, item, table=None, db=None, hash_check_item=None, unique_key='id', hash_check_enable=True):
    _save_item = item.copy()
    if not _save_item.get('save_mysql', True) or not _save_item.get('easyspider', {}).get('save_mysql', True):
        return item
    pop_key_list = ['crawled_urls_path', 'spider', 'crawled_server', 'crawled_time']
    for key in pop_key_list:
        if key in _save_item:
            _save_item.pop(key)

    hash_check_item = _save_item.pop('hash_check_item', None)
    if _save_item.get('easyspider'):
        easyspider_meta = _save_item.pop('easyspider')
    else:
        easyspider_meta = {}
    mysql_config = easyspider_meta.get('mysql_config') or {}
    table = table or mysql_config.get('table')
    db = db or mysql_config.get('db')
    if not hash_check_item:
        hash_check_item = mysql_config.get('hash_check_item')
    unique_key = mysql_config.get('unique_key')
    hash_check_enable = mysql_config.get('hash_check_enable', True)
    error_flag = False
    error_limit = 3
    error_count = 1
    while error_count <= error_limit:
        try:
            _insert_or_update(server, _save_item, table, db, hash_check_item, unique_key, hash_check_enable)
            error_flag = False
            break
        except Exception:
            error_flag = True
            logger.exception('第[%s / %s]操作数据库失败，下次再尝试' % (error_count, error_limit))
            time.sleep(2)

        error_count += 1

    if error_flag:
        _insert_or_update(server, _save_item, table, db, hash_check_item, unique_key, hash_check_enable)
    return item


def _insert_or_update(server, item, table=None, db=None, hash_check_item=None, unique_key='id', hash_check_enable=True):
    if not table:
        current_table = ''
    else:
        current_table = table
    if not db:
        current_db = ''
    else:
        current_db = db
    if not hash_check_item:
        _hash_check_item = item
    else:
        _hash_check_item = {}
        for check_item in hash_check_item:
            _hash_check_item[check_item] = item.get(check_item)

    if not unique_key:
        unique_key = 'id'
    if hash_check_enable:
        hash_code = md5_from_dict(_hash_check_item)
        query_map = 'hash_check="%s"' % hash_code
    else:
        query_map = MysqlService.join_query_map(_hash_check_item)
    check_sql = 'select %s from %s.%s where %s;' % (unique_key, current_db, current_table, query_map)
    check_result = server.query(check_sql)
    if check_result:
        unique_key_item = check_result[0].get(unique_key)
        if hash_check_enable:
            item['last_checktime'] = current_time()
        update_sql = server.update_sql_from_map(current_table, {unique_key: unique_key_item}, item, current_db).replace('%', '%%')
        logger.debug('already have record, update last_checktime, running sql is %s' % update_sql)
        server.execute(update_sql)
    else:
        if hash_check_enable:
            item['hash_check'] = hash_code
            item['last_checktime'] = current_time()
        sql = server.join_sql_from_map(current_table, item, current_db).replace('%', '%%')
        logger.debug('find a new record, insert sql is %s' % sql)
        server.execute(sql)


class commonMysqlpipeline(commonpipeline):

    def __init__(self, settings):
        self.mysql_host = settings.get('MYSQL_HOST')
        self.mysql_user = settings.get('MYSQL_USER')
        self.mysql_password = settings.get('MYSQL_PASSWORD')
        self.mysql_port = settings.get('MYSQL_PORT')
        self.mysql_db = settings.get('MYSQL_DB')
        self.mysql_table = settings.get('MYSQL_TABLE')
        self.server = MysqlService(self.mysql_host, self.mysql_user, self.mysql_password, self.mysql_port)
        self.server.select_db(self.mysql_db)

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def _process_item(self, item, spider, response):
        _save_item = item.copy()
        if not _save_item.get('save_mysql', True) or not _save_item.get('easyspider', {}).get('save_mysql', True):
            return item
        _save_item.pop('crawled_urls_path')
        _save_item.pop('spider')
        _save_item.pop('crawled_server')
        _save_item.pop('crawled_time')
        hash_check_item = _save_item.pop('hash_check_item', None)
        if _save_item.get('easyspider'):
            easyspider_meta = _save_item.pop('easyspider')
        else:
            easyspider_meta = {}
        mysql_config = easyspider_meta.get('mysql_config') or {}
        table = mysql_config.get('table')
        db = mysql_config.get('db')
        if not hash_check_item:
            hash_check_item = mysql_config.get('hash_check_item')
        unique_key = mysql_config.get('unique_key')
        hash_check_enable = mysql_config.get('hash_check_enable', True)
        error_flag = False
        error_limit = 3
        error_count = 1
        while error_count <= error_limit:
            try:
                _copy_save_item = copy.deepcopy(_save_item)
                self._insert_or_update(_copy_save_item, spider, table, db, hash_check_item, unique_key, hash_check_enable)
                error_flag = False
                break
            except Exception:
                error_flag = True
                logger.exception('第[%s / %s]操作数据库失败，下次再尝试' % (error_count, error_limit))
                time.sleep(2)

            error_count += 1

        if error_flag:
            self._insert_or_update(_save_item, spider, table, db, hash_check_item, unique_key, hash_check_enable)
        return item

    def _insert_or_update(self, item, spider, table=None, db=None, hash_check_item=None, unique_key='id', hash_check_enable=True):
        if not table:
            current_table = self.mysql_table
        else:
            current_table = table
        if not db:
            current_db = self.mysql_db
        else:
            current_db = db
        if not hash_check_item:
            _hash_check_item = item
        else:
            _hash_check_item = {}
            for check_item in hash_check_item:
                _hash_check_item[check_item] = item.get(check_item)

        if not unique_key:
            unique_key = 'id'
        if hash_check_enable:
            hash_code = md5_from_dict(_hash_check_item)
            query_map = 'hash_check="%s"' % hash_code
        else:
            query_map = MysqlService.join_query_map(_hash_check_item)
        check_sql = 'select %s from %s.%s where %s;' % (unique_key, current_db, current_table, query_map)
        check_result = self.server.query(check_sql)
        if check_result:
            unique_key_item = check_result[0].get(unique_key)
            if hash_check_enable:
                item['last_checktime'] = current_time()
            update_sql = self.server.update_sql_from_map(current_table, {unique_key: unique_key_item}, item, current_db).replace('%', '%%')
            logger.debug('already have record, update last_checktime, running sql is %s' % update_sql)
            self.server.execute(update_sql)
        else:
            if hash_check_enable:
                item['hash_check'] = hash_code
                item['last_checktime'] = current_time()
            sql = self.server.join_sql_from_map(current_table, item, current_db).replace('%', '%%')
            logger.debug('find a new record, insert sql is %s' % sql)
            self.server.execute(sql)