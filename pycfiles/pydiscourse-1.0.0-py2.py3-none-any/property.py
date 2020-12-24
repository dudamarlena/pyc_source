# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\disc\crawler\property.py
# Compiled at: 2009-04-28 19:46:18
__doc__ = '\nCreated on 2009-4-25\n\n@author: mingqi\n'
from disc import commutil
from disc.crawler import dbsource
from disc import sip
from disc.sip.sipproxy import SIPTaobaoProxy
from datetime import datetime
import simplejson as json
logger = commutil.get_logger('disc.sip.itemcat')

class ItemProperty:
    """
    pid
    name
    parent_pid
    parent_vid
    status
    is_key
    is_sale
    is_color
    is_enum
    is_input
    sort_order
    """


def get_leaf_categories():
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


def get_timestamp(cid):
    _sql = ' \n        select last_crawl_date from tb_property_crawl_timestamp\n        where category_id=%s\n    '
    _conn = dbsource.get_conn()
    _cursor = _conn.cursor()
    _cursor.execute(_sql, cid)
    _row = _cursor.fetchone()
    _cursor.close()
    if _row:
        return _row[0]
    return


def update_properties(property_list):
    _update_sql = ' update tb_properties set\n            name = %(name)s,\n            PARENT_PROPERTY_ID = %(parent_pid)s,\n            PARENT_VALUE_ID = %(parent_vid)s,\n            IS_KEY = %(is_key)s,\n            IS_SALE = %(is_sale)s,\n            IS_INPUT = %(is_input)s,\n            IS_ENUM = %(is_enum)s,\n            IS_COLOR = %(is_color)s,\n            STATUS = %(status)s,\n            SORT_ORDER = %(sort_order)s,\n            LAST_UPDATE_DATE = now()\n        where PROPERTY_ID=%(pid)s\n    '
    _insert_sql = ' insert into tb_properties(\n                        PROPERTY_ID,\n                        name,\n                        PARENT_PROPERTY_ID,\n                        PARENT_VALUE_ID,\n                        IS_KEY,\n                        IS_SALE,\n                        IS_INPUT,\n                        IS_ENUM,\n                        IS_COLOR,\n                        STATUS,\n                        SORT_ORDER,\n                        CREATION_DATE,\n                        LAST_UPDATE_DATE\n                    ) values(\n                        %(pid)s,\n                        %(name)s,\n                        %(parent_pid)s,\n                        %(parent_vid)s,\n                        %(is_key)s,\n                        %(is_sale)s,\n                        %(is_input)s,\n                        %(is_enum)s,\n                        %(is_color)s,\n                        %(status)s,\n                        %(sort_order)s,\n                        now(),\n                        now()\n                    )'
    _conn = dbsource.get_conn()
    _cursor = _conn.cursor()
    for _property in property_list:
        logger.info('scraped property %s: %s' % (_property.pid, _property.name))
        _cursor.execute(_update_sql, vars(_property))
        if _cursor.rowcount == 0:
            _cursor.execute(_insert_sql, vars(_property))

    return True


def post_timestamp(cid, timestamp):
    _update_sql = 'update TB_PROPERTY_CRAWL_TIMESTAMP set LAST_CRAWL_DATE=%(timestamp)s where CATEGORY_ID=%(cid)s'
    _insert_sql = 'insert into TB_PROPERTY_CRAWL_TIMESTAMP(CATEGORY_ID,LAST_CRAWL_DATE) values(%(cid)s,%(timestamp)s)'
    _conn = dbsource.get_conn()
    _cursor = _conn.cursor()
    _cursor.execute(_update_sql, vars())
    if _cursor.rowcount == 0:
        _cursor.execute(_insert_sql, vars())
    return True


def crawl_properties(cid, parent_pid=None):
    _proxy = SIPTaobaoProxy(sip.APP_CODE, sip.APP_SECRET)
    _args = {'fields': 'pid,name,parent_pid,parent_vid,status,                        is_enum_prop, is_key_prop,                        is_sale_prop,is_color_prop,                        is_input_prop,sort_order', 
       'cid': str(cid)}
    _timestamp = get_timestamp(cid)
    if _timestamp:
        _args['datetime'] = _timestamp.strftime('%Y-%m-%d %H:%M:%S')
    else:
        _args['datetime'] = '1970-01-01 00:00:00'
    if parent_pid:
        _args['parent_pid'] = str(parent_pid)
    _res = _proxy.call_sip('taobao.itemprops.get.v2', **_args)
    _json_res = json.loads(_res)
    _property_list = []
    if _json_res['rsp'].has_key('item_props'):
        for _prop_dict in _json_res['rsp']['item_props']:
            _o = ItemProperty()
            _o.pid = _prop_dict['pid']
            _o.name = _prop_dict['name']
            _o.is_key = bool(_prop_dict['is_key_prop'])
            _o.is_sale = bool(_prop_dict['is_sale_prop'])
            _o.is_color = bool(_prop_dict['is_color_prop'])
            _o.is_enum = bool(_prop_dict['is_enum_prop'])
            _o.is_input = bool(_prop_dict['is_input_prop'])
            if _prop_dict['status'] == 'normal':
                _o.status = 0
            else:
                _o.status = 1
            _o.sort_order = int(_prop_dict['sort_order'])
            if _prop_dict['parent_pid'] == '0':
                _o.parent_pid = None
            else:
                _o.parent_pid = _prop_dict['parent_pid']
            if _prop_dict['parent_vid'] == '0':
                _o.parent_vid = None
            else:
                _o.parent_vid = _prop_dict['parent_vid']
            _property_list.append(_o)

    return _property_list


if __name__ == '__main__':
    for category_id in get_leaf_categories():
        update_properties(crawl_properties(category_id))
        post_timestamp(category_id, datetime.now())