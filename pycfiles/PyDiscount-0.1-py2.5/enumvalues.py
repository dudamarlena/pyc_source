# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\disc\crawler\enumvalues.py
# Compiled at: 2009-04-28 19:43:06
"""
Created on 2009-4-28

@author: mingqi
"""
from disc import commutil
from disc.crawler import dbsource
from disc import sip
from disc.sip.sipproxy import SIPTaobaoProxy
from datetime import datetime
import simplejson as json
logger = commutil.get_logger('disc.sip.itemcat')

class PropertyEnum:
    """
    cid
    pid
    vid
    name
    status
    sort_order
    """
    pass


def sql_all_leaf_categories():
    """fetch all leaf category"""
    _conn = dbsource.get_conn()
    _cursor = _conn.cursor()
    _sql = '\n        select category_id from tb_item_categories where is_parent=0 and status=0\n    '
    _cursor.execute(_sql)
    _category_list = []
    _row = None
    while 1:
        _row = _cursor.fetchone()
        if not _row:
            break
        _category_list.append(_row[0])

    _cursor.close()
    return _category_list


def sql_check_timestramp(cid):
    _sql = ' \n        select last_crawl_date from tb_property_crawl_timestamp\n        where category_id=%s\n    '
    _conn = dbsource.get_conn()
    _cursor = _conn.cursor()
    _cursor.execute(_sql, cid)
    _row = _cursor.fetchone()
    _cursor.close()
    if _row:
        return _row[0]
    return


def sql_update_enum(enum_list):
    _update_sql = '\n        update TB_ENUM_VALUES set\n            PROPERTY_ID=%(pid)s,\n            CATEGORY_ID=%(cid)s,\n            ENUM_VALUE_NAME=%(name)s,\n            STATUS=%(status)s,\n            SORT_ORDER=%(sort_order)s,\n            LAST_UPDATE_DATE=now()\n        where ENUM_VALUE_ID=%(vid)s\n    '
    _insert_sql = '\n        insert into TB_ENUM_VALUES(\n            ENUM_VALUE_ID,\n            PROPERTY_ID,\n            CATEGORY_ID,\n            ENUM_VALUE_NAME,\n            STATUS,\n            SORT_ORDER,\n            CREATION_DATE,\n            LAST_UPDATE_DATE)\n        values(\n            %(vid)s,\n            %(pid)s,\n            %(cid)s,\n            %(name)s,\n            %(status)s,\n            %(sort_order)s,\n            now(),\n            now()\n        )\n    '
    _conn = dbsource.get_conn()
    _cursor = _conn.cursor()
    for _enum in enum_list:
        logger.info('pulled enum %s:%s' % (_enum.vid, _enum.name))
        _cursor.execute(_update_sql, vars(_enum))
        if _cursor.rowcount == 0:
            _cursor.execute(_insert_sql, vars(_enum))

    return True


def post_timestamp(cid, timestamp):
    _update_sql = 'update TB_ENUM_CRAWL_TIMESTAMP set LAST_CRAWL_DATE=%(timestamp)s where CATEGORY_ID=%(cid)s'
    _insert_sql = 'insert into TB_ENUM_CRAWL_TIMESTAMP(CATEGORY_ID,LAST_CRAWL_DATE) values(%(cid)s,%(timestamp)s)'
    _conn = dbsource.get_conn()
    _cursor = _conn.cursor()
    _cursor.execute(_update_sql, vars())
    if _cursor.rowcount == 0:
        _cursor.execute(_insert_sql, vars())
    return True


def crawl_enum_values(cid):
    """crawl enum values by category"""
    _proxy = SIPTaobaoProxy(sip.APP_CODE, sip.APP_SECRET)
    _args = {'fields': 'cid,pid,vid,name,is_parent,status,sort_order', 'cid': str(cid)}
    _timestamp = sql_check_timestramp(cid)
    if _timestamp:
        _args['datetime'] = _timestamp.strftime('%Y-%m-%d %H:%M:%S')
    else:
        _args['datetime'] = '1970-01-01 00:00:00'
    _res = _proxy.call_sip('taobao.itempropvalues.get', **_args)
    _json_res = json.loads(_res)
    _enum_list = []
    if _json_res['rsp'].has_key('prop_values'):
        for _enum_dict in _json_res['rsp']['prop_values']:
            _o = PropertyEnum()
            _o.cid = _enum_dict['cid']
            _o.pid = _enum_dict['pid']
            _o.vid = _enum_dict['vid']
            _o.name = _enum_dict['name']
            if _enum_dict['status'] == 'normal':
                _o.status = 0
            else:
                _o.status = 1
            _o.sort_order = int(_enum_dict['sort_order'])
            _enum_list.append(_o)

    return _enum_list


if __name__ == '__main__':
    for _category_id in sql_all_leaf_categories():
        sql_update_enum(crawl_enum_values(_category_id))
        post_timestamp(_category_id, datetime.now())