# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/utils/DBService.py
# Compiled at: 2017-09-02 02:31:39
"""DB tools

"""
import json, copy, logging, threading
from collections import Iterable
from importlib import import_module
import threading
logger = logging.getLogger(__name__)

class DBService(threading.local):

    def __getattr__(self, key):
        logger.debug('menthod or attribute %s does no exists, now will be interperted call as <self.server.%s>' % (key, key))
        return eval("super(DBService, self).__getattribute__('server').%s" % key)


class RedisService(DBService):
    """this class is an improvement to the native python redis class.
    it has overwirte some function to make you use redis more convenient.

    it just overwrite the methods in native redis(but did not inherit it),
    so the methods name are keep the same, that means you don't need to adapt
    new api.
    one of the most amazing thing is, this class use `__getattr__` to bind
    unoverwritten's native redis method on  itself,

    when the method you called didn't exist
    in this class(but exists in native redis), you can also call it because at
    this time, you call will be interperted as call a Redis object.

    for example
        1. it has overwrite redis `rpush`, in this rpush, it
        will auto check the argument is list or string and if argument
        is provide as list type(iterable type), it will use redis pipe
        to transfer the command and just submit once.

        2. if the method is not overwritetn, you can also use it because
        when the method is not exists, your call will be interperted as
        call Redis object.
    """

    def __init__(self, redis_url):
        self.redis = import_module('redis')
        pool = self.redis.ConnectionPool.from_url(redis_url)
        self.server = self.redis.StrictRedis(connection_pool=pool)

    def join_pipe_commands(self, key, vals, op):
        """if given a large list or set to insert, it will auto call _pipe"""
        _pipe = self.server.pipeline()
        if isinstance(vals, str) or isinstance(vals, unicode):
            eval('_pipe.%s(key, vals)' % op)
        elif isinstance(vals, Iterable):
            logger.debug('start join redis pipe...')
            for val in vals:
                eval('_pipe.%s(key, isinstance(val, dict) and json.dumps(val, ensure_ascii=False) or val)' % op)

        else:
            logger.error("rpush vals %s's type is no avaliabled, type is %s" % (vals, type(vals)))
            return
        logger.debug('join redis pipe complete...start transfer to server')
        return _pipe.execute()

    def rpush(self, key, vals):
        return self.join_pipe_commands(key, vals, 'rpush')

    def sadd(self, key, vals):
        return self.join_pipe_commands(key, vals, 'sadd')


class MongoService(DBService):
    """all function args isn't bind at self, so you can directily use like this
    when you first use mongo connection ,it will bind with instance, and next time
    wher you use it, it will auto check if the instnace bind address has changed

    >>>server = MongoService()
    >>>server.find_all("mongodb://localhost:27017", "test")
    >>>server.find_all("mongodb://114.114.114.114:27017", "test")

    """

    def __init__(self, url=None, db=None):
        self.pymongo = import_module('pymongo')
        self.errors = import_module('pymongo.errors')
        if url:
            self.get_mongo_connection(url, db)

    def get_mongo_connection(self, url, db):
        self.current_mongo_url = url
        self.current_mongo_db = db
        try:
            self.server = self.pymongo.MongoClient(url)
        except self.errors.InvalidURI:
            logger.exception('mongourl <%s> is invalid...' % url)
            exit(-1)

        self.select_db(db)

    def select_db(self, db=None):
        if db:
            self.db = self.server[db]
            self.current_mongo_db = db
        else:
            try:
                self.db = self.server.get_default_database()
                self.current_mongo_db = db
            except self.errors.ConfigurationError:
                self.db = None

        return

    def find_one(self, collection, query_sql):
        """actually the function will call function find_limit and give the limit argument as 1"""
        return self.find_limit(collection, query_sql, 1)

    def find_all(self, collection, query_sql):
        """alike the function find_one, actually call find_limit"""
        return self.find_limit(collection, query_sql, 0)

    def find_limit(self, collection, query_sql, limit):
        """alike find_one, actually call function find_limit_and_skip"""
        return self.find_limit_and_skip(collection, query_sql, limit, 0)

    def find_limit_and_skip(self, collection, query_sql, limit, skip):
        """alike find_limit, actually call function find"""
        return self.find(collection, query_sql, limit, skip)

    def find(self, collection, query_sql, limit_count, skip_count=0, fetch_rate=5000):
        """ the <root> function when you run 'query' commands will called.
        no matter what query commands is(find_one or find_all or find_limit, etc.), actually it just the different kind
        of arguments to called this root function `find`.

        find is from pymongo.collection.find, ref: https://api.mongodb.com/python/current/api/pymongo/collection.html
        but i wanner explain what the argument `fetch_rate` is:

        when your query return a large numbers of result(like use find_all, to extract all result in a collection),
        you may wait until query done and fetch completed for a long time. during this period, you don't know
        how many querys has been done or even if query still alive(sometime the query will crashed).
        fetch_rate is the argument that control how many results to fetch in one time(default to 5k), and with the fetch_rate,
        you can directily know the query rate.
        """
        result_count = self.db[collection].find(query_sql, limit=limit_count, skip=skip_count).count(with_limit_and_skip=True)
        rate, result_list = 0, []
        while rate < result_count:
            result_list.extend([ i.pop('_id') and eval(json.dumps(i, ensure_ascii=False)) for i in self.db[collection].find(query_sql, limit=fetch_rate if limit_count > fetch_rate else limit_count, skip=rate if rate > skip_count else skip_count)
                               ])
            rate += fetch_rate
            logger.debug('fetch rate: [%d / %d]' % (rate, result_count))

        return result_list

    def insert(self, collection, document):
        """auto check insert many or insert_one"""
        document_copy = copy.deepcopy(document)
        __insert = self.db[collection].insert_many([document_copy] if type(document_copy) not in (list, set, tuple) else document_copy)
        return len(__insert.inserted_ids)

    def replace_one(self, collection, query_sql, document):
        """mongo save(replace), has not save multi argument, replace or save can only replace one"""
        document_copy = copy.deepcopy(document)
        __replace = self.db[collection].replace_one(query_sql, document_copy)
        return __replace.modified_count

    def delete_one(self, collection, query_sql):
        return self.delete(collection, query_sql)

    def delete_all(self, collection, query_sql):
        return self.delete_all(collection, query_sql, True)

    def delete(self, collection, query_sql, multi=False):
        """merge delete_one and delete_many by use argument multi"""
        __delete = (multi or self.db[collection].delete_one)(query_sql) if 1 else self.db[collection].delete_many(query_sql)
        return __delete.deleted_count

    def list_all_collections(self, db=None):
        if not db or self.current_mongo_db == db:
            return self.convert_unciode_result(self.db.collection_names())
        else:
            self.select_db(db)
            return self.list_all_collections(db)

    def list_all_dbs(self):
        """ convert [u"admin", u"local"] -> ["admin", "local"]"""
        return self.convert_unciode_result(self.server.database_names())

    def collection_result_count(self, collection):
        return self.db[collection].count()

    def convert_unciode_result(self, result):
        u""" convert [u"admin", u"local"] -> ["admin", "local"]
        or {u"中文": u"not bad"} -> {"中文": "not bad"}
        because somethings bas will occur when the result is not in english
        """
        return eval(json.dumps(result, ensure_ascii=False))


