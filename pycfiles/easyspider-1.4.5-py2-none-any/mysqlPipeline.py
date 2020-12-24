# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/pipelines/mysqlPipeline.py
# Compiled at: 2018-02-28 09:29:19
import time, logging, hashlib
from DBService import MysqlService
from twisted.internet.threads import deferToThread
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


class mysqlPipeline(object):

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

    def process_item(self, item, spider):
        print '\n\n\n\n\n%s\n' % item
        return item

    def insert_or_update(self, item, spider, table=None, db=None, hash_check_item=None):
        return deferToThread(self._insert_or_update, item, spider, table, db, hash_check_item)

    def _insert_or_update(self, item, spider, table=None, db=None, hash_check_item=None):
        if not hash_check_item:
            _hash_check_item = item
        else:
            _hash_check_item = {}
            for check_item in hash_check_item:
                _hash_check_item[check_item] = item.get(check_item)

        hash_code = md5_from_dict(_hash_check_item)
        if not table:
            current_table = self.mysql_table
        else:
            current_table = table
        if not db:
            current_db = self.mysql_db
        else:
            current_db = db
        hashcode_list = self.server.query('select id from %s.%s where hash_check="%s";' % (
         current_db, current_table, hash_code))
        if hashcode_list:
            record_id = hashcode_list[0].get('id')
            item['last_checktime'] = current_time()
            update_sql = self.server.update_sql_from_map(current_table, {'id': record_id}, item, current_db).replace('%', '%%')
            logger.debug('already have record, update last_checktime, running sql is %s' % update_sql)
            self.server.execute(update_sql)
        else:
            item['hash_check'] = hash_code
            item['last_checktime'] = current_time()
            sql = self.server.join_sql_from_map(current_table, item, current_db).replace('%', '%%')
            logger.debug('find a new record, insert sql is %s' % sql)
            self.server.execute(sql)