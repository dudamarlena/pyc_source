# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python\automation\projects\test\tests\example\debugtalk.py
# Compiled at: 2019-03-06 07:06:43
# Size of source mod 2**32: 985 bytes
from zybats.ext.appext.dbUtil import Db
from zybats.ext.appext.redisUtil import RedisSingleNode
import os

def get_base_url():
    url = os.environ['url']
    return url


def query_mysql_one_result(sql_str):
    ip = '192.168.240.197'
    port = 8888
    user_name = 'root'
    password = 'root'
    db_name = 'adx_admin'
    dbClient = Db(ip, port, user_name, password, db_name)
    result = dbClient.select(sql_str)
    return result[0][0]


def get_redis_str_value(key):
    ip = '192.168.240.98'
    port = 6379
    client = RedisSingleNode(ip, port)
    v = client.get(key)
    return v.decode()


def show_request_function(request_body, replace_app_id):
    print('You can do something here! for example:')
    request_body['json']['appId'] = replace_app_id
    print('Replaced request body is:', request_body)


def show_response_function(response_body, id):
    print('You can do something here! for example:')
    print(response_body)


if __name__ == '__main__':
    aaa = 'aaa'