class MysqlService(DBService):

    @classmethod
    def join_sql_from_map(cls, insert_table, args_map):
        """ magic method, surprise method, a very helpful method to
        allow you generate insert sql script from a dict.

        e.g:
        >>>MysqlService.join_sql_from_map("test_table", {"first_name": "zhang", "last_name": "yiTian"})
        >>>'insert into test_table(`first_name`,`last_name`) value("zhang","yiTian");'

        >>>MysqlService.join_sql_from_map("test_table", {"first_name": "zhang", "last_name": 'yi"Tian'})
        >>>'insert into test_table(`first_name`,`last_name`) value("zhang","yi"Tian");'

        with the help of this method, you no longer warry about how to generate a sql script.
        """
        sql_template = 'insert into %s(%s) value(%s);'
        dict_list = args_map.items()
        fields = (',').join(map(lambda x: '`%s`' % x[0], dict_list))
        value = (',').join(map(lambda x: '"%s"' % x[1].replace('"', '\\"'), dict_list))
        return sql_template % (insert_table, fields, value)

    def __init__(self):
        pass


def test_mongo_service():
    server = MongoService('mongodb://localhost:27017/easyspider')
    print 'all mongo dbs are %s' % server.list_all_dbs()
    print "db easyspider's collections are %s" % server.list_all_collections()
    print "db easyspider's collections are %s" % server.easyspider.collection_names()
    print "db admin's collections are %s" % server.list_all_collections('admin')
    print 'select db easyspider again', server.select_db('easyspider')
    insert_result = {'test': 'hello'}
    print 'insert %s ' % insert_result, server.insert('test_collection', insert_result)
    insert_result = [{'info2': ['1', '中文', 'english']}, {'info2': ['2', '中文', 'english']}]
    print 'insert %s ' % insert_result, server.insert('test_collection', insert_result)
    insert_result = ({'info2': ['1', '中文', 'english']},
     {'info2': [
                '2', '中文', 'english']})
    print 'insert %s ' % str(insert_result), server.insert('test_collection', insert_result)
    print 'find one in test_collection ', server.find_one('test_collection', {})
    print 'find all in test_collection ', server.find_all('test_collection', {})
    collection_result_count = server.collection_result_count('test_collection')
    print 'test_collection have %s result' % collection_result_count
    print 'test_collection last result is %s' % server.find_limit_and_skip('test_collection', {}, 1, collection_result_count - 1)
    print 'test del one %s' % server.delete('test_collection', {})
    collection_result_count = server.collection_result_count('test_collection')
    print 'test_collection have %s result' % collection_result_count
    print 'test del all %s' % server.delete('test_collection', {}, multi=True)


def test_redis_service():
    server = RedisService('redis://127.0.0.1')
    print server.server.ping()
    print server.ping()
    print server.rpush('test', [ i for i in range(10) ])
    print server.rpush('test2', ['hello', {'zhang': 'yiTian'}, 3])
    print server.sadd('test3', 'ni hao')
    print server.sadd('test4', ['你好', 'China'])
    print server.hset('test5', 'zhang', {'Tian': 1})
    print server.hset('test5', '中国', 'no bad')
    print server.hgetall('test5')
    print server.hgetall('test5').keys()[0], server.hgetall('test5').values()[0]


def test_mysql_service():
    print MysqlService.join_sql_from_map('test_table', {'first_name': 'zhang', 'last_name': 'yiTian'})
    print MysqlService.join_sql_from_map('test_table', {'first_name': 'zhang', 'last_name': 'yi"Tian'})


def main():
    test_mysql_service()


if __name__ == '__main__':
    main()