# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mysql_util/mysql_util.py
# Compiled at: 2018-06-11 21:10:46
import os, re, time, pymysql, datetime
try:
    MYSQL_HOST = __conf__.MYSQL_HOST
    MYSQL_USER = __conf__.MYSQL_USER
    MYSQL_PASSWORD = __conf__.MYSQL_PASSWORD
    MYSQL_NAME = __conf__.MYSQL_NAME
except Exception as e:
    pass

try:
    from settings import *
except Exception as e:
    pass

def mongo_conv(d):
    if isinstance(d, (datetime.datetime, datetime.date)):
        return str(d)
    else:
        if isinstance(d, (unicode,)):
            return str(d.encode('utf-8'))
        if isinstance(d, list):
            return map(mongo_conv, d)
        if isinstance(d, tuple):
            return tuple(map(mongo_conv, d))
        if isinstance(d, dict):
            return dict([ (mongo_conv(k), mongo_conv(v)) for k, v in d.items() ])
        return d


def Conn(db_host=None, db_user=None, db_password=None, db_name=None, **kwargs):
    db_host = db_host or MYSQL_HOST
    db_user = db_user or MYSQL_USER
    db_password = db_password or MYSQL_PASSWORD
    db_name = db_name or MYSQL_NAME
    return pymysql.connect(host=db_host, user=db_user, passwd=db_password, db=db_name, charset='utf8')


def m_execute(sql, **kwargs):
    u"""
        保存数据
    """
    conn = Conn(**kwargs)
    conn.cursor().execute(sql)
    conn.commit()


def m_query_one(sql, fields, **kwargs):
    u"""
        查询单条记录
    """
    conn = Conn(**kwargs)
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchall()
    if rs:
        rs = rs[0]
        rs = dict((fields[i], rs[i]) for i in range(len(rs)))
        return mongo_conv(rs)
    return {}


def m_query(sql, fields, **kwargs):
    u"""
        查询列表数据
        支持分页
    """
    page_index = int(kwargs.pop('page_index', 1)) or 1
    page_size = int(kwargs.pop('page_size', 10))
    findall = kwargs.pop('findall', None)
    sorts = kwargs.pop('sorts', None)
    sql_count = re.sub('select.*from', 'select count(*) from', sql)
    count = m_query_one(sql_count, ('count', ), **kwargs)['count']
    if count and findall:
        page_index = 1
        page_size = count
    page_num = (count + page_size - 1) / page_size
    if page_num < page_index:
        page_index = page_num
    page = dict(page_index=page_index, page_size=page_size, page_num=page_num, allcount=count)
    if page_num == 0:
        return ([], page)
    else:
        sql += (' limit {},{}').format((page_index - 1) * page_size, page_size)
        if sorts:
            sql += (' {}').format(sorts)
        conn = Conn(**kwargs)
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
        data = []
        if fields:
            for r in rs:
                d = dict((fields[i], r[i]) for i in range(len(r)))
                data.append(d)

        return (
         mongo_conv(data), page)


def m_count(sql, **kwargs):
    u"""
        查询个数
    """
    return m_query_one(sql, ('count', ), **kwargs).get('count') or 